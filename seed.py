import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def seed_data():
    from models import db, Test, Vocabulary, Question

    if not Vocabulary.query.first():
        for w,t,d,e,c in [
            ("analyze","tahlil qilmoq","To examine in detail","The data was analyzed carefully.","Academic"),
            ("significant","ahamiyatli","Important","A significant increase was observed.","Academic"),
            ("consequently","natijada","As a result","The weather was bad; consequently it was canceled.","Linking"),
            ("demonstrate","ko'rsatmoq","To show clearly","The experiment demonstrates the theory.","Academic"),
            ("environment","atrof-muhit","The surroundings","Protect the environment.","Environment"),
            ("global","global","Relating to the whole world","Global warming is serious.","Environment"),
            ("tradition","an'ana","Long-established custom","This tradition dates back centuries.","Culture"),
            ("diverse","xilma-xil","Showing variety","The city has a diverse population.","Culture"),
            ("economy","iqtisodiyot","Trade and money","The economy is growing.","Economics"),
            ("investment","investitsiya","Putting money into something","Education is a good investment.","Economics"),
            ("technology","texnologiya","Application of scientific knowledge","Technology is advancing.","Technology"),
            ("innovation","yangilik","A new method","Innovation drives progress.","Technology"),
        ]:
            db.session.add(Vocabulary(word=w,translation=t,definition=d,example=e,category=c))
        db.session.commit()
        print("Vocabulary seeded")

    # Always refresh test data (clear old, add fresh with passages and questions)
    Question.query.delete()
    Test.query.delete()
    db.session.commit()
    _seed_reading_tests()
    _seed_listening_tests()
    _seed_writing_tests()
    _seed_speaking_tests()
    db.session.commit()
    print("All tests seeded")


def _seed_reading_tests():
    from models import db, Test, Question
    
    passage1 = """The history of the electric vehicle (EV) is far longer than most people realize. While many assume that EVs are a recent phenomenon driven by modern environmental concerns, the first electric vehicles actually appeared in the early 19th century.

In the 1830s, inventors in Hungary, the Netherlands, and the United States began experimenting with battery-powered vehicles. The first practical EV was built by Thomas Davenport in the United States in 1834, but it was limited to running on a short circular track. By the late 1800s, electric cars had become quite popular in urban areas because they were quiet, easy to drive, and did not emit the unpleasant fumes associated with gasoline-powered cars.

However, the popularity of EVs was short-lived. The discovery of large petroleum reserves in Texas and the Middle East made gasoline cheap and abundant. At the same time, Charles Kettering invented the electric starter in 1912, which eliminated the need for hand-cranking a gasoline engine. This made gasoline cars much more convenient. By the 1930s, electric vehicles had all but disappeared.

Fast forward to the late 20th century, and concerns about air pollution and oil dependence triggered a renewed interest in EVs. The California Air Resources Board (CARB) played a crucial role by mandating that automakers produce zero-emission vehicles. This led to the development of modern EVs like the General Motors EV1 in 1996.

The real breakthrough came with the introduction of lithium-ion battery technology. Unlike older lead-acid batteries, lithium-ion batteries are lighter, store more energy, and last longer. Tesla Motors, founded in 2003, was the first company to prove that EVs could be desirable, high-performance vehicles. The Tesla Roadster (2008) could accelerate from 0 to 100 km/h in under 4 seconds and had a range of over 300 kilometers.

Today, nearly every major automaker produces electric vehicles. Battery costs have fallen by nearly 90% since 2010, making EVs more affordable than ever. Governments around the world are setting targets to phase out gasoline vehicles, and charging infrastructure is expanding rapidly. While challenges remain — including battery production's environmental impact and the need for more charging stations — the future of transportation is increasingly electric."""

    r1 = Test(type='reading', title='The Evolution of Electric Vehicles', description='Academic reading passage about EV history', difficulty='medium', passage=passage1)
    db.session.add(r1)
    db.session.flush()

    for q_text, opts, answer, order in [
        ("When did the first practical electric vehicle appear?", json.dumps(["1820s","1830s","1880s","1900s"]), "1830s", 1),
        ("What made gasoline cars more convenient after 1912?", json.dumps(["Cheaper fuel","The electric starter","Faster engines","Better roads"]), "The electric starter", 2),
        ("Which organization mandated zero-emission vehicles in California?", json.dumps(["EPA","CARB","NHTSA","DOE"]), "CARB", 3),
        ("What battery technology revolutionized modern EVs?", json.dumps(["Lead-acid","Nickel-cadmium","Lithium-ion","Solid-state"]), "Lithium-ion", 4),
        ("How much have battery costs fallen since 2010?", json.dumps(["50%","70%","90%","99%"]), "90%", 5),
    ]:
        db.session.add(Question(test_id=r1.id, question_text=q_text, options=opts, correct_answer=answer, order=order))

    passage2 = """The migration patterns of Arctic terns have long puzzled ornithologists. These small seabirds travel from pole to pole each year, covering a distance that no other animal on Earth matches. Recent studies using geolocator technology have revealed that the route is not a straight line — instead, the birds use atmospheric pressure systems to conserve energy, adding thousands of kilometers to their journey.

This discovery challenges earlier assumptions that Arctic terns relied solely on celestial navigation. Researchers now believe that these birds have an innate ability to detect and follow favorable wind patterns. The implications are significant: if climate change alters these pressure systems, it could disrupt the migration routes that terns have followed for millennia.

The Arctic tern's migration is truly remarkable. A single bird can travel up to 80,000 kilometers per year — that's roughly twice the circumference of the Earth. During its 30-year lifespan, an Arctic tern may fly over 2.4 million kilometers, equivalent to three round trips to the Moon.

Scientists are particularly interested in how young terns learn these routes. Unlike many migratory birds that follow their parents, young Arctic terns appear to migrate independently. This suggests that the ability to navigate using atmospheric pressure may be instinctive rather than learned."""

    r2 = Test(type='reading', title='Arctic Tern Migration', description='Academic passage about bird migration patterns', difficulty='hard', passage=passage2)
    db.session.add(r2)
    db.session.flush()

    for q_text, opts, answer, order in [
        ("What technology did scientists use to study tern migration?", json.dumps(["Satellite tags","Geolocators","Radar","GPS collars"]), "Geolocators", 1),
        ("How do Arctic terns conserve energy during migration?", json.dumps(["Flying at night","Using pressure systems","Eating more","Flying in groups"]), "Using pressure systems", 2),
        ("What is the max distance an Arctic tern can travel in a year?", json.dumps(["40,000 km","60,000 km","80,000 km","100,000 km"]), "80,000 km", 3),
        ("Young Arctic terns learn migration routes by:", json.dumps(["Following parents","Instinct","Learning from flock","Trial and error"]), "Instinct", 4),
    ]:
        db.session.add(Question(test_id=r2.id, question_text=q_text, options=opts, correct_answer=answer, order=order))

    for t,d,df in [("Education Systems Comparison","Passage comparing education systems","medium"),("Renewable Energy Sources","Passage about solar and wind energy","easy")]:
        db.session.add(Test(type='reading', title=t, description=d, difficulty=df))


