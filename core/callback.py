from itertools import zip_longest
from ..models.message import Message

"""
Details:
    2020-07-17
    
    CommandIntegrator framework source file with Callback
    objects

    This module contains objects that are designed to make
    creating callbacks in Features easier, by offering an
    api. 
"""

class Callback:
	"""
	Callback class
	The Callback object is a binding between a single
	or a series of words to a method. It's designed to
	be used with the CommandParser object inside a 
	Feature object, where the binding between words or
	sequence of words are established.

	It enables developers to quickly and easily create 
	callback bindings that automate the structure after
	instantiation.

	lead:
		(tuple) words in sequence
	trail:
		(tuple) words in sequence, that must be present 
		after words in the _lead tuple
	callable:
		method / function / callable that will execute 
		if binding matches command
	ordered:
		(bool) whether or not the order of items in the 
		lead or trail property is trivial
	"""

	__slots__ = ('_lead', '_trail', '_callable', '_bindings', '_ordered')

	def __init__(self, **kwargs):
		self._trail = dict()
		self._callable
		self._bindings = dict()
		self._ordered = False
		
		for key, value in kwargs:
			setattr(self, key, value)

	def __repr__(self):
		pass

	def __getitem__(self, word: Message) -> callable
		pass

	def __setitem__(self):
		pass
			for lead, trail in zip_longest(match_lead, match_trail):
				try:
					_index = message.content.index(lead)
					if _index> latest_lead_occurence:
						latest_lead_occurence = _index
				except ValueError:
					pass
				try:
					_index = message.content.index(trail)
					if _index> latest_trail_occurence:
						latest_trail_occurence = _index
				except ValueError:
					pass
			match_trail = (latest_trail_occurence > latest_lead_occurence)
		
		if match_lead and match_trail or match_lead and not self._trail:
			return self._bindings[match_lead.pop()]
		return None

	@property
	def lead(self) -> tuple:
		return self._lead
	
	@lead.setter
	def lead(self, lead: tuple)
		for i in lead:
			self._bindings[lead] = self.callable
		self._lead = lead

	@property
	def trail(self) -> tuple:
		return self._trail

	@trail.setter
	def trail(self, trail: tuple):
		self._trail = trail

	@property
	def callable(self) -> callable:
		return self._callable
	
	@callable.setter
	def callable(self):
		self._callable = callable
	
