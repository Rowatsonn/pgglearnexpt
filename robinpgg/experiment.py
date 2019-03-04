"""My Social learning and cooperation experiment"""
from dallinger.config import get_config
from dallinger.experiments import Experiment
from dallinger.networks import Burst

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


class pgglearn(Experiment):
    """Define the structure of the experiment."""
    num_participants = 2

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
        return Burst(max_size=5)
        
    def add_note_to_network(self, node, network):
    	"""Hopefully, this should just add a node to the network."""
    	network.add_node(node) 
    	
    def recruit(self):
    	"""Hopefully should recruit one pp at a time, until the network fills."""
    	if self.networks(full=False):
    		self.recruiter.recruit(n=1)
    	else: 
    		self.recruiter.close_recruitment()

    def node_post_request(self, participant, node):
	"""Hopefully should run once the node has been created. Check to see if the node's network is 		full, if it is, then the source should transmit, if it isn't then do nothing."""
	if node.network.full:
		node.network.nodes(type=QuizSource)[0].transmit() 
	else:
 		pass # This is actually redundant, but is here for completeness     
    	
