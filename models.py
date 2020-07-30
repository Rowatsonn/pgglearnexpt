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
                'question': 'A person from a small nation who speaks the same language as a person from a larger nation will…',
                'number' : 1,
                'Wwer1': 'Feel intimidated by the person from the larger nation',
                'Wwer2': 'Admire the person from the larger nation',
                'Rwer': 'Show prejudice to the larger nation',
            }),
            json.dumps({
                'question': 'What might happen in a classroom if the teacher divides the students into a “Blue Team” and a “Red Team”?',
                'number': 2,
                'Wwer1': 'The students will act as they always do',
                'Wwer2': 'The students will get to know others who they did not originally hang out with very much',
                'Rwer': 'The students will stop talking to members of the opposite team and make friends with their own team',
            }),
            json.dumps({
                'question': 'Being part of a group...',
                'number': 3,
                'Wwer1': 'Increases the acceptance of other people within that group',
                'Wwer2': 'Increases empathy towards other groups',
                'Rwer': 'Decreases trust in people from other groups',
            }),
            json.dumps({
                'question': 'A group of people have guessed the number of sweets in a jar out loud. Joe thinks they are wrong. What does he do?',
                'number': 4,
                'Wwer1': 'Disagree with them and give them the correct answer',
                'Wwer2': 'Privately tell the person in charge that he disagrees',
                'Rwer': 'Agree with the people who have guessed before him, even though he thinks they were wrong',
            }),
            json.dumps({
                'question': 'What type of person is more likely to be elected for a leadership position?',
                'number': 5,
                'Wwer1': 'A person who stands out as being different',
                'Wwer2': 'A person with the relevant experience and qualifications',
                'Rwer': 'A person with a high level of charisma',
            }),
            json.dumps({
                'question': 'In a group discussion how will a final decision be made?',
                'number': 6,
                'Wwer1': 'Generally, the group will be unable to come to a final decision',
                'Wwer2': 'Generally, the group will go with the first opinion given by someone',
                'Rwer': 'Generally, the group will go with the majority’s decision',
            }),
            json.dumps({
                'question': 'What are new members of an established group expected to do?',
                'number': 7,
                'Wwer1': 'Share their own attitudes and values with the group',
                'Wwer2': 'Recruit new members to the group',
                'Rwer': 'Take on the attitudes and values of the group',
            }),
            json.dumps({
                'question': 'When people encounter someone from a different group, what is their first impression most often based on?',
                'number': 8,
                'Wwer1': 'The way they look and talk',
                'Wwer2': 'The group member’s personality',
                'Rwer': 'What they know about the group the person comes from',
            }),
            json.dumps({
                'question': 'When working on a group task…',
                'number' : 9,
                'Wwer1': 'People will put in the same amount of effort as when working on their own',
                'Wwer2': 'People will work harder than when working on their own',
                'Rwer': 'People will work less hard than when working on their own',
            }),
            json.dumps({
                'question': 'If someone has a different opinion to the group, how can they change the rest of the group’s opinion?',
                'number': 10,
                'Wwer1': 'Allow other members of the group to believe that the ultimate decision is still up to them',
                'Wwer2': 'Use detailed arguments',
                'Rwer': 'Show a certain amount of flexibility',
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



