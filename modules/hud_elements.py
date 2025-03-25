import pygame as pyg
import random
import os
random.seed(os.times()[1])
class Title_Circle:
	def __init__(self,y):
		self.center = (1,y)
		self.radius = random.randint(10,50)
	def draw(self, screen):
		pyg.draw.circle(screen,(255,255,255), self.center, self.radius, 1)
class Button:
	def __init__(self,text,pos,func):
		#this code also supports icon buttons
		self.text=text
		self.textrect = self.text.get_rect(midtop=pos)
		self.ogtext = text
		self.func = func
	def draw(self,screen):
		#run every loop
		screen.blit(self.text,self.textrect)
	def detect_hover(self,mouserect,change_onhover=None,clicked=False):
		#run every loop
		if (self.textrect.colliderect(mouserect)):
			if (change_onhover!=None):
				self.text = change_onhover
			if (clicked):
				self.func()
			return True
		else:
			self.text = self.ogtext