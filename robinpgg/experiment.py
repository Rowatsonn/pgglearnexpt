"""My Social learning and cooperation experiment"""
from dallinger.config import get_config
from dallinger.experiments import Experiment
from dallinger.networks import Burst
from dallinger.nodes import Source
from dallinger.nodes import Node

from . import models

import json

try:
    from bots import Bot
    Bot = Bot
except ImportError:
    pass

config = get_config()


def extra_parameters():

    types = {
        'custom_variable': bool,
        'num_participants': int,
    }

    for key in types:
        config.register(key, types[key])

def all_same(items):
    return all(x == items[0] for x in items) # Function to help with the post_info check down the line

class pgglearn(Experiment):
    """Define the structure of the experiment."""
    num_participants = 1

    def __init__(self, session=None):
        """Call the same parent constructor, then call setup() if we have a session.
        """
        super(pgglearn, self).__init__(session)
        from . import models 
        self.models = models
        self.experiment_repeats = 1
        self.initial_recruitment_size = 1 # Change this to = the number of probe nodes
        if session:
            self.setup()
            
    def setup(self):
        if not self.networks():
                super(pgglearn, self).setup()
                for net in self.networks():
                        self.models.QuizSource(network=net)
                        self.models.PogBot(network=net)     
           
    def configure(self):
        super(pgglearn, self).configure()
        self.experiment_repeats = 1
        self.custom_variable = config.get('custom_variable')
        self.num_participants = config.get('num_participants', 1)

    def create_network(self):
        """Return a new network."""
        from . import models
        return self.models.RNetwork(max_size=3) #Change this to change the sample size. N + 2
        
    def create_node(self, participant, network):
        """Create a node for the participant. Hopefully a ProbeNode"""
        node = self.models.ProbeNode(network=network, participant=participant)
        node.property1 = json.dumps({
                'score_in_quiz': 0
            })
        node.property2 = json.dumps({
                'prestige' : 0
            })
        node.property3 = json.dumps({
                'score_in_pgg' : 0
            })
        node.property4 = json.dumps({
                'leftovers' : 0,
            })
        node.property5 = json.dumps({
                'prestige_list' : [],
                'conform_list' : [],
                'payoff_list' : [],
            })
        return node
    	
    def recruit(self):
    	"""Hopefully should recruit one pp at a time, until the network fills."""
    	if self.networks(full=False):
    		self.recruiter.recruit(n=1)
    	else: 
    		self.recruiter.close_recruitment()

    def node_post_request(self, participant, node):
        if node.network.full:
            import json
            pog = node.network.nodes(type=self.models.PogBot)[0]
            pog.property1 = json.dumps({
                    'pot': 0 
                })
            pog.property2 = json.dumps({
                    'round': 0 
                })
            pog.property3 = json.dumps({
                    'snowdrift': 1 # Set for whether the game is a snowdrift or not.
                })
            node.network.nodes(type=Source)[0].transmit() 
    
    def info_post_request(self, node, info):
        """This will handle the source transmitting, calculating
        the score in the quiz and assigning prestige to the winner.
        Then finally for the PGG, it will transmit choices to the POG
        """
        nodes = node.network.nodes(type=self.models.ProbeNode) # All probenodes ONLY
        pog = node.network.nodes(type=self.models.PogBot)[0] # Get the POG 
        probes = node.network.size(type=self.models.ProbeNode) # How many probes?
        answers = [len(node.infos()) for node in nodes] # Works out how many questions (infos) each node has answered(produced)
    
        if len(node.infos()) == 10: # If a node has answered 10 questions
            correct_answers = ["1918","Venus","Bob Odenkirk","1890","Russia","1215","Franklin D. Roosevelt","Asia","Iodine","The Comedy of Errors"]
            score = 0
            infos = node.infos()
            for info in infos:
               if info.contents in correct_answers:
                    score +=1 
            node.score_in_quiz = score
    
        if all_same(answers) and answers[0] == 10: #Have ALL nodes answered 10 questions?
            import operator  #For operator.attrgetter
            winner = max(nodes, key=operator.attrgetter("score_in_quiz"))
            winner.prestige = 1
            node.network.nodes(type=Source)[0].transmit()  
       
        elif all_same(answers) and answers[0] == 11:
            node.network.rearrange_network() # This kills the source, its vectors and adds the POGbot     
    
        elif all_same(answers): # Have ALL nodes answered the same number of questions
            current_answers = []
            # For all nodes, get the most recently made info
            import operator
            for n in nodes:
                current_answers.append(max(n.infos(), key=operator.attrgetter("id")))
            # is the current info the most recently made info across all nodes?
            if info == max(current_answers, key=operator.attrgetter("id")):
                try:
                    node.network.nodes(type=Source)[0].transmit()
                except: 
                    pass #This is to stop errors in the PGG part of the study

        if len(node.infos()) > 11: # Is the questionaire over?
            info_int = int(info.contents) # This converts it to an integer. Which is good.
            node.donation = info_int 
            leftovers = 10 - info_int
            node.score_in_pgg += leftovers # This will add whatever points the node didn't spend to its score
            node.leftovers = leftovers # This will store their leftovers seperately for use in js
            if node.prestige == 1:
                for node in nodes: # This updates the prestige_list on all nodes. If the current node is the prestige
                    plist = node.prestige_list
                    plist.extend([info_int])
                    node.prestige_list = plist
            node.transmit(what=info , to_whom=self.models.PogBot)
            pogst = node.network.transmissions(status='pending') # How many pending transmissions?
            pendings = len(pogst) 
            if pendings == probes:
                pog.receive()
# This will cause the node to transmit to PogBot ONLY. This is to avoid transmissions being receieved at the wrong time.
