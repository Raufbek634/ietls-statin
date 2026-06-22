import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.index import app
from models import db, Test, Vocabulary, Question

with app.app_context():
    db.create_all()

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

    if not Test.query.filter_by(type='reading').first():
        passage1 = """The history of the electric vehicle (EV) is far longer than most people realize. While many assume that EVs are a recent phenomenon driven by modern environmental concerns, the first electric vehicles actually appeared in the early 19th century.

In the 1830s, inventors in Hungary, the Netherlands, and the United States began experimenting with battery-powered vehicles. The first practical EV was built by Thomas Davenport in the United States in 1834, but it was limited to running on a short circular track. By the late 1800s, electric cars had become quite popular in urban areas because they were quiet, easy to drive, and did not emit the unpleasant fumes associated with gasoline-powered cars.

However, the popularity of EVs was short-lived. The discovery of large petroleum reserves in Texas and the Middle East made gasoline cheap and abundant. At the same time, Charles Kettering invented the electric starter in 1912, which eliminated the need for hand-cranking a gasoline engine. This made gasoline cars much more convenient. By the 1930s, electric vehicles had all but disappeared.

Fast forward to the late 20th century, and concerns about air pollution and oil dependence triggered a renewed interest in EVs. The California Air Resources Board (CARB) played a crucial role by mandating that automakers produce zero-emission vehicles. This led to the development of modern EVs like the General Motors EV1 in 1996.

The real breakthrough came with the introduction of lithium-ion battery technology. Unlike older lead-acid batteries, lithium-ion batteries are lighter, store more energy, and last longer. Tesla Motors, founded in 2003, was the first company to prove that EVs could be desirable, high-performance vehicles. The Tesla Roadster (2008) could accelerate from 0 to 100 km/h in under 4 seconds and had a range of over 300 kilometers.

Today, nearly every major automaker produces electric vehicles. Battery costs have fallen by nearly 90% since 2010, making EVs more affordable than ever. Governments around the world are setting targets to phase out gasoline vehicles, and charging infrastructure is expanding rapidly. While challenges remain — including battery production's environmental impact and the need for more charging stations — the future of transportation is increasingly electric."""

        r1 = Test(type='reading', title='The Evolution of Electric Vehicles', description='Academic reading passage about EV history', difficulty='medium', passage=passage1)
        db.session.add(r1)
        db.session.flush()

        questions1 = [
            ("When did the first practical electric vehicle appear?", json.dumps(["1820s","1830s","1880s","1900s"]), "1830s", 1),
            ("What made gasoline cars more convenient after 1912?", json.dumps(["Cheaper fuel","The electric starter","Faster engines","Better roads"]), "The electric starter", 2),
            ("Which organization mandated zero-emission vehicles in California?", json.dumps(["EPA","CARB","NHTSA","DOE"]), "CARB", 3),
            ("What battery technology revolutionized modern EVs?", json.dumps(["Lead-acid","Nickel-cadmium","Lithium-ion","Solid-state"]), "Lithium-ion", 4),
            ("How much have battery costs fallen since 2010?", json.dumps(["50%","70%","90%","99%"]), "90%", 5),
            ("What was the Tesla Roadster's approximate range?", json.dumps(["200 km","300 km","400 km","500 km"]), "300 km", 6),
            ("True or False: Electric vehicles first appeared in the 1990s.", json.dumps(["True","False"]), "False", 7),
            ("According to the passage, what challenge for EVs is mentioned?", json.dumps(["High speed","Battery production impact","Lack of colors","Noise"]), "Battery production impact", 8),
        ]
        for q_text, opts, answer, order in questions1:
            db.session.add(Question(test_id=r1.id, question_text=q_text, options=opts, correct_answer=answer, order=order))

        passage2 = """The migration patterns of Arctic terns have long puzzled ornithologists. These small seabirds travel from pole to pole each year, covering a distance that no other animal on Earth matches. Recent studies using geolocator technology have revealed that the route is not a straight line — instead, the birds use atmospheric pressure systems to conserve energy, adding thousands of kilometers to their journey.

This discovery challenges earlier assumptions that Arctic terns relied solely on celestial navigation. Researchers now believe that these birds have an innate ability to detect and follow favorable wind patterns. The implications are significant: if climate change alters these pressure systems, it could disrupt the migration routes that terns have followed for millennia.

The Arctic tern's migration is truly remarkable. A single bird can travel up to 80,000 kilometers per year — that's roughly twice the circumference of the Earth. During its 30-year lifespan, an Arctic tern may fly over 2.4 million kilometers, equivalent to three round trips to the Moon.

Scientists are particularly interested in how young terns learn these routes. Unlike many migratory birds that follow their parents, young Arctic terns appear to migrate independently. This suggests that the ability to navigate using atmospheric pressure may be instinctive rather than learned.

Conservation efforts are now focusing on protecting key stopover sites along the tern's migration route. These sites, located in the North Atlantic and along the coasts of West Africa, provide essential feeding grounds where terns rest and refuel before continuing their epic journey."""

        r2 = Test(type='reading', title='Arctic Tern Migration', description='Academic passage about bird migration patterns', difficulty='hard', passage=passage2)
        db.session.add(r2)
        db.session.flush()

        questions2 = [
            ("What technology did scientists use to study tern migration?", json.dumps(["Satellite tags","Geolocators","Radar","GPS collars"]), "Geolocators", 1),
            ("How do Arctic terns conserve energy during migration?", json.dumps(["Flying at night","Using pressure systems","Eating more","Flying in groups"]), "Using pressure systems", 2),
            ("What is the maximum distance an Arctic tern can travel in a year?", json.dumps(["40,000 km","60,000 km","80,000 km","100,000 km"]), "80,000 km", 3),
            ("Young Arctic terns learn migration routes by:", json.dumps(["Following parents","Instinct","Learning from flock","Trial and error"]), "Instinct", 4),
            ("Climate change could affect terns by:", json.dumps(["Making them larger","Disrupting pressure systems","Changing feather color","Reducing speed"]), "Disrupting pressure systems", 5),
        ]
        for q_text, opts, answer, order in questions2:
            db.session.add(Question(test_id=r2.id, question_text=q_text, options=opts, correct_answer=answer, order=order))

        db.session.add(Test(type='reading', title='Education Systems Comparison', description='Academic passage comparing education systems', difficulty='medium'))
        db.session.add(Test(type='reading', title='Renewable Energy Sources', description='Academic passage about solar and wind energy', difficulty='easy'))
        db.session.commit()
        print("Reading tests seeded")

    if not Test.query.filter_by(type='listening').first():
        db.session.add(Test(type='listening', title='Conversation: University Registration', description='Listening Part 1 conversation', difficulty='easy'))
        db.session.add(Test(type='listening', title='Lecture: Marine Biology', description='Listening Part 4 academic lecture', difficulty='hard'))
        db.session.commit()
        print("Listening tests seeded")

    if not Test.query.filter_by(type='writing').first():
        for t,d,df in [
            ("Task 1: Energy Consumption Chart","The chart below shows energy consumption by source in the US. Summarize the information.","medium"),
            ("Task 2: University Education","Some people believe university education should be free for all. To what extent do you agree or disagree?","medium"),
            ("Task 2: Environmental Solutions","What are the main causes of environmental pollution? What solutions can you suggest?","hard"),
            ("Task 2: Technology and Communication","How has technology affected the way people communicate with each other? Is this a positive or negative development?","medium"),
            ("Task 1: Population Growth Graph","The graph shows population growth in major cities from 1950 to 2020. Write a report.","easy"),
        ]:
            db.session.add(Test(type='writing', title=t, description=d, difficulty=df))
        db.session.commit()
        print("Writing tests seeded")

    if not Test.query.filter_by(type='speaking').first():
        for t,d,df in [
            ("Part 1: Work and Studies","Do you work or are you a student? What do you like about your job/studies?","easy"),
            ("Part 1: Hobbies and Free Time","What do you do in your free time? Do you prefer spending time alone or with others?","easy"),
            ("Part 1: Travel","Do you enjoy traveling? What is the best place you have ever visited?","easy"),
            ("Part 2: Describe a Person","Describe someone you admire. You should say: who this person is, how you know them, what qualities they have, and explain why you admire them.","medium"),
            ("Part 2: Describe a Place","Describe a place you have visited that left a strong impression on you. Say where it was, when you went, what you did there, and why it was memorable.","medium"),
            ("Part 3: Technology and Society","How has technology changed the way people interact? Do you think this is mostly positive or negative? What will communication look like in 50 years?","hard"),
            ("Part 3: Education and Learning","What makes a good teacher? How has education changed in your country? What role will technology play in education?","hard"),
        ]:
            db.session.add(Test(type='speaking', title=t, description=d, difficulty=df))
        db.session.commit()
        print("Speaking tests seeded")

    print("All seed data added!")
