from dallinger.nodes import Source
from dallinger.models import Node, Info
from dallinger.networks import Burst

import sys
import json
from operator import attrgetter

from datetime import datetime

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
        questions = [
            json.dumps({
                'question': 'What is the hottest planet in the solar system?',
                'number' : 1,
                'Wwer1': 'Mercury',
                'Wwer2': 'Jupiter',
                'Rwer': 'Venus',
            }),
            json.dumps({
                'question': 'Rearrange the anagram "KENOMY" and select the category to which it fits',
                'number': 2,
                'Wwer1': 'Place',
                'Wwer2': 'Food',
                'Rwer': 'Animal',
            }),
            json.dumps({
                'question': 'What is the next number in this sequence: 1,4,9,16,25,36...',
                'number': 3,
                'Wwer1': '42',
                'Wwer2': '45',
                'Rwer': '49',
            }),
            json.dumps({
                'question': 'Which of these chemical elements is a Halogen?',
                'number': 4,
                'Wwer1': 'Xenon',
                'Wwer2': 'Uranium',
                'Rwer': 'Iodine',
            }),
            json.dumps({
                'question': 'Which of these countries has the SMALLEST population?',
                'number': 5,
                'Wwer1': 'India',
                'Wwer2': 'United States of America',
                'Rwer': 'Russia',
            }),
            json.dumps({
                'question': 'If Tanya is older than Eric and Cliff is older than Tanya. Then is Eric older or younger than Chris?',
                'number': 6,
                'Wwer1': 'Older',
                'Wwer2': 'Not enough information',
                'Rwer': 'Younger',
            }),
            json.dumps({
                'question': 'A bat and a ball cost $1.10 in total. The bat cost $1.00 more than the ball. How much did the ball cost?',
                'number': 7,
                'Wwer1': '$0.01',
                'Wwer2': '$0.10',
                'Rwer': '$0.05',
            }),
            json.dumps({
                'question': 'In which continent is Mt. Everest located?',
                'number': 8,
                'Wwer1': 'Austrailia (Oceania)',
                'Wwer2': 'Europe',
                'Rwer': 'Asia',
            }),
            json.dumps({
                'question': 'I am facing West. If I turn 90 degrees right, 180 degrees left then 90 degrees right. Which direction am I facing?',
                'number' : 9,
                'Wwer1': 'West',
                'Wwer2': 'North',
                'Rwer': 'East',
            }),
            json.dumps({
                'question': 'Which of these Shakespeare plays was written FIRST?',
                'number': 10,
                'Wwer1': 'Macbeth',
                'Wwer2': 'Romeo and Juiliet',
                'Rwer': 'The Comedy of Errors',
            }),
             json.dumps({
                'question': 'This is a dummy question',
                'number': 11,
                'Wwer1': 'Quiz Finished',
                'Wwer2': 'Quiz Finished',
                'Rwer': 'Quiz Finished',
            }),
        ]

        return questions[number_transmissions]

class ProbeNode(Node):
    """A custom node for use in the experiment. Has some properties changed"""
    

    __mapper_args__ = {
        "polymorphic_identity": "probe_node"
    }

    @property
    def score_in_quiz(self):
        return json.loads(self.property1)["score_in_quiz"]

    @property
    def last_request(self):
        from datetime import datetime
        return datetime.strptime(json.loads(self.property1)["last_request"], "%Y-%m-%d %H:%M:%S.%f")

    @property
    def prestige(self):
        return json.loads(self.property2)["prestige"]

    @property
    def score_in_pgg(self):
        return json.loads(self.property3)["score_in_pgg"]

    @property
    def round_earnings(self):
        return json.loads(self.property3)["round_earnings"]

    @property
    def leftovers(self):
        return json.loads(self.property4)["leftovers"]
    
    @property
    def donation(self):
        return json.loads(self.property4)["donation"]

    @property
    def prestige_list(self):
        return json.loads(self.property5)["prestige_list"]

    @property
    def payoff_list(self):
        return json.loads(self.property5)["payoff_list"]

    @property
    def conform_list(self):
        return json.loads(self.property5)["conform_list"]

    @property
    def info_choice(self):
        return json.loads(self.property4)["info_choice"]

    @score_in_quiz.setter
    def score_in_quiz(self, val):
        p1 = json.loads(self.property1)
        p1["score_in_quiz"] = val
        self.property1 = json.dumps(p1)

    @last_request.setter
    def last_request(self, val):
        p1 = json.loads(self.property1)
        p1["last_request"] = str(val)
        self.property1 = json.dumps(p1)

    @prestige.setter
    def prestige(self, val):
        p2 = json.loads(self.property2)
        p2["prestige"] = val
        self.property2 = json.dumps(p2)

    @score_in_pgg.setter
    def score_in_pgg(self, val):
        p3 = json.loads(self.property3)
        p3["score_in_pgg"] = val
        self.property3 = json.dumps(p3)

    @round_earnings.setter
    def round_earnings(self, val):
        p3 = json.loads(self.property3)
        p3["round_earnings"] = val
        self.property3 = json.dumps(p3)

    @leftovers.setter
    def leftovers(self, val):
        p4 = json.loads(self.property4)
        p4["leftovers"] = val
        self.property4 = json.dumps(p4)

    @donation.setter
    def donation(self, val):
        p4 = json.loads(self.property4)
        p4["donation"] = val
        self.property4 = json.dumps(p4)

    @info_choice.setter
    def info_choice(self, val):
        p4 = json.loads(self.property4)
        p4["info_choice"] = val
        self.property4 = json.dumps(p4)

    @prestige_list.setter
    def prestige_list(self, val):
        p5 = json.loads(self.property5)
        p5["prestige_list"] = val
        self.property5 = json.dumps(p5)

    @payoff_list.setter
    def payoff_list(self, val):
        p5 = json.loads(self.property5)
        p5["payoff_list"] = val
        self.property5 = json.dumps(p5)

    @conform_list.setter
    def conform_list(self, val):
        p5 = json.loads(self.property5)
        p5["conform_list"] = val
        self.property5 = json.dumps(p5)

    def fail(self):

        # don't allow multiple failings
        if self.failed is True:
            raise AttributeError(
                "Cannot fail {} - it has already failed.".format(self))
        else:

            # if the group has started, shrink the network.
            if self.network.infos():
                self.network.max_size -= 1

            # fail the node
            self.failed = True
            self.time_of_death = datetime.now()
            self.network.calculate_full()

            for v in self.vectors():
                v.fail()
            for i in self.infos():
                i.fail()
            for t in self.transmissions(direction="all"):
                t.fail()
            for t in self.transformations():
                t.fail()


