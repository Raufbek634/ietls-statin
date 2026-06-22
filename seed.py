"""
Seed script — populates database with sample data.
Run: python seed.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.index import app
from models import db, Test, Vocabulary

with app.app_context():
    db.create_all()

    # Seed vocabulary
    words = [
        ("analyze", "tahlil qilmoq", "To examine something in detail", "The data was analyzed carefully.", "Academic"),
        ("significant", "ahamiyatli", "Important or notable", "There was a significant increase in sales.", "Academic"),
        ("consequently", "natijada", "As a result", "The weather was bad; consequently, the event was canceled.", "Linking"),
        ("demonstrate", "ko'rsatmoq", "To show clearly", "The experiment demonstrates the theory.", "Academic"),
        ("environment", "atrof-muhit", "The surroundings or conditions", "We must protect the environment.", "Environment"),
        ("global", "global, jahon", "Relating to the whole world", "Global warming is a serious issue.", "Environment"),
        ("tradition", "an'ana", "A long-established custom", "This tradition dates back centuries.", "Culture"),
        ("diverse", "xilma-xil", "Showing a great deal of variety", "The city has a diverse population.", "Culture"),
        ("economy", "iqtisodiyot", "The state of a country's trade and money", "The economy is growing steadily.", "Economics"),
        ("investment", "investitsiya", "The act of putting money into something", "Education is a good investment.", "Economics"),
        ("technology", "texnologiya", "Application of scientific knowledge", "Technology is advancing rapidly.", "Technology"),
        ("innovation", "yangilik, innovatsiya", "A new method or product", "Innovation drives progress.", "Technology"),
        ("benefit", "foyda", "An advantage or profit", "Regular exercise has many benefits.", "Health"),
        ("nutrition", "ovqatlanish", "The process of providing food", "Good nutrition is essential for health.", "Health"),
        ("urban", "shahar", "Relating to a city", "Urban areas are growing fast.", "Geography"),
        ("rural", "qishloq", "Relating to the countryside", "Rural communities rely on farming.", "Geography"),
    ]

    for word, translation, definition, example, category in words:
        if not Vocabulary.query.filter_by(word=word).first():
            db.session.add(Vocabulary(
                word=word,
                translation=translation,
                definition=definition,
                example=example,
                category=category
            ))

    # Seed reading tests
    reading_tests = [
        ("The History of the Internet", "Academic reading passage about internet development", "hard"),
        ("Climate Change Effects", "Academic passage about climate change impact", "medium"),
        ("Education Systems Around the World", "Comparison of different education systems", "medium"),
    ]

    for title, desc, difficulty in reading_tests:
        if not Test.query.filter_by(title=title, type='reading').first():
            db.session.add(Test(
                type='reading',
                title=title,
                description=desc,
                content=f"Sample passage for: {title}\n\nThis is a placeholder reading passage. In production, this would contain the full reading text with questions.",
                difficulty=difficulty
            ))

    # Seed listening tests
    listening_tests = [
        ("Conversation: University Registration", "Listening Part 1 - conversation", "easy"),
        ("Lecture: Marine Biology", "Listening Part 4 - academic lecture", "hard"),
    ]

    for title, desc, difficulty in listening_tests:
        if not Test.query.filter_by(title=title, type='listening').first():
            db.session.add(Test(
                type='listening',
                title=title,
                description=desc,
                content=f"Transcript for: {title}\n\nThis is a placeholder transcript. In production, this would include an audio player with the listening recording.",
                difficulty=difficulty
            ))

    # Seed writing topics
    writing_topics = [
        ("Task 1: Chart Description", "Describe the given chart about energy consumption", "medium"),
        ("Task 2: Education", "Some people think that university education should be free. Discuss.", "medium"),
        ("Task 2: Environment", "What are the main causes of environmental pollution? Suggest solutions.", "hard"),
    ]

    for title, desc, difficulty in writing_topics:
        if not Test.query.filter_by(title=title, type='writing').first():
            db.session.add(Test(
                type='writing',
                title=title,
                description=desc,
                content=f"Writing task: {title}\n\n{desc}",
                difficulty=difficulty
            ))

    # Seed speaking questions
    speaking_questions = [
        ("Part 1: Work/Study", "Do you work or study? What do you do?", "easy"),
        ("Part 1: Hobbies", "What do you do in your free time?", "easy"),
        ("Part 2: Describe a Place", "Describe a place you visited that you liked.", "medium"),
        ("Part 3: Technology", "How has technology changed the way people communicate?", "hard"),
    ]

    for title, desc, difficulty in speaking_questions:
        if not Test.query.filter_by(title=title, type='speaking').first():
            db.session.add(Test(
                type='speaking',
                title=title,
                description=desc,
                content=f"Speaking question: {title}\n\n{desc}",
                difficulty=difficulty
            ))

    db.session.commit()
    print("Seed data added successfully!")
