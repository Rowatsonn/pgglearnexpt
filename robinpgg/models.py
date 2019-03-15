from dallinger.nodes import Source
from dallinger.models import Node 

import json

class QuizSource(Source):
    """A Source that reads a question and transmits it. The question is transmitted along with the 
    correct and incorrect answers."""

    __mapper_args__ = {
        "polymorphic_identity": "quiz_source"
    }

    def _contents(self):
        """Define the contents of new Infos .... (New transmissions??)

        transmit() -> _what() -> create_information() -> _contents().
        """
        number_transmissions = len(self.infos())
        import json
        questions = [
            json.dumps({
                'question': 'When did the First World War end?',
                'number' : 1,
                'Wwer1': '1914',
		'Wwer2': '1939',
                'Rwer': '1918',
                }),
            json.dumps({
                'question': 'What is the hottest planet in the solar system?',
                'number': 2,
                'Wwer1': 'Mercury',
		'Wwer2': 'Jupiter',
                'Rwer': 'Venus',
                }),
            json.dumps({
                'question': 'Which actor played Saul Goodman in the show Breaking Bad?',
                'number': 3,
                'Wwer1': 'Aaron Paul',
		'Wwer2': 'Jonathan Banks',
                'Rwer': 'Bob Odenkirk',
                }),
            json.dumps({
                'question': 'Vincent van Gogh died in which year?',
                'number': 4,
                'Wwer1': '1880',
		'Wwer2': '1900',
                'Rwer': '1890',
                }),
            json.dumps({
                'question': 'Which of these countries has the SMALLEST population?',
                'number': 5,
                'Wwer1': 'India',
		'Wwer2': 'United States of America',
                'Rwer': 'Russia',
                }),
            json.dumps({
		'question': 'In which year was the Magna Carta signed?',
                'number': 6,
                'Wwer1': '1066',
		'Wwer2': '1775',
                'Rwer': '1215',
                }),
            json.dumps({
                'question': 'Which of these US presidents was president FIRST?',
                'number': 7,
                'Wwer1': 'Richard Nixon',
		'Wwer2': 'John F. Kennedy',
                'Rwer': 'Franklin D. Roosevelt',
                }),
            json.dumps({
                'question': 'In Which continent is Mt. Everest located?',
                'number': 8,
                'Wwer1': 'Austrailia (Oceania)',
		'Wwer2': 'Europe',
                'Rwer': 'Asia',
                }),
            json.dumps({
		'question': 'Which of these chemical elements is a Halogen?',
                'number' : 9,
                'Wwer1': 'Xenon',
		'Wwer2': 'Phosphorus',
                'Rwer': 'Iodine',
                }),
            json.dumps({
                'question': 'Which of these Shakespeare plays was written FIRST?',
                'number': 10,
                'Wwer1': 'Macbeth',
		'Wwer2': 'Romeo and Juiliet',
                'Rwer': 'The Comedy of Errors',
                }),
             json.dumps({
                'question': 'This is a dummy question, if you see this. It gone broke.',
                'number': 11,
                'Wwer1': 'Woops',
		'Wwer2': 'Oh well',
                'Rwer': 'dallinger debug',
                }),
        ]

        return questions[number_transmissions]

class ProbeNode(Node):
    

    __mapper_args__ = {
        "polymorphic_identity": "probe_node"
    }

    @property
    def score_in_quiz(self):
        import json
        return json.loads(self.property1)["score_in_quiz"]

    @property
    def prestige(self):
        import json
        return json.loads(self.property2)["prestige"]

    @score_in_quiz.setter
    def score_in_quiz(self, val):
        import json
        p1 = json.loads(self.property1)
        p1["score_in_quiz"] = val
        self.property1 = json.dumps(p1)

    @prestige.setter
    def prestige(self,val):
        import json
        p2 = json.loads(self.property2)
        p2["prestige"] = val
        self.property2 = json.dumps(p2)

