import pygame as pg
from modules import Spritesheet
import math
import copy
#render type parameter for sprites is to check if the render is or is not a spritestack
#draw special flags include:
#1 = change alpha of frame to index 0 in flag parameter list. index 1 can be used to find frames to change alpha to for read types 0 & 2
def render_stack(surf,images,pos,rotation,spread=1,scale=()):
	for i, img in enumerate(images):
		rotated_img = pg.transform.rotate(img, rotation)
		rotated_img.set_colorkey((0,0,0))
		surf.blit(rotated_img, (pos[0] - rotated_img.get_width() // 2, pos[1] - rotated_img.get_height() // 2 - i * spread))
def goto_angle(velocity,angle):
	direction = pg.Vector2(0, velocity).rotate(-angle)
	return direction
class Sprite:
	def __init__(self,image,pos,render_type=0,size=(5,5),angle = 0,speed=1,oscillate=False):
		self.pos = list(pos)
		self.speed = speed
		self.image = image
		self.oscillate = oscillate
		self.blt_surf = pg.Surface(size)
		self.hitbox = self.blt_surf.get_rect()
		self.hitbox.center = self.pos
		if (self.oscillate):
			self.oscillate_direction = 0
			self.oscillate_top = copy.copy(self.pos[1])-10
			self.oscillate_bottom = copy.copy(self.pos[1])+10
		#oscillate starting downwards
		if (type(self.image) == Spritesheet and render_type==0):
			self.read_img = 0
			self.img_size = (self.image.width,self.image.height)
		elif (type(self.image) == Spritesheet and render_type==1):
			self.read_img = 2
			self.img_size = (self.image.width,self.image.height)
		else:
			self.img_size = self.image.get_size()
			self.read_img = 1
		self.render_type = render_type
		self.vel = [0,0]
		self.angle = angle
		self.other_spritestack_img_bot = []
		self.other_spritestack_img_top = []
		self.debug_mode = False
		self.debug_hb_color = (255,95,95)
		self.invisible = False
	def scale(self,newsize):
		self.img_size = newsize
	def update(self,vel_change=[0,0]):
		self.vel[0] += vel_change[0]
		self.vel[1] += vel_change[1]
		if (self.oscillate):
			if (self.oscillate_direction == 0):
				self.pos[1] += 1*self.vel[1]
			else:
				self.pos[1] -= self.vel[1]
			if (self.pos[1] >= self.oscillate_bottom):
				self.oscillate_direction = 1
			elif (self.pos[1] <= self.oscillate_top):
				self.oscillate_direction = 0
			self.vel = [0,0]
		else:
			self.pos[0] += self.vel[0]
			self.pos[1] += self.vel[1]
		self.hitbox.center = self.pos
	def new_stack(self,img,location=0):
		if (location == 0):
			self.other_spritestack_img_bot.append(img)
		else:
			self.other_spritestack_img_top.append(img)
	def draw(self,screen,frames=[0],spread=1.5,special_flag=0,special_flag_params=[]):
		if (not self.invisible):
			if (self.read_img == 0):
				blt_frame = pg.transform.scale(pg.transform.rotate(self.image.load_frame(frames[0]),self.angle),self.img_size)
				if (special_flag == 1):
					if (special_flag_params[1] == None or special_flag_params[1] == frame):
						blt_frame.set_alpha(special_flag_params[0])
				blt_frame.set_colorkey((0,0,0))
				screen.blit(blt_frame,self.hitbox.topleft)
			elif (self.read_img == 1):
				blt_frame = pg.transform.scale(pg.transform.rotate(self.image,self.angle),self.img_size)
				blt_frame.set_colorkey((0,0,0))
				screen.blit(blt_frame,self.hitbox.topleft)
			elif (self.read_img == 2):
				blt_stack = []
				for cust_frame in self.other_spritestack_img_bot:
					blt_stack.append(cust_frame)
				for frame in frames:
					blt_frame = self.image.load_frame(frame)
					if (special_flag == 1):
						if (special_flag_params[1] == None or special_flag_params[1] == frame):
							blt_frame.set_alpha(special_flag_params[0])
					blt_stack.append(blt_frame)
				for cust_frame in self.other_spritestack_img_top:
					blt_stack.append(cust_frame)
				render_stack(screen,blt_stack,self.hitbox.center,self.angle,spread,self.img_size)
			if (self.debug_mode):
				pg.draw.rect(screen,self.debug_hb_color,self.hitbox)
				circle_surf = pg.Surface((15,15))
				pg.draw.circle(screen,(255,255,255),self.pos,5)
	def copy(self):
		return Sprite(self.image,self.pos,self.render_type,(self.hitbox.width,self.hitbox.height),self.angle,self.speed)
	def face_target(self,targetpos,face=True):
		pdir = (targetpos[0]-self.pos[0],targetpos[1]-self.pos[1])
		length = math.hypot(*pdir)
		if (length == 0.0):
			pdir = (0,1)
		else:
			pdir = (pdir[0]/length, pdir[1]/length)
		if (face):
			self.angle = math.degrees(math.atan2(-pdir[0],-pdir[1]))
		return math.atan2(-pdir[0],-pdir[1])
class Projectile(Sprite):
	def __init__(self,image,pos,render_type=0,size=(5,5),angle = 0,speed=0,life=50,oscillate=False):
		super().__init__(image,pos,render_type,size,angle,speed,oscillate)
		self.life = life
	def update_life(self):
		self.life -= 1
		if (self.life > 0):
			return False
		else:
			return True
class Player(Sprite):
	def __init__(self,image,pos,render_type=0,size=(5,5),angle = 0,speed=0,life=20,oscillate=False):
		super().__init__(image,pos,render_type,size,angle,speed,oscillate)
		self.hp = life
		self.ammo = 10
		self.mode = 0
		self.on_wall = False
		self.jumping = False
		self.modechange_cooldown = 0
		self.paction_cooldown = 0
		self.fired = False
		self.muzzle = 0
		self.states = {
			"jumping":[5,10,10,1,9,2,4],
			"m0":[5,0,3,2],
			"m1 wammo":[7,0,6,2],
			"m1 nammo":[7,0,8,2]
		}
		self.dmg_frames = 0
	def special_update(self,screen,vel_change=[0,0]):
		if (self.jumping):
			vel_change = [vel_change[0]-goto_angle(self.speed,self.angle)[0],vel_change[1]-goto_angle(self.speed,self.angle)[1]] 
		self.update(vel_change)
		if (self.jumping):
			self.draw(screen,self.states["jumping"],special_flag=1,special_flag_params=[80,4])
		else:
			if (self.mode == 0):
				self.draw(screen,self.states["m0"])
			elif (self.mode == 1 and self.ammo > 0):
				self.draw(screen,self.states["m1 wammo"])
			elif (self.mode == 1 and self.ammo <= 0):
				self.draw(screen,self.states["m1 nammo"])
		if (self.paction_cooldown > 0):
			self.paction_cooldown -= 1
		if (self.modechange_cooldown > 0):
			self.modechange_cooldown -= 1
		if (self.muzzle > 0):
			self.muzzle -= 1
	def start_jump(self):
		self.jumping = True
		self.on_wall = False
	def fire(self):
		self.ammo -= 1
		self.paction_cooldown = 30
		self.fired = True
	def change_mode(self):
		if (self.mode == 0):
			self.mode = 1
		elif (self.mode == 1):
			self.mode = 0
		self.modechange_cooldown = 15
		self.paction_cooldown = 0
class Enemy(Player):
	def __init__(self,image,pos,render_type=0,size=(5,5),angle = 0,speed=0.4,life=5,oscillate=False):
		super().__init__(image,pos,render_type,size,angle,speed,life,oscillate)
		self.states = {
			"CHASE":{"frames":[3,5,5,4,2,0,1],"spread":1.5,"mode":0,"transition":0,"pause":0},
			"FACE TARGET":{"frames":[3,4,2,0,1],"spread":1.5,"mode":1,"transition":0,"pause":30},
			"DAMAGE":{"frames":[3,8,7,6],"spread":1.5,"mode":2,"transition":1,"pause":30},
			"ATTACK":{"frames":[3,5,4,2,0,1],"spread":1.5,"mode":3,"transition":0,"pause":35}
		}
		self.mode = 1
		self.completion_pause = 0
		self.pocket_mode = None
		self.attack_steps = 3
		self.highest_step_num = 3
	def special_update(self,screen,vel_change=[0,0],target_pos=(0,0)):
		if (self.dmg_frames > 0):
			self.dmg_frames -= 1
		return_value = None
		if (self.completion_pause <= 0):
			for modeOption in self.states.values():
				if (self.mode == modeOption["mode"]):
					self.draw(screen,modeOption["frames"],spread=modeOption["spread"])
					if (modeOption == self.states["FACE TARGET"]):
						self.face_target(target_pos)
						self.pocket_mode = modeOption["transition"]
					elif (modeOption == self.states["CHASE"]):
						self.on_wall = False
						if (not self.attack_steps <= 0):
							vel_change = [-goto_angle(self.speed,self.angle)[0],-goto_angle(self.speed,self.angle)[1]]
							self.pocket_mode = modeOption["transition"]
						else:
							self.mode = 3
					elif (modeOption == self.states["DAMAGE"]):
						vel_change = [0,0]
						self.dmg_frames = 80
						self.pocket_mode = modeOption["transition"]
					elif (modeOption == self.states["ATTACK"]):
						vel_change = [0,0]
						self.face_target(target_pos)
						self.pocket_mode = modeOption["transition"]
						return_value = 1
					self.completion_pause = modeOption["pause"]
					break
			if (self.attack_steps <= 0):
				self.attack_steps = self.highest_step_num
		else:
			for modeOption in self.states.values():
				if (self.mode == modeOption["mode"]):
					self.draw(screen,modeOption["frames"],spread=modeOption["spread"])
			self.completion_pause -= 1
			if (self.completion_pause <= 0 and self.pocket_mode != None):
				self.mode = copy.copy(self.pocket_mode)
				self.attack_steps -= 1
				self.pocket_mode = None
		self.update(vel_change)
		return return_value