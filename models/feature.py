from ..baseclasses.baseclasses import FeatureBase

"""
Details:
    2020-07-05
    
    CommandIntegrator framework Feature source file

Module details:
    
    The Feature object is a ready-to-use variant 
    of the FeatureBase class which is designed for 
    inheritation. Using the Feature object enables 
    developers to use the default configuration of 
    the Feature without writing a trivial inherit with only
    a constructor for child and parent class, allowing
    for two ways to develop with CommandIntegrator.
"""

class Feature(FeatureBase):
	"""
	Class with attributes and methods from the base
    class FeatureBase, to be used when
    no method overloading is desired by the developer.
	"""
	def __init__(self, *args, **kwargs):
		try:
			self.__class__.__name__ = kwargs['name']
		except KeyError:
			pass
		super().__init__(*args, **kwargs)