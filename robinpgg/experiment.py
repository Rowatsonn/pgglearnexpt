"""My Social learning and cooperation experiment"""
from dallinger.config import get_config
from dallinger.experiments import Experiment
from dallinger.networks import Burst
from dallinger.nodes import Source
from dallinger.nodes import Node

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
        self.initial_recruitment_size = 1
        if session:
            self.setup()
            
    def setup(self):
        if not self.networks():
                super(pgglearn, self).setup()
                for net in self.networks():
                        self.models.QuizSource(network=net)        
           
    def configure(self):
        super(pgglearn, self).configure()
        self.experiment_repeats = 1
        self.custom_variable = config.get('custom_variable')
        self.num_participants = config.get('num_participants', 1)

    def create_network(self):
        """Return a new network."""
        return Burst(max_size=2)
        
    def create_node(self, participant, network):
        """Create a node for the participant. Hopefully a ProbeNode"""
        node = self.models.ProbeNode(network=network, participant=participant)
        node.property1 = json.dumps({
                'score_in_quiz': 0
            })
        node.property2 = json.dumps({
                'prestige' : "FALSE"
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
            node.network.nodes(type=Source)[0].transmit()
        else:
            pass # This is actually redundant, but is here for completeness
    
    def info_post_request(self, node, info):
        """This will handle the source transmitting, calculating
        the score in the quiz and assigning prestige to the winner."""
        nodes = node.network.nodes(type=self.models.ProbeNode) # All nodes but the source
        answers = [len(node.infos()) for node in nodes] # Works out how many questions each node has answered
    
        if len(node.infos()) == 10: # If the nodes have answered 10 questions
            correct_answers = ["1918","Venus","Bob Odenkirk","1890","Russia","1215","Franklin D. Roosevelt" ,     "Asia" , "Iodine" , "The Comedy of Errors"]
            score = 0
            infos = node.infos()
            for info in infos:
               if info.contents in correct_answers:
                    score +=1 
            node.score_in_quiz = score
    
        if all_same(answers) and answers[0] == 10: #Have all nodes answered 10 questions?
            import operator 
            winner = max(nodes, key=operator.attrgetter("score_in_quiz"))
            winner.prestige = "TRUE"
            node.network.nodes(type=Source)[0].transmit()         
    
        elif all_same(answers):
            node.network.nodes(type=Source)[0].transmit() 
         
