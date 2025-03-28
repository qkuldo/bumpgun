import pygame as pg
import sys
import json
import modules as mods
import random
import math
import copy
import os
def startup():
	global screen
	global clock
	global font_data
	global assets
	global skins
	global mouse_img
	global mouse_rect
	global current_skin
	global floor
	global music
	global sound_effects
	global face
	global gun
	global lights
	global fullscreen
	global font
	global trauma
	global outlines
	global current_outline
	global map_icons
	global ammo_bar
	global player_bullet
	global game_icons
	global enemy_spritesheets
	global music
	global mousehover_img
	pg.init()
	pg.mixer.init()
	pg.mixer.quit()
	pg.mixer.init()
	pg.mixer.music.set_volume(0.46)
	random.seed(os.times()[1])
	screen = pg.display.set_mode((600,600))
	clock = pg.time.Clock()
	font_file = open("fonts/dialogue.json")
	font_data = json.load(font_file)
	asset_file = open("assets/reference.json")
	assets = json.load(asset_file)
	pg.display.set_caption("BumpGun by qkuldo")
	floor = mods.Sprite(mods.Spritesheet(pg.transform.scale(pg.image.load(assets["images"]["environment"]["factory floor"]), (360*3,360)),360,360),[300,300],0,(360,360))
	lights = pg.transform.scale(pg.image.load(assets["images"]["environment"]["lights"]), (430,430)).convert_alpha()
	skins = []
	outlines = []
	sound_effects = assets["sfx"]["sound effects"]
	music = assets["sfx"]["music"]
	for sfx in sound_effects:
		sound_effects[sfx] = pg.mixer.Sound(sound_effects[sfx])
	music = assets["sfx"]["music"]
	for skin in assets["images"]["skins"].values():
		skins.append(mods.Spritesheet(pg.transform.scale(pg.image.load(skin).convert_alpha(),(26*11,36)),26,36))
	enemy_spritesheets = []
	for enemy_img in assets["images"]["enemies"].values():
		enemy_spritesheets.append(mods.Spritesheet(pg.transform.scale(pg.image.load(enemy_img["img path"]),(enemy_img["img size"][0]*enemy_img["frames"],enemy_img["img size"][1])).convert_alpha(),enemy_img["img size"][0],enemy_img["img size"][1]))
	mouse_img = pg.transform.scale(pg.image.load(assets["images"]["hud"]["mouse"]).convert_alpha(), (16,16)).convert_alpha()
	mousehover_img = pg.transform.scale(pg.image.load(assets["images"]["hud"]["mouse hover"]).convert_alpha(), (16,16)).convert_alpha()
	mouse_rect = mouse_img.get_rect()
	current_skin = skins[0]
	trauma = 2
	map_icons = (mods.Spritesheet(pg.transform.scale(pg.image.load(assets["images"]["hud"]["factory"]),(128*2,128)),128,128),)
	ammo_bar = mods.Spritesheet(pg.transform.scale(pg.image.load(assets["images"]["hud"]["ammo bar"]),(26*12,91)).convert_alpha(),26,91)
	game_icons = mods.Spritesheet(pg.transform.scale(pg.image.load(assets["images"]["hud"]["hud icons"]),(32*3,32)).convert_alpha(),32,32)
	player_bullet = mods.Spritesheet(pg.transform.scale(pg.image.load(assets["images"]["projectiles"]["player bullet"]),(15*2,25)).convert_alpha(),15,25)
def mainloop():
	title()
def dropshadow(org_surf,org_pos,alpha=155,extension=10):
	shadow = org_surf.copy()
	shadow.set_alpha(alpha)
	screen.blit(shadow, (org_pos[0],org_pos[1]+extension))
def title():
	global fullscreen
	title_font = pg.font.Font("fonts/Quaptype.ttf", 80)
	button_font = pg.font.Font("fonts/Quaptype.ttf", 30)
	title_img = title_font.render(font_data["headings"]["title"],True,(255,255,255)).convert_alpha()
	title = mods.Sprite(title_img,(400,200),size=[title_img.get_width(),title_img.get_height()])
	start_button = mods.hud_e.Button(button_font.render(font_data["buttons"]["startgame"],True,(180,180,180)),(100,100),choose_map)
	pg.mouse.set_visible(False)
	while True:
		clicked = False
		mouse_rect.center = pg.mouse.get_pos()
		for event in pg.event.get():
			if (event.type == pg.QUIT):
				pg.mixer.quit()
				pg.quit()
				sys.exit()
			if (event.type == pg.KEYDOWN):
				if (event.key == pg.K_ESCAPE):
					pg.mixer.quit()
					pg.quit()
					sys.exit()
			elif (event.type == pg.MOUSEBUTTONDOWN):
				#print("trejrhtjrjihji")
				clicked = True
		screen.fill((30,30,30))
		dropshadow(title.image,(title.hitbox.x,title.hitbox.y),extension=5,alpha=80)
		title.draw(screen)
		hover = start_button.detect_hover(mouse_rect,button_font.render(font_data["buttons"]["startgame"],True,(255,255,255)),clicked)
		dropshadow(start_button.text,(start_button.textrect.x,start_button.textrect.y),extension=3,alpha=80)
		start_button.draw(screen)
		if (pg.mouse.get_focused() and not hover):
			screen.blit(mouse_img, mouse_rect)
		elif (pg.mouse.get_focused() and hover):
			screen.blit(mousehover_img, mouse_rect)
		pg.display.update()
		clock.tick(60)
