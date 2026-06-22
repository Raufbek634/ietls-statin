import os
import sys
from datetime import datetime, timezone

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from models import db, User, Result, Test, Vocabulary

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
    static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.get_database_uri()

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


with app.app_context():
    db.create_all()
    if not Vocabulary.query.first():
        _words = [
            ("analyze","tahlil qilmoq","To examine in detail","The data was analyzed carefully.","Academic"),
            ("significant","ahamiyatli","Important or notable","A significant increase was observed.","Academic"),
            ("consequently","natijada","As a result","The weather was bad; consequently, the event was canceled.","Linking"),
            ("demonstrate","ko'rsatmoq","To show clearly","The experiment demonstrates the theory.","Academic"),
            ("environment","atrof-muhit","The surroundings or conditions","We must protect the environment.","Environment"),
            ("global","global, jahon","Relating to the whole world","Global warming is a serious issue.","Environment"),
            ("tradition","an'ana","A long-established custom","This tradition dates back centuries.","Culture"),
            ("diverse","xilma-xil","Showing variety","The city has a diverse population.","Culture"),
            ("economy","iqtisodiyot","The state of trade and money","The economy is growing steadily.","Economics"),
            ("investment","investitsiya","Putting money into something","Education is a good investment.","Economics"),
            ("technology","texnologiya","Application of scientific knowledge","Technology is advancing rapidly.","Technology"),
            ("innovation","yangilik","A new method or product","Innovation drives progress.","Technology"),
            ("benefit","foyda","An advantage or profit","Regular exercise has many benefits.","Health"),
            ("nutrition","ovqatlanish","The process of providing food","Good nutrition is essential.","Health"),
            ("urban","shahar","Relating to a city","Urban areas are growing fast.","Geography"),
            ("rural","qishloq","Relating to the countryside","Rural communities rely on farming.","Geography"),
        ]
        for w,t,d,e,c in _words:
            db.session.add(Vocabulary(word=w,translation=t,definition=d,example=e,category=c))
        for title,desc,diff in [("The History of the Internet","Academic reading passage","hard"),("Climate Change Effects","Academic passage about climate","medium")]:
            db.session.add(Test(type='reading',title=title,description=desc,difficulty=diff))
        for title,desc,diff in [("Conversation: University Registration","Listening Part 1","easy"),("Lecture: Marine Biology","Listening Part 4","hard")]:
            db.session.add(Test(type='listening',title=title,description=desc,difficulty=diff))
        for title,desc,diff in [("Task 1: Chart Description","Describe a chart about energy","medium"),("Task 2: Education","Should university be free? Discuss.","medium")]:
            db.session.add(Test(type='writing',title=title,description=desc,difficulty=diff))
        for title,desc,diff in [("Part 1: Work/Study","Do you work or study?","easy"),("Part 2: Describe a Place","Describe a place you visited.","medium"),("Part 3: Technology","How has technology changed communication?","hard")]:
            db.session.add(Test(type='speaking',title=title,description=desc,difficulty=diff))
        db.session.commit()


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
    return render_template('reading_test.html', test=test)


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
