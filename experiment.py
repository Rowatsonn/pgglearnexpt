"""My Social learning and cooperation experiment"""
from dallinger.config import get_config
from dallinger.experiments import Experiment
from dallinger.networks import Burst
from dallinger.nodes import Source, Node
from dallinger.nodes import Node

from . import models
from datetime import datetime
from operator import attrgetter
import json

config = get_config()

class pgglearn(Experiment):
    """Define the structure of the experiment."""
    def __init__(self, session=None):
        """Call the same parent constructor, then call setup() if we have a session.
        """
        super(pgglearn, self).__init__(session)
        from . import models 
        self.models = models
        self.experiment_repeats = 1 # Change this to the number of runs you want. 
        self.initial_recruitment_size = 4 # Change this to = the number of probe nodes across ALL networks. Although over recruiting is wise
        self.known_classes = {
            "PogBot": models.PogBot,
            "QuizSource": models.QuizSource,
        }
        if session:
            self.setup()
            
    def setup(self):
        if not self.networks():
            super(pgglearn, self).setup()
            for net in self.networks():
                self.models.QuizSource(network=net)
                self.models.PogBot(network=net)

    def get_network_for_participant(self, participant):
        if participant.nodes(failed="all"):
            return None

        networks = self.networks(full=False)
        if networks:
            return min(networks, key=attrgetter("id"))
        else:
            return None

    def create_network(self):
        """Return a new network."""
        return self.models.RNetwork(max_size=6) # Change this to change the sample size. N + 2. N + 2 because the network already has PoG and quiz source
        
    def create_node(self, participant, network):
        """Create a node for the participant. Hopefully a ProbeNode"""
        node = self.models.ProbeNode(network=network, participant=participant)
        node.property1 = json.dumps({
            'score_in_quiz': 0,
            'last_request' : str(datetime.now()),
        })
        node.property2 = json.dumps({
            'prestige' : 0
        })
        node.property3 = json.dumps({
            'score_in_pgg' : 0,
            'round_earnings' : []
        })
        node.property4 = json.dumps({
            'leftovers' : 0,
            'donation' : 0,
            'info_choice' : "BB" # To manually set the social learning, change this. To either conformity / prestige / payoff / regular (a regular public goods game with a table of donations) / full (regular, plus the prestigious and winning node are labelled / extra (all the information of full + their overall scores) BB (Black box, although do type BB). See below to change to / from a snowdrift.
        })
        node.property5 = json.dumps({
            'prestige_list' : [],
            'conform_list' : [],
            'payoff_list' : []
        })
        return node

    def bonus(self, participant):
        """Calculate a participants bonus."""
        node = participant.nodes()[0]
        score = node.score_in_pgg
        bonus = round(score * 0.017, 2) # This can be changed to what you like, but right now every point in the game is worth 0.017 cents
        bonus = min(bonus,3.00)
        return bonus
        
    def node_post_request(self, participant, node):
        node.network.property1 = json.dumps({ 'num_probes': len(node.network.nodes(type=self.models.ProbeNode)) }) # Set for the benefit of Javascript in the check_network
        if node.network.full:
            node.network.nodes(type=Source)[0].transmit() 

    def transmission_get_request(self, node, transmissions):
        """All this does is update the last_request property for use in the AFK functions"""
        node.last_request = datetime.now()
        self.stiller_remover(node)
         # fix for hanging issue.
        received_transmissions = node.transmissions(direction="incoming", status="received")
        if not transmissions:
            if received_transmissions:
                most_recent_transmission = max(received_transmissions, key=attrgetter("id"))
                responses = node.infos(failed="all")
                transmission_newer_than_response = False
                if responses:
                    most_recent_response = max(responses, key=attrgetter("id"))
                    if most_recent_transmission.receive_time > most_recent_response.creation_time:
                        transmission_newer_than_response = True
                if transmission_newer_than_response or not responses:
                    if not node.transmissions(direction="incoming", status="pending"):
                        most_recent_transmission.origin.transmit(what=most_recent_transmission.info, to_whom=node)

    def node_get_request(self, node, nodes):
        """Runs when neighbors is requested and also updates last request for use in AFK"""
        node.last_request = datetime.now()
        self.stiller_remover(node)

    def info_get_request(self, node, infos):
        """Runs on the instructions page automatically and also when the popup comes up"""
        node.last_request = datetime.now()
    
    def info_post_request(self, node, info):
        """This will handle the source transmitting, calculating
        the score in the quiz and assigning prestige to the winner.
        Then finally for the PGG, it will transmit choices to the POG
        """
        node.last_request = datetime.now()
        my_infos = node.infos()
        n_infos = len(my_infos)
        
        if n_infos <= 11:
            self.advance_quiz(node, my_infos, info)
        else:
            self.advance_pgg(node, info)    

    def advance_quiz(self, node, my_infos, info):
        n_infos = len(my_infos)
        nodes = node.network.nodes(type=self.models.ProbeNode)

        if n_infos == 10: # if you've finished calculate your score
            self.score_node(node, my_infos)

        if self.everyone_ready(nodes): # if everyone has answered the same question
            if info == max(node.network.infos(), key=attrgetter("id")): # if you're the most recent to answer
                if n_infos <= 10:
                    if n_infos == 10:
                        winner = max(nodes, key=attrgetter("score_in_quiz"))
                        winner.prestige = 1
                    node.network.nodes(type=Source)[0].transmit()
                else: # so n_infos must be 11
                    node.network.rearrange_network()

    def score_node(self, node, infos):
        correct_answers = ["Show prejudice to the larger nation","The students will stop talking to members of the opposite team and make friends with their own team","Decreases trust in people from other groups","Agree with the people who have guessed before him, even though he thinks they were wrong","A person with a high level of charisma","Generally, the group will go with the majority’s decision","Take on the attitudes and values of the group","What they know about the group the person comes from","People will work less hard than when working on their own","Show a certain amount of flexibility"]
        answers = [i.contents for i in infos]
        node.score_in_quiz = len([a for a in answers if a in correct_answers])

    def everyone_ready(self, nodes):
        num_answers = [len(node.infos()) for node in nodes]
        return all([x == num_answers[0] for x in num_answers])

    def advance_pgg(self, node, info):
        
        # Define the pog
        pog = node.network.nodes(type=self.models.PogBot)[0]

	# Check that the donation is between 0 and 10. If it isn't (implying some javascript tomfoolery) correct it. 
        donation = int(info.contents)
        if donation < 0 or donation > 10:
            if donation < 0:
                donation = 0
            elif donation > 10:
                donation = 10
            info.fail()
            info = self.models.Info(origin = node, contents = donation) # Make a new info to send to the POG

        # send their choice to the pog
        transmission = node.transmit(what=info, to_whom=self.models.PogBot)[0]
        self.save()

        # update their score
        node.donation = donation 
        node.leftovers = 10 - donation
        node.score_in_pgg += node.leftovers

        # inform everyone else
        nodes = node.network.nodes(type=self.models.ProbeNode)
        if node.prestige == 1:
            for n in nodes:
                n.prestige_list = n.prestige_list + [donation]

        # tell pog to process transmissions
        pending_transmissions = node.network.transmissions(status='pending')
        if len(pending_transmissions) == len(nodes):
            if transmission == max(pending_transmissions, key=attrgetter("id")):
                pog.receive()


    # Function to manage the removal of stillers
    def stiller_remover(self, node):
        nodes = node.network.nodes(type=self.models.ProbeNode)
        bad_nodes = [n for n in nodes if (node.last_request - n.last_request).total_seconds() > 60]
        good_nodes = [n for n in nodes if n not in bad_nodes]
        if bad_nodes and node.id == max(good_nodes, key=attrgetter("id")).id:
            for n in bad_nodes:
                n.fail()

            self.readvance_network(node)

    # Readvances the network when somebody either drops out or abandones on Mturk. Calls automatically in the Mturk case and in stiller remover otherwise. 
    def readvance_network(self, node):
        if node.network.infos():
            if node.network.nodes(type=Source):
                most_recent_info = max(node.network.infos(), key=attrgetter("id"))
                self.info_post_request(most_recent_info.origin, most_recent_info)
            else:
                try:
                    most_recent_transmission = max(node.transmissions(), key=attrgetter("id"))
                    most_recent_transmission.fail()
                    self.info_post_request(most_recent_transmission.origin, most_recent_transmission.info)
                except ValueError: # There are no transmissions, because they have gone AFK in the scorescreen. In which case, just removing the nodes is fine as the game is advanced by the participants
                    pass
                

    def assignment_abandoned(self, participant):
        #networks = [n.network for n in participant.nodes()]
        self.fail_participant(participant)
        for n in participant.nodes(failed="all"):
            self.readvance_network(n)

    def assignment_returned(self, participant):
        #networks = [n.network for n in participant.nodes()]
        self.fail_participant(participant)
        for n in participant.nodes(failed="all"):
            self.readvance_network(n)