def _seed_listening_tests():
    from models import db, Test
    for t,d,df in [("Conversation: University Registration","Listening Part 1","easy"),("Lecture: Marine Biology","Listening Part 4","hard")]:
        db.session.add(Test(type='listening', title=t, description=d, difficulty=df))


def _seed_writing_tests():
    from models import db, Test
    for t,d,df in [
        ("Task 1: Energy Consumption Chart","The chart shows energy consumption by source. Summarize.","medium"),
        ("Task 2: University Education","Should university education be free for all? Discuss.","medium"),
        ("Task 2: Environmental Solutions","What causes pollution? What solutions can you suggest?","hard"),
        ("Task 2: Technology and Communication","How has technology affected communication? Positive or negative?","medium"),
        ("Task 1: Population Growth Graph","The graph shows population growth in major cities from 1950 to 2020.","easy"),
    ]:
        db.session.add(Test(type='writing', title=t, description=d, difficulty=df))


def _seed_speaking_tests():
    from models import db, Test
    for t,d,df in [
        ("Part 1: Work and Studies","Do you work or study? What do you like about it?","easy"),
        ("Part 1: Hobbies","What do you do in your free time?","easy"),
        ("Part 1: Travel","Do you enjoy traveling? Best place visited?","easy"),
        ("Part 2: Describe a Person","Describe someone you admire.","medium"),
        ("Part 2: Describe a Place","Describe a memorable place you visited.","medium"),
        ("Part 3: Technology and Society","How has technology changed interaction? Positive or negative?","hard"),
        ("Part 3: Education and Learning","What makes a good teacher? How has education changed?","hard"),
    ]:
        db.session.add(Test(type='speaking', title=t, description=d, difficulty=df))


if __name__ == '__main__':
    from api.index import app
    with app.app_context():
        seed_data()
