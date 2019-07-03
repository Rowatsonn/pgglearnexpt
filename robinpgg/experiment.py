"""My Social learning and cooperation experiment"""
from dallinger.config import get_config
from dallinger.experiments import Experiment
from dallinger.networks import Burst
from dallinger.nodes import Source, Node
from dallinger.nodes import Node

from . import models
from datetime import datetime

import operator
import json

config = get_config()

def all_same(items):
    return all(x == items[0] for x in items)

class pgglearn(Experiment):
    """Define the structure of the experiment."""
    def __init__(self, session=None):
        """Call the same parent constructor, then call setup() if we have a session.
        """
        super(pgglearn, self).__init__(session)
        from . import models 
        self.models = models
        self.experiment_repeats = 1 # Change this to the number of runs you want. 
        self.initial_recruitment_size = 1 # Change this to = the number of probe nodes
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
                pog = self.models.PogBot(network=net)
                pog.property1 = json.dumps({ 'pot': 0 })
                pog.property2 = json.dumps({ 'round': 0 })
                # Set for whether the game is a snowdrift or not.
                pog.property3 = json.dumps({ 'snowdrift': 0 })

    def create_network(self):
        """Return a new network."""
        return self.models.RNetwork(max_size=3) #Change this to change the sample size. N + 2
        
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
            'info_choice' : "extra" # To manually set the social learning, change this. To either conformity / prestige / payoff / regular (a regular public goods game with a table of donations) / full (regular, plus the prestigious and winning node are labelled / extra (all the information of full + their overall scores) BB (Black box, although do type BB). See below to change from a snowdrift.
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
        bonus = score * 0.02 # This can be changed to what you like, but right now every point in the game is worth 2 cents
        self.log(str(bonus))
        return bonus
        
    def node_post_request(self, participant, node):
        if node.network.full:
            node.network.nodes(type=Source)[0].transmit() 

    def transmission_get_request(self, node, transmissions):
        """All this does is update the last_request property for use in the AFK functions"""
        node.last_request = datetime.now()
        self.stiller_remover(node)
    
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
        nodes = node.network.nodes(type=self.models.ProbeNode) # All probenodes ONLY
        pog = node.network.nodes(type=self.models.PogBot)[0] # Get the POG 
        num_answers = [len(node.infos()) for node in nodes] # Works out how many questions (infos) each node has answered(produced)
    
        my_infos = node.infos()
        if len(my_infos) == 10: # If a node has answered 10 questions
            correct_answers = ["1918","Venus","Bob Odenkirk","1890","Russia","1215","Franklin D. Roosevelt","Asia","Iodine","The Comedy of Errors"]
            answers = [i.contents for i in my_infos]
            score = len([a for a in answers if a in correct_answers])
            node.score_in_quiz = score
    
        if all_same(num_answers):

            if num_answers[0] < 10:
                current_answers = []
                for n in nodes:
                    current_answers.append(max(n.infos(), key=operator.attrgetter("id")))
                # is the current info the most recently made info across all nodes?
                if info == max(current_answers, key=operator.attrgetter("id")):
                    node.network.nodes(type=Source)[0].transmit()

            elif num_answers[0] == 10: # Have ALL nodes answered 10 questions?
                winner = max(nodes, key=operator.attrgetter("score_in_quiz"))
                winner.prestige = 1
                node.network.nodes(type=Source)[0].transmit()  
       
            elif num_answers[0] == 11:
                node.network.rearrange_network() # This kills the source, its vectors and adds the POGbot     

        if len(my_infos) > 11: # Is the questionaire over?
            # This will cause the node to transmit to PogBot ONLY. This is to avoid transmissions being receieved at the wrong time.
            node.transmit(what=info, to_whom=self.models.PogBot)
            info_int = int(info.contents) # This converts it to an integer. Which is good.
            node.donation = info_int 
            leftovers = 10 - info_int
            node.score_in_pgg += leftovers # This will add whatever points the node didn't spend to its score
            node.leftovers = leftovers # This will store their leftovers seperately for use in js

            if node.prestige == 1:
                for node in nodes: # This updates the prestige_list on all nodes. If the current node is the prestige
                    node.prestige_list.append(info_int)

            pogst = node.network.transmissions(status='pending') # How many pending transmissions?
            if len(pogst) == len(nodes):
                pog.receive()

    # Function to manage the removal of stillers
    def stiller_remover(self, node):
        good_nodes = []
        bad_nodes = []
        nodes = node.network.nodes(type=self.models.ProbeNode)
        for n in nodes:
            if (node.last_request - n.last_request).total_seconds() > 60:
                bad_nodes.append(n)
            else:
                good_nodes.append(n)
        if bad_nodes and node.id == max(good_nodes, key=operator.attrgetter("id")).id:
            for n in bad_nodes:
                node.network.max_size -= 1
                n.fail()
            if node.transmissions(): # This is to allow the function to still work in the PGG. Otherwise, the transmission resubmits and breaks the study.
                most_recent_transmission = max(node.transmissions(), key=operator.attrgetter("id"))
                most_recent_transmission.fail()
            most_recent_info = max(node.network.infos(), key=operator.attrgetter("id"))
            self.info_post_request(node, most_recent_info)