def choose_map():
	title_font = pg.font.Font("fonts/Quaptype.ttf", 60)
	button_font = pg.font.Font("fonts/Quaptype.ttf", 25)
	title_img = title_font.render(font_data["headings"]["mapchoose"],True,(255,255,255)).convert_alpha()
	title = mods.Sprite(title_img,(300,100),size=[title_img.get_width(),title_img.get_height()])
	factory_button = mods.hud_e.Button(map_icons[0].load_frame(0),(100,200),game)
	while True:
		clicked = False
		mouse_rect.center = pg.mouse.get_pos()
		for event in pg.event.get():
			if (event.type == pg.QUIT):
				pg.mixer.quit()
				pg.quit()
				sys.exit()
			if (event.type == pg.KEYDOWN):
				if (event.key == pg.K_ESCAPE):
					pg.mixer.quit()
					pg.quit()
					sys.exit()
			elif (event.type == pg.MOUSEBUTTONDOWN):
				#print("trejrhtjrjihji")
				clicked = True
		screen.fill((30,30,30))
		render_Ffloor = factory_button.detect_hover(mouse_rect,clicked=clicked,change_onhover=map_icons[0].load_frame(1))
		if (render_Ffloor):
			floor.angle+=0.5
			render_stack(screen,[floor.image.load_frame(0),floor.image.load_frame(1),floor.image.load_frame(1),floor.image.load_frame(1),floor.image.load_frame(2)],floor.hitbox.center,floor.angle,spread=4)
		else:
			floor.angle = 0
		dropshadow(title.image,(title.hitbox.x,title.hitbox.y),extension=5,alpha=80)
		title.draw(screen)
		dropshadow(factory_button.text,(factory_button.textrect.x,factory_button.textrect.y),extension=3,alpha=80)
		factory_button.draw(screen)
		if (pg.mouse.get_focused() and not render_Ffloor):
			screen.blit(mouse_img, mouse_rect)
		elif (pg.mouse.get_focused() and render_Ffloor):
			screen.blit(mousehover_img, mouse_rect)
		pg.display.update()
		clock.tick(60)
def goto_angle(velocity,angle):
	direction = pg.Vector2(0, velocity).rotate(-angle)
	return direction
def screenshake():
	global trauma
	buffersurf = screen.copy()
	screen.fill((30,30,30))
	buffersurf = pg.transform.rotate(buffersurf,3*random.uniform(-trauma/trauma,trauma/trauma)*random.uniform(-1.0,1.0))
	screen.blit(buffersurf, (0+(7*random.uniform(-trauma/trauma,trauma/trauma)*random.uniform(-1.0,1.0)),0+(7*random.uniform(-trauma/trauma,trauma/trauma)*random.uniform(-1.0,1.0))))
