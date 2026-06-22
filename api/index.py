import os
import sys
import json
from datetime import datetime, timezone

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import text

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from models import db, User, Result, Test, Vocabulary, Question

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
    static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.get_database_uri()


@app.template_filter('fromjson')
def fromjson_filter(value):
    try:
        return json.loads(value)
    except:
        return []

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


with app.app_context():
    db.create_all()
    try:
        db.session.execute(db.text('ALTER TABLE test ADD COLUMN passage TEXT'))
        db.session.commit()
    except:
        db.session.rollback()


_translations = {}
_tr_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'translations')
if os.path.isdir(_tr_path):
    for f in os.listdir(_tr_path):
        if f.endswith('.json'):
            lang = f.replace('.json', '')
            with open(os.path.join(_tr_path, f), 'r', encoding='utf-8') as fh:
                _translations[lang] = json.load(fh)


def _(key, lang='uz'):
    return _translations.get(lang, _translations.get('uz', {})).get(key, key)


@app.context_processor
def inject_globals():
    lang = request.cookies.get('lang', 'uz')
    return dict(_=lambda k: _(k, lang), lang=lang, current_lang=lang)


@app.route('/set-lang/<lang>')
def set_lang(lang):
    if lang in ('uz', 'en', 'ru'):
        resp = redirect(request.referrer or '/')
        resp.set_cookie('lang', lang, max_age=365*24*3600)
        return resp
    return redirect('/')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return render_template('register.html')
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return render_template('register.html')
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/reading')
def reading():
    tests = Test.query.filter_by(type='reading').all()
    return render_template('reading.html', tests=tests)


@app.route('/reading/<int:test_id>')
def reading_test(test_id):
    test = db.session.get(Test, test_id)
    if not test or test.type != 'reading':
        return redirect(url_for('reading'))
    questions = Question.query.filter_by(test_id=test.id).order_by(Question.order).all()
    return render_template('reading_test.html', test=test, questions=questions)


@app.route('/api/check-answers', methods=['POST'])
def check_answers():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    answers = data.get('answers', {})
    test_id = data.get('test_id')
    questions = Question.query.filter_by(test_id=test_id).order_by(Question.order).all()
    correct = 0
    total = len(questions)
    results = []
    for q in questions:
        user_ans = answers.get(str(q.id), '').strip()
        correct_ans = q.correct_answer.strip()
        is_correct = user_ans.lower() == correct_ans.lower()
        if is_correct:
            correct += 1
        results.append({
            'id': q.id,
            'correct': is_correct,
            'user_answer': user_ans,
            'correct_answer': correct_ans,
            'question_text': q.question_text
        })
    return jsonify({
        'score': correct,
        'total': total,
        'percentage': round(correct / total * 100, 1) if total else 0,
        'results': results
    })


@app.route('/listening')
def listening():
    tests = Test.query.filter_by(type='listening').all()
    return render_template('listening.html', tests=tests)


@app.route('/listening/<int:test_id>')
def listening_test(test_id):
    test = db.session.get(Test, test_id)
    if not test or test.type != 'listening':
        return redirect(url_for('listening'))
    return render_template('listening_test.html', test=test)


@app.route('/writing')
def writing():
    topics = Test.query.filter_by(type='writing').all()
    return render_template('writing.html', topics=topics)


@app.route('/speaking')
def speaking():
    questions = Test.query.filter_by(type='speaking').all()
    return render_template('speaking.html', questions=questions)


@app.route('/vocabulary')
def vocabulary():
    words = Vocabulary.query.all()
    categories = db.session.query(Vocabulary.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]
    return render_template('vocabulary.html', words=words, categories=categories)


@app.route('/mock-exam')
def mock_exam():
    return render_template('mock_exam.html')


@app.route('/results')
@login_required
def results():
    user_results = Result.query.filter_by(user_id=current_user.id).order_by(Result.created_at.desc()).all()
    return render_template('results.html', results=user_results)


@app.route('/leaderboard')
def leaderboard():
    top_users = User.query.order_by(User.score.desc()).limit(50).all()
    return render_template('leaderboard.html', top_users=top_users)


_cefr_levels = {
    'a1': 'Beginner',
    'a2': 'Elementary',
    'b1': 'Intermediate',
    'b2': 'Upper Intermediate',
    'c1': 'Advanced',
    'c2': 'Proficient',
}


@app.route('/cefr')
def cefr():
    return render_template('cefr.html')


@app.route('/cefr/<level>')
def cefr_level(level):
    level = level.lower()
    if level not in _cefr_levels:
        return redirect(url_for('cefr'))
    return render_template('cefr_level.html', level=level, name=_cefr_levels[level])


@app.route('/api/submit-result', methods=['POST'])
@login_required
def submit_result():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No data provided'}), 400
    result = Result(
        user_id=current_user.id,
        test_type=data.get('test_type', 'unknown'),
        score=data.get('score', 0),
        total=data.get('total', 0),
        details=data.get('details', '')
    )
    db.session.add(result)
    current_user.score = (current_user.score or 0) + int(data.get('score', 0))
    db.session.commit()
    return jsonify({'status': 'ok'})


@app.route('/api/vocabulary/random')
def random_vocabulary():
    word = Vocabulary.query.order_by(db.func.random()).first()
    if word:
        return jsonify({
            'word': word.word,
            'translation': word.translation,
            'definition': word.definition,
            'example': word.example,
            'category': word.category
        })
    return jsonify({'error': 'No words found'}), 404


@app.route('/api/leaderboard')
def api_leaderboard():
    top = User.query.order_by(User.score.desc()).limit(50).all()
    return jsonify([{
        'username': u.username,
        'score': u.score or 0,
        'is_premium': u.is_premium
    } for u in top])


handler = app
