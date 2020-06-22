from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
	"""
	This class represents a crude structure of 
	the message object received, inspired by the message class
	from the the Discord API.
	
	The intent with this class is to have something 
	independet of platform to refer to with the type
	hinting in this framework, as well as providing 
	a construct to use if a given platform does not 
	provide a message object of this nature from the API.

	The developer can then use the message string and 
	assign it to the 'content' property, which the 
	CommandProcessor relies on to function normally. 
	"""

	author: str
	content: str
	channel: int
	created_at: datetime