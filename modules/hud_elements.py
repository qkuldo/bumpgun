import pygame as pyg
import random
import os
random.seed(os.times()[1])
class Button:
	"""
	Class for creating and managing buttons in the HUD.
	"""
	def __init__(self,text,pos,func):
		#this code also supports icon buttons
		self.text=text
		self.textrect = self.text.get_rect(midtop=pos)
		self.ogtext = text
		self.func = func
	def draw(self,screen):
		#run every loop
		screen.blit(self.text,self.textrect)
	def detect_hover(self,mouserect,change_onhover=None,clicked=False,immediate_call=True):
		# Detect mouse hover over a button and handle click events.
		#run every loop
		if (self.textrect.colliderect(mouserect)):
			if (change_onhover!=None):
				self.text = change_onhover
			if (clicked):
				if (immediate_call):
					self.func()
				else:
					return 3
			return True
		else:
			self.text = self.ogtext