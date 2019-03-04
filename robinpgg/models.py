from dallinger.nodes import Source


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
                'Wwer1': '1914',
		'Wwer2': '1939',
                'Rwer': '1918',
                }),
            json.dumps({
                'question': 'What is the hottest planet in the solar system?',
                'Wwer1': 'Mercury',
		'Wwer2': 'Jupiter',
                'Rwer': 'Venus',
                }),
            json.dumps({
                'question': 'Which actor played Saul Goodman in the show Breaking Bad?',
                'Wwer1': 'Aaron Paul',
		'Wwer2': 'Jonathan Banks',
                'Rwer': 'Bob Odenkirk',
                }),
            json.dumps({
                'question': 'Vincent van Gogh died in which year?',
                'Wwer1': '1880',
		'Wwer2': '1900',
                'Rwer': '1890',
                }),
            json.dumps({
                'question': 'Which of these countries has the SMALLEST population?',
                'Wwer1': 'India',
		'Wwer2': 'United States of America',
                'Rwer': 'Russia',
                }),
            json.dumps({
		'question': 'In which year was the Magna Carta signed?',
                'Wwer1': '1066',
		'Wwer2': '1775',
                'Rwer': '1215',
                }),
            json.dumps({
                'question': 'Which of these US presidents was president FIRST?',
                'Wwer1': 'Richard Nixon',
		'Wwer2': 'John F. Kennedy',
                'Rwer': 'Franklin D. Roosevelt',
                }),
            json.dumps({
                'question': 'In Which continent is Mt. Everest located?',
                'Wwer1': 'Austrailia (Oceania)',
		'Wwer2': 'Europe',
                'Rwer': 'Asia',
                }),
            json.dumps({
		'question': 'Which of these chemical elements is a Halogen?',
                'Wwer1': 'Xenon',
		'Wwer2': 'Phosphorus',
                'Rwer': 'Iodine',
                }),
            json.dumps({
                'question': 'Which of these Shakespeare plays was written FIRST?',
                'Wwer1': 'Macbeth',
		'Wwer2': 'Romeo and Juiliet',
                'Rwer': 'The Comedy of Errors',
                }),
        ]
        number_transmissions = len(self.infos()) 

        return questions[number_transmissions]