def render_stack(surf,images,pos,rotation,spread=1,scale=()):
	for i, img in enumerate(images):
		rotated_img = pg.transform.rotate(img, rotation)
		rotated_img.set_colorkey((0,0,0))
		surf.blit(rotated_img, (pos[0] - rotated_img.get_width() // 2, pos[1] - rotated_img.get_height() // 2 - i * spread))
def play(environment,track,loops = -1):
	pg.mixer.music.load(music[environment][track])
	pg.mixer.music.play(loops)
def game():
	fade()
	global trauma
	throw_arrow = pg.transform.scale(pg.image.load(assets["images"]["hud"]["throw arrow"]).convert_alpha(),(40,50)).convert_alpha()
	#throw_arrow.set_alpha(225)
	player = copy.copy(current_skin)
	player = mods.Player(player,[300,300],1,(50,50),speed=0.8)
	throw_arrow_rect = throw_arrow.get_rect(x=300,y=300)
	particles = []
	screenshake_duration = 0
	ammo_sprite = mods.Sprite(ammo_bar,[80,240],0,(33,50))
	frames = 0
	jump_frames = 0
	player_projectiles = [] 
	gun_power_sprite = mods.Sprite(game_icons,[78,340],size=(32,32))
	heading_font = pg.font.Font("fonts/Quaptype.ttf", 30)
	heading = mods.Sprite(heading_font.render(font_data["headings"]["placeholder"],True,(210,95,95)),[250,550],size=(32,32))
	heading.invisible = True
	heading_timer = 0
	heading_fade = 5
	floor.angle = 0
	current_level = 1
	level_flash = heading_font.render(font_data["headings"]["start level"]+str(current_level)+font_data["headings"]["start"],True,(230,230,230))
	level_flash = mods.Sprite(level_flash,[300,100],size=(level_flash.get_rect().width,level_flash.get_rect().height))
	sequences = {
		"LEVELINTRO":0,
		"LEVELGAME":1,
		"LEVELEND":2,
		"LEVELCHANGE":3,
		"PLAYERDIE":4
	}
	current_sequence = sequences["LEVELINTRO"]
	player.angle = 180
	clicked = False
	fadein = True
	enemies = []
	effect_queue = []
	#test_sprite = mods.Sprite(enemy_spritesheets[0],[300,300],1,(50,50))
	hp_rect = pg.Rect(80,135,22,80)
	hp_rect.center = (75,150)
	enemies.append(mods.Enemy(enemy_spritesheets[0],[200,300],1,(50,50)))
	shadow_hp_sprite = mods.Sprite(pg.Surface((22,20*4)),(hp_rect.topleft[0]+2,hp_rect.topleft[1]+2))
	shadow_hp_sprite.image.fill((255,126,71))
	shadow_hp_sprite.image.set_alpha(30)
	while True:
		player.fired = False
		screen.fill((30,30,30))
		draw_throw = False
		for event in pg.event.get():
			if (event.type == pg.QUIT):
				pg.mixer.quit()
				pg.quit()
				sys.exit()
			elif (event.type == pg.MOUSEBUTTONDOWN):
				#print("trejrhtjrjihji")
				clicked = True
		keys = pg.key.get_pressed()
		mouse_rect.center = pg.mouse.get_pos()
		if (current_sequence == sequences["LEVELGAME"] and (not player.jumping)):
			player.face_target(mouse_rect.center)
	#		test_sprite.face_target(mouse_rect.center)
		if (current_sequence == sequences["LEVELINTRO"] and keys[pg.K_x]):
			floor.angle = 360
		if (current_sequence == sequences["LEVELGAME"] and keys[pg.K_SPACE] and player.paction_cooldown <= 0 and not player.jumping):
			if (player.mode == 0):
				player.start_jump()
				sound_effects["jump"].play()
				jump_frames = 20
				for i in range(random.randint(3,5),random.randint(7,10)):
					white_random = random.randint(200,225)
					particles.append(mods.Particle(copy.copy(player.pos),[goto_angle(random.randint(3,6),player.angle+random.randint(-4,4))[0],goto_angle(random.randint(3,6),player.angle+random.randint(-4,4))[1]],time_max=2,time_min=1,color=(white_random,white_random,white_random),radius=random.randint(4,6),radius_decrease=0.03,shadow_color=(24,49,86)))
			elif (player.mode == 1 and player.ammo > 0):
				player.fire()
				sound_effects["gunfire"].play()
				trauma += 5
				screenshake_duration = 8
				player_projectiles.append(mods.Projectile(player_bullet,[player.pos[0],player.pos[1]],size=(40,40),speed=0.75,render_type=1,angle=copy.copy(player.angle)+random.randint(-5,5)))
				for i in range(random.randint(3,5),random.randint(7,10)):
					white_random = random.randint(200,225)
					particles.append(mods.Particle(copy.copy(player.pos),[-goto_angle(random.randint(3,6),player.angle+random.randint(-4,4))[0],-goto_angle(random.randint(3,6),player.angle+random.randint(-4,4))[1]],time_max=2,time_min=1,color=(white_random,white_random,white_random),radius=random.randint(2,4),radius_decrease=0.03,shadow_color=(24,49,86)))
				if (player.ammo <= 0):
					heading.invisible = False
					heading_timer = 120
					heading.image = heading_font.render(font_data["headings"]["no ammo"],True,(210,210,210))
			elif (current_sequence == sequences["LEVELGAME"] and player.mode == 1 and player.ammo == 0):
				sound_effects["no ammo"].play()
				player.paction_cooldown = 30
				trauma = 0.5
				screenshake_duration = 8
		elif (current_sequence == sequences["LEVELGAME"] and (keys[pg.K_LCTRL] or keys[pg.K_RCTRL]) and player.modechange_cooldown <= 0  and (not keys[pg.K_LEFT]) and (not keys[pg.K_RIGHT]) and (not keys[pg.K_SPACE]) and not player.jumping):
			if (player.mode == 0):
				player.mode = 1
			elif (player.mode == 1):
				player.mode = 0
			player.modechange_cooldown = 15
			player.paction_cooldown = 0
		#TEST CODE
		#if (keys[pg.K_v]):
		#	enemies.append(mods.Enemy(enemy_spritesheets[0],[200,300],1,(50,50)))
		#elif (keys[pg.K_y] and player.ammo > 0):
		#	player.ammo -= 1
		#elif (keys[pg.K_x] and player.hp > 0):
		#	player.hp -= 1
		#TEST CODE
		#if (not player_dx > max_player_dx_right):
		#	player_dx += 0.5
		if (not floor.hitbox.contains(player.hitbox)):
			#works!:)
			if (not player.on_wall):
				sound_effects["wall hit"].play()
				for i in range(random.randint(3,5),random.randint(7,10)):
					white_random = random.randint(200,225)
					particles.append(mods.Particle(copy.copy(player.pos),[goto_angle(random.randint(3,6),player.angle+random.randint(-4,4))[0],goto_angle(random.randint(3,6),player.angle+random.randint(-4,4))[1]],time_max=3,time_min=1,color=(white_random,white_random,white_random),radius=random.randint(4,6),radius_decrease=0.03,shadow_color=(24,49,86)))
				screenshake_duration = 8
			player.jumping = False
			player.on_wall = True
			trauma += 1
			player.paction_cooldown = 10
			turn_cooldown = 3
			wall_hit_timer = 70
			player.vel = [0,0]
			jump_frames = 0
			if (player.pos[0] > floor.hitbox.center[0]):
				player.pos[0] -= 2
			if (player.pos[0] < floor.hitbox.center[0]):
				player.pos[0] += 2
			if (player.pos[1] > floor.hitbox.center[1]):
				player.pos[1] -= 2
			if (player.pos[1] < floor.hitbox.center[1]):
				player.pos[1] += 2
		floor.update()
		render_stack(screen,[floor.image.load_frame(0),floor.image.load_frame(1),floor.image.load_frame(1),floor.image.load_frame(2)],floor.hitbox.center,floor.angle,spread=4)
		if (player.jumping):
			trauma += 0.5
		if (current_sequence == sequences["LEVELINTRO"] and floor.angle != 360):
			floor.angle += 2
			player.angle += 2
			level_flash.invisible = False
		elif (current_sequence == sequences["LEVELINTRO"] and floor.angle >= 360):
			floor.angle = 0
			player.angle = 180
			level_flash.invisible = True
			play("factory",0)
			current_sequence = sequences["LEVELGAME"]
		player.special_update(screen)
	#	test_sprite.draw(screen,[3,4,2,0,1],spread=1.5)
		for location,particle in sorted(enumerate(particles),reverse=True):
			is_die = particle.update(screen)
			if (is_die):
				particles.pop(location)
		for location,projectile in sorted(enumerate(player_projectiles),reverse=True):
			is_die = projectile.update_life()
			projectile.update(-goto_angle(projectile.speed,projectile.angle))
			projectile.draw(screen,[1,0],spread=2)
			for enemy in enemies:
				if (enemy.hitbox.colliderect(projectile.hitbox) and enemy.dmg_frames <= 0):
					enemy.mode = 2
					enemy.vel = [0,0]
					sound_effects["gun wall hit"].play()
					for i in range(random.randint(3,5),random.randint(7,10)):
						white_random = random.randint(200,225)
						particles.append(mods.Particle(copy.copy(projectile.pos),[goto_angle(random.randint(3,6),projectile.angle+random.randint(-4,4))[0],goto_angle(random.randint(3,6),projectile.angle+random.randint(-4,4))[1]],time_max=3,time_min=1,color=(white_random+20,white_random-50,white_random-50),radius=random.randint(4,6),radius_decrease=0.03,shadow_color=(24,49,86)))
					enemy.hp -= 1
					player_projectiles.pop(location)
				break
			if (is_die or not floor.hitbox.contains(projectile.hitbox)):
				if (player_projectiles != []):
					player_projectiles.pop(location)
					sound_effects["gun wall hit"].play()
					for i in range(random.randint(3,5),random.randint(7,10)):
						white_random = random.randint(200,225)
						particles.append(mods.Particle(copy.copy(projectile.pos),[goto_angle(random.randint(3,6),projectile.angle+random.randint(-4,4))[0],goto_angle(random.randint(3,6),projectile.angle+random.randint(-4,4))[1]],time_max=2,time_min=1,color=(white_random+20,white_random-50,white_random-50),radius=random.randint(4,6),radius_decrease=0.03,shadow_color=(24,49,86)))
		for location,enemy in sorted(enumerate(enemies),reverse=True):
			if (not floor.hitbox.contains(enemy.hitbox)):
				if (enemy.pos[0] > floor.hitbox.center[0]):
					enemy.pos[0] -= 2
				if (enemy.pos[0] < floor.hitbox.center[0]):
					enemy.pos[0] += 2
				if (enemy.pos[1] > floor.hitbox.center[1]):
					enemy.pos[1] -= 2
				if (enemy.pos[1] < floor.hitbox.center[1]):
					enemy.pos[1] += 2
				if (enemy.dmg_frames > 0):	
					enemy.pocket_mode = 1
				else:
					enemy.mode = 1
				enemy.vel = [0,0]
				if (not enemy.on_wall):
					sound_effects["wall hit"].play()
					enemy.on_wall = True
			enemy.special_update(screen,target_pos=player.pos)
			if (enemy.hp <= 0):
				enemies.pop(location)
				for i in range(random.randint(3,5),random.randint(7,10)):
					white_random = random.randint(200,225)
					particles.append(mods.Particle(copy.copy(enemy.pos),[goto_angle(random.randint(3,6),random.randint(1,360))[0],goto_angle(random.randint(3,6),random.randint(1,360))[1]],time_max=5,time_min=2,color=(white_random-50,white_random+20,white_random-50),radius=random.randint(6,9),radius_decrease=0.03,shadow_color=(24,49,86)))
		if (current_sequence == sequences["LEVELGAME"] and heading_timer <= 0):
			heading.invisible = True
		if (screenshake_duration > 0):
			screenshake()
			screenshake_duration -= 1
		level_flash.draw(screen)
		if (player.fired):
			player.muzzle = 10
		if (current_sequence == sequences["LEVELGAME"]):
			if (heading_timer > 0):
				dropshadow(heading.image,heading.hitbox.topleft,extension=5,alpha=80)
			heading.draw(screen)
			if (not player.muzzle > 0):
				ammo_sprite.draw(screen,[player.ammo])
			else:
				ammo_sprite.draw(screen,[11])
			hp_rect.height = player.hp * 4
			hp_rect.bottomleft = (64,190)
			shadow_hp_sprite.draw(screen)
			pg.draw.rect(screen,(255,126,71),hp_rect)
			if (player.mode == 0):
				gun_power_sprite.draw(screen,[0])
			elif (player.mode == 1 and player.ammo > 0):
				gun_power_sprite.draw(screen,[1])
			elif (player.mode == 1 and player.ammo <= 0):
				gun_power_sprite.draw(screen,[2])
			if (pg.mouse.get_focused()):
				screen.blit(mouse_img, mouse_rect)
		if (current_sequence == sequences["LEVELGAME"]):
			if (not trauma == 0):
				trauma -= 0.1
			if (heading_timer > 0):
				heading_timer -= 1
			frames += 1
			if (frames > 60):
				frames = 0
		clicked = False
		if (fadein):
			fade2()
			fadein = not fadein
		pg.display.update()
		clock.tick(60)
def fade():
	current_screen = screen.copy()
	surf = pg.Surface((600,600))
	surf.fill("black")
	surf.set_alpha(0)
	alpha = 0
	while True:
		for event in pg.event.get():
			if (event.type == pg.QUIT):
				pg.quit()
				sys.exit()
		alpha += 3
		if (alpha >= 255):
			break
		surf.set_alpha(alpha)
		screen.blit(current_screen, (0,0))
		screen.blit(surf,(0,0))
		if (pg.mouse.get_focused()):
			screen.blit(mouse_img, mouse_rect)
		pg.display.update()
		clock.tick(60)
#--------------------
def fade2():
	current_screen = screen.copy()
	surf = pg.Surface((600,600))
	surf.fill("black")
	surf.set_alpha(255)
	alpha = 255
	while True:
		for event in pg.event.get():
			if (event.type == pg.QUIT):
				pg.quit()
				sys.exit()
		alpha -= 3
		if (alpha <= 0):
			break
		surf.set_alpha(alpha)
		screen.blit(current_screen, (0,0))
		screen.blit(surf,(0,0))
		if (pg.mouse.get_focused()):
			screen.blit(mouse_img, mouse_rect)
		pg.display.update()
		clock.tick(60)