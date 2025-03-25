import pygame
import random
class Particle:
	def __init__(self,pos,velocity,gravity=0.1,time_max=6,time_min=4,color=(95,95,95),radius=5,radius_decrease=0.05,shadow_color=None):
		self.pos = pos
		self.velocity = velocity
		self.gravity = gravity
		self.color = color
		self.time = random.randint(time_min,time_max)
		self.radius = radius
		self.radius_decrease = radius_decrease
		self.shadow_color = shadow_color
	def update(self,screen,shadow_offset=3):
		self.pos[0]+=self.velocity[0]
		self.pos[1]+=self.velocity[1]
		self.pos[1]+=self.gravity
		self.time -= 0.1
		self.radius -= self.radius_decrease
		if (self.shadow_color):
			pygame.draw.circle(screen,self.shadow_color,(int(self.pos[0]),int(self.pos[1])+shadow_offset),int(self.radius))
		pygame.draw.circle(screen,self.color,(int(self.pos[0]),int(self.pos[1])),int(self.radius))
		if (self.time <= 0):
			return True
