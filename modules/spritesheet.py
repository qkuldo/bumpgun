import pygame
class Spritesheet:
	def __init__(self,sheet,width,height):
		self.sheet = sheet
		self.width = width
		self.height = height
	def load_frame(self,frame):
		image = pygame.Surface((self.width,self.height)).convert_alpha()
		image.blit(self.sheet,(0,0),((frame*self.width),0,self.width,self.height))
		image.set_colorkey((0,0,0))
		return image