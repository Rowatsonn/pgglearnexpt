from dallinger.nodes import Source
from dallinger.models import Node, Info
from dallinger.networks import Burst

import sys
import json

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


class PogBot(Node):
    """The pot of greed, which will handle working out the scores for each of the participants."""
    
    __mapper_args__ = {
        "polymorphic_identity": "pot_of_greed_bot"
    }
    
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


    def update(self, infos):
        """This will handle working out the scores. Infos end up here whenever .receieve()
        is called in the backend"""
        decisions = [] # Empty list ready for decisions
        probes = self.network.size(type=ProbeNode) # Number of ProbeNodes
        nodes = self.network.nodes(type=ProbeNode) # Object containing the probes
        pog = self.network.nodes(type=PogBot)[0] # Get the Pog
        snowdrift = self.snowdrift #Determines what maths need to happen to the pot
        sum = 0 # Object for PGG contributions
        for info in infos: # Get the contents of the infos and set to integer
            info = int(info.contents)
            decisions.append(info)
        for num in decisions: # Add up these numbers
                sum += num

        mean = sum / probes # This is currently the conformist learning. Maybe will change this. 
        for node in nodes: # Give the conformity information to all the nodes
            clist = node.conform_list
            clist.extend([mean])
            node.conform_list = clist

        if snowdrift == 0: # Game is a prisoner's dilemma
            winning_score = 0 # Necessary for the payoff learning
            sum = sum*2 # Double the result
            earnings = sum/probes # Divide by the number of probes (pps) in the network
            self.pot = earnings
            for node in nodes:
                node.score_in_pgg += earnings
                round_scores = node.round_earnings # Update the round_earnings list in property 3
                leftovers = int(node.leftovers)
                this_round = leftovers + earnings
                round_scores.extend([this_round])
                node.round_earnings = round_scores
                node_score = node.score_in_pgg
                if node_score > winning_score:
                    winning_score = node_score

            for node in nodes:
                node_score = node.score_in_pgg # Is the node the winning node. If it is, get their payoff list and their donation. Extend the list
                if node_score == winning_score: 
                    paylist = node.payoff_list
                    donation = node.donation
                    paylist.extend([donation])
                    for node in nodes: # Then update it on every node
                        node.payoff_list = paylist

            self.round += 1 # Up the round counter by one. This is a necessary cue for the front end
        
        elif snowdrift == 1: # The game is a snowdrift
            if sum < 10: # The threshold has not been met
                winning_score = 0
                self.pot = 0  
                for node in nodes: # This is necessary because the nodes increase their own score during info_post_request
                    round_scores = node.round_earnings
                    this_round = 0 # Set the round earnings in property 3 to 0, because the snowdrift was failed
                    round_scores.extend([this_round])
                    node.round_earnings = round_scores
                    leftovers = int(node.leftovers)
                    current_score = int(node.score_in_pgg)
                    new_score = current_score - leftovers
                    if new_score > winning_score:
                        winning_score = new_score
                    node.score_in_pgg = new_score 
                    node.leftovers = 0
                for node in nodes:
                    node_score = node.score_in_pgg
                    if node_score == winning_score: # Is the node the winning node. If it is, get their payoff list and their donation. Extend the list
                        paylist = node.payoff_list
                        donation = node.donation
                        paylist.extend([donation])
                        for node in nodes: # Then update it on every node
                            node.payoff_list = paylist

                self.round += 1
            else: # The threshold HAS been met
                winning_score = 0
                sum = sum*2
                earnings = sum/probes
                self.pot = earnings
                for node in nodes:
                    node.score_in_pgg += earnings
                    round_scores = node.round_earnings # Update the round_earnings list in property 3
                    leftovers = int(node.leftovers)
                    this_round = leftovers + earnings
                    round_scores.extend([this_round])
                    node.round_earnings = round_scores
                    node_score = node.score_in_pgg
                    if node_score > winning_score:
                        winning_score = node_score

                for node in nodes:
                    node_score = node.score_in_pgg
                    if node_score == winning_score: # Is the node the winning node. If it is, get their payoff list and their donation. Extend the list
                        paylist = node.payoff_list
                        donation = int(node.donation)
                        paylist.extend([donation])
                        for node in nodes: # Then update it on every node
                            node.payoff_list = paylist
                self.round += 1

class RNetwork(Burst):
    """A custom form of the burst network to be used in the public goods game"""

    __mapper_args__ = {
        "polymorphic_identity": "Robin_Network"
    }

    def rearrange_network(self):
        """This function will convert the current, regular, burst network into this"""
        source = self.nodes(type=QuizSource)
        for s in source:
            s.fail()

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