class PogBot(Node):
    """The pot of greed, which will handle working out the scores for each of the participants."""
    
    __mapper_args__ = {
        "polymorphic_identity": "pot_of_greed_bot"
    }
    
    def __init__(self, network):
        super().__init__(network)
        self.property1 = json.dumps({ 'pot': 0 })
        self.property2 = json.dumps({ 'round': 0 })
        # Set for whether the game is a snowdrift or not.
        self.property3 = json.dumps({ 'snowdrift': 0 })


    @property
    def pot(self):
        return json.loads(self.property1)["pot"]

    @property
    def round(self):
        return json.loads(self.property2)["round"]
    
    @property
    def snowdrift(self):
        return json.loads(self.property3)["snowdrift"]

    @pot.setter
    def pot(self, val):
        p1 = json.loads(self.property1)
        p1["pot"] = val
        self.property1 = json.dumps(p1)

    @round.setter
    def round(self, val):
        p2 = json.loads(self.property2)
        p2["round"] = val
        self.property2 = json.dumps(p2)
 
    @snowdrift.setter
    def snowdrift(self, val):
        p3 = json.loads(self.property3)
        p3["snowdrift"] = val
        self.property3 = json.dumps(p3)


    def process_pd(self, nodes, total):
        self.pot = total*2/len(nodes)
        for node in nodes:
            node.score_in_pgg += self.pot
            node.round_earnings.append(node.leftovers + self.pot)

    def process_failed_snowdrift(self, nodes):
        self.pot = 0  
        for node in nodes:
            node.round_earnings = node.round_earnings + [0]
            node.score_in_pgg -= node.leftovers
            node.leftovers = 0

    def update(self, infos):
        """This will handle working out the scores. Infos end up here whenever .receieve()
        is called in the backend"""
        nodes = self.network.nodes(type=ProbeNode)
        snowdrift = self.snowdrift == 1

        total = sum([int(i.contents) for i in infos])
        mean = total/len(nodes)
        for node in nodes:
            node.conform_list = node.conform_list + [mean]

        if not snowdrift or total >= 10:
            self.process_pd(nodes, total)
        else:
            self.process_failed_snowdrift(nodes)     

        winner = max(nodes, key=attrgetter("score_in_pgg"))
        for node in nodes:
            node.payoff_list = node.payoff_list + [winner.donation]
        
        self.round += 1

class RNetwork(Burst):
    """A custom form of the burst network to be used in the public goods game"""

    __mapper_args__ = {
        "polymorphic_identity": "Robin_Network"
    }

    @property
    def num_probes(self):
        return json.loads(self.property1)["num_probes"]

    @num_probes.setter
    def num_probes(self, val):
        p1 = json.loads(self.property1)
        p1["num_probes"] = val
        self.property1 = json.dumps(p1)
 
    def rearrange_network(self):
        """This function will convert the current, regular, burst network into this"""
        source = self.nodes(type=QuizSource)
        for s in source:
            s.fail()
            s.network.max_size -= 1 # Shrink the network to avoid someone turning up at the end and breaking the study.
            s.network.calculate_full() # This will update the network to say whether it is full 

        nodes = self.nodes() # This wil connect all the nodes up, except to themselves.
        for n in nodes:
            for n2 in nodes:
                if n != n2:
                    n.connect(n2)

class Info(Info):
    """Standard Info class which includes a human property to tell if it was randomly chosen"""

    @property
    def human(self):
        return json.loads(self.property1)["human"]

    @human.setter
    def human(self, val):
        p3 = json.loads(self.property1)
        p3["human"] = val
        self.property3 = json.dumps(p3)



