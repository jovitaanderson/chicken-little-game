import pygame
import math
from sys import exit
from random import randint, choice

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 64
FPS = 60

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Chicken Little')
test_font = pygame.font.Font('font/VT323-Regular.ttf', 50)
title_font = pygame.font.Font('font/VT323-Regular.ttf', 70)
game_active = False

start_time = 0
score = 0
bg_x = 0
theme = 1

bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.1)
bg_music.play(loops = -1)


class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		#to store character images
		self.player_walk = []
		for i in range(1,11):
			player_walk_image = pygame.transform.scale(pygame.image.load(f"graphics/player/ChikBoy_run{i}.png").convert_alpha(),(84, 84))
			self.player_walk.append(player_walk_image)

		self.player_index = 0
		self.player_jump = pygame.transform.scale(pygame.image.load('graphics/player/ChikBoy_jump.png').convert_alpha(),(84, 84))
		
		self.player_crouch = pygame.transform.scale(pygame.image.load('graphics/player/ChikBoy_crouch.png').convert_alpha(),(84, 95))
		self.crouch = False

		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (80,SCREEN_HEIGHT - GROUND_HEIGHT))
		self.gravity = 0

		self.jump_sound = pygame.mixer.Sound('audio/jump.wav')
		self.jump_sound.set_volume(0.5)

		# obstacle audio to be modified
		self.obstacle_sound = pygame.mixer.Sound('audio/collision.wav')
		self.obstacle_sound.set_volume(1)

	def player_input(self):
		keys = pygame.key.get_pressed()
		if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.bottom >= (SCREEN_HEIGHT - GROUND_HEIGHT):
			print("jump detected")
			self.gravity = -20
			self.jump_sound.play()

		if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right <= SCREEN_WIDTH - (SCREEN_WIDTH * 1/10):
			print("right detected")
			self.rect.x += 2.5

		if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.right >= SCREEN_WIDTH * 1/10:
			print("left detected")
			self.rect.x -= 2.5
			
		if (keys[pygame.K_DOWN] or keys[pygame.K_s] and self.rect.bottom <= (SCREEN_HEIGHT - GROUND_HEIGHT)):
			self.crouch = True
			self.gravity = 10
			print("crouched detected")
		
		#todo: add player crouch movement
		#for event in pygame.event.get():
		#	if event.type == pygame.KEYDOWN :
		#		if event.key == pygame.K_DOWN :
		#			self.image = pygame.transform.scale(pygame.image.load('graphics/player/ChikBoy_crouch.png').convert_alpha(),(84, 50))
		#			self.rect = self.image.get_rect(midbottom = (80,SCREEN_HEIGHT - ground_height))

		#	if event.type == pygame.KEYUP :
		#		if event.key == pygame.K_DOWN :
		#			self.image = self.player_walk[0]
		#			self.rect = self.image.get_rect(midbottom = (80,SCREEN_HEIGHT - ground_height))

		#todo: add player crouch movement
		#if keys[pygame.K_DOWN] and self.rect.bottom == (SCREEN_HEIGHT - ground_height):
		#	self.image = pygame.transform.scale(pygame.image.load('graphics/player/ChikBoy_crouch.png').convert_alpha(),(84, 50))
		#	self.rect = self.image.get_rect(midbottom = (80,SCREEN_HEIGHT - ground_height))
		#elif not keys[pygame.K_DOWN] and self.gravity==0:
		#	self.image = self.player_walk[0]
		#	self.rect = self.image.get_rect(midbottom = (80,SCREEN_HEIGHT - ground_height))

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= (SCREEN_HEIGHT - GROUND_HEIGHT):
			self.rect.bottom = (SCREEN_HEIGHT - GROUND_HEIGHT)

	def animation_state(self):
		# player jump
		if self.rect.bottom < (SCREEN_HEIGHT - GROUND_HEIGHT): 
			self.image = self.player_jump

		# player crouch
		elif self.crouch:
			self.image = self.player_crouch
			self.crouch = False


		# player walk
		else:
			self.player_index += 0.3
			if self.player_index >= len(self.player_walk):self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'fly':
			fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
			fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
			self.frames = [fly_1,fly_2]
			y_pos = (SCREEN_HEIGHT - GROUND_HEIGHT) - 90
		elif type == 'snail':
			snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
			snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
			self.frames = [snail_1,snail_2]
			y_pos  = (SCREEN_HEIGHT - GROUND_HEIGHT)
		else:
			snake_1 = pygame.transform.scale(pygame.image.load('graphics/snake/Snake1.png').convert_alpha(),(50, 50))
			snake_2 = pygame.transform.scale(pygame.image.load('graphics/snake/Snake2.png').convert_alpha(),(50, 50))
			self.frames = [snake_1,snake_2]
			y_pos  = (SCREEN_HEIGHT - GROUND_HEIGHT) + 5


		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= 6
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()

class Crosshair(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
	
		self.gunshot = pygame.mixer.Sound('audio/shooting.wav')
		self.cool_down_count = 0
		self.image = pygame.image.load('graphics/shooting/crosshair_red_large.png')
		self.rect = self.image.get_rect()
		self.activate_cooldown = False

	def shoot(self):
		# if player is not on cooldown
		if not self.activate_cooldown:
			print("player shooting")
			self.gunshot.play()
			self.cool_down_count = 1
			self.cool_down()
			# shoot_press_time = pygame.time.get_ticks()
			pygame.sprite.spritecollide(crosshair, obstacle_group, True)

		# if player shot 3 times, he or she will be placed on cooldown
		else:
			print("player on cooldown")
			pygame.sprite.spritecollide(crosshair, obstacle_group, False)
			self.cool_down()


	# update position of crosshair to mouse position
	def update(self):
		self.rect.center = pygame.mouse.get_pos() # get x and y position of mouse
		self.cool_down()

	def cool_down(self):
		if (self.cool_down_count == 1 ):
			self.activate_cooldown = True
			self.image = pygame.image.load('graphics/shooting/crosshair_white_large.png')

		else:
			self.image = pygame.image.load('graphics/shooting/crosshair_red_large.png')

#Crosshair
crosshair = Crosshair()
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

# crosshair_group.draw(screen)



#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = test_font.render(f'Score: {current_time}',False,(255, 255, 255))
	score_rect = score_surf.get_rect(center = (400,50))
	screen.blit(score_surf,score_rect)
	return current_time

def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
		obstacle_group.empty()
		print("Collision")
		bg_music = pygame.mixer.Sound('audio/collision.wav')
		bg_music.play()
		return False
	else: 
		return True


#player idle images
player_idle = []
for i in range(1,7):
	player_idle_image = pygame.transform.scale(pygame.image.load(f"graphics/player/ChikBoy_idle{i}.png").convert_alpha(),(84, 84))
	player_idle_image = pygame.transform.rotozoom(player_idle_image,0,2)
	player_idle.append(player_idle_image)
player_idle_index = 0

#world images
world = []
for i in range(0,60):
	world_images = pygame.transform.scale(pygame.image.load(f"graphics/world/frame_{i}_delay-0.34s.png").convert_alpha(),(390, 390))
	#world_images = pygame.transform.rotozoom(world_images,0,4)
	world.append(world_images)
world_index = 0

# gradient background: author: https://stackoverflow.com/questions/62336555/how-to-add-color-gradient-to-rectangle-in-pygame
def gradientRect( window, left_colour, right_colour, target_rect ):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pygame.Surface( ( 2, 2 ) )                                   # tiny! 2x2 bitmap
    pygame.draw.line( colour_rect, left_colour,  ( 0,0 ), ( 0,1 ) )            # left colour line
    pygame.draw.line( colour_rect, right_colour, ( 1,0 ), ( 1,1 ) )            # right colour line
    colour_rect = pygame.transform.smoothscale( colour_rect, ( target_rect.width, target_rect.height ) )  # stretch!
    window.blit( colour_rect, target_rect )  

# background themes
bg_images = []

bg_theme_1 = pygame.transform.scale(pygame.image.load("graphics/background/background_theme1.png").convert_alpha(),(800, 400))
bg_theme_2 = pygame.transform.scale(pygame.image.load("graphics/background/background_theme2.png").convert_alpha(),(800, 400))
bg_theme_3 = pygame.transform.scale(pygame.image.load("graphics/background/background_theme3.png").convert_alpha(),(800, 400))
bg_theme_4 = pygame.transform.scale(pygame.image.load("graphics/background/background_theme4.png").convert_alpha(),(800, 400))

#bg_rect = bg_theme_1.get_rect()

bg_images.append(bg_theme_1)
bg_images.append(bg_theme_1)

def draw_bg():
	for x, i in enumerate(bg_images):
		screen.blit(i, ((x * bg_theme_1.get_width()) + bg_x, 0))
		#bg_rect.x = x  * bg_theme_1.get_width() + bg_x
		#pygame.draw.rect(screen, (255,0,0), bg_rect,1)

# Intro screen
player_stand = pygame.transform.scale(pygame.image.load('graphics/player/ChikBoy_run1.png').convert_alpha(),(84, 84))
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = title_font.render('CHICKEN LITTLE',False,(34, 37, 74))
game_name_rect = game_name.get_rect(center = (400,80))
game_name_surface = pygame.Surface(game_name.get_size(), pygame.SRCALPHA)
game_name_surface.fill((192, 192, 192))
game_name_surface.set_alpha(180)

game_message = test_font.render('Press [SPACE] to start',False,(145, 54, 54))
game_message_rect = game_message.get_rect(center = (400,330))

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)
new_game_timer = 20

cooldown_timer = pygame.USEREVENT + 1
pygame.time.set_timer(cooldown_timer, 3000)

#Game loop
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			crosshair.shoot()
	
		if game_active:
			# handle player cooldown
			if crosshair.activate_cooldown:
				if event.type == cooldown_timer:				
					crosshair.cool_down_count = 0
					crosshair.activate_cooldown = False

			# handle obstacle 
			if event.type == obstacle_timer:
				if theme == 1:
					obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
				elif theme == 2:
					obstacle_group.add(Obstacle(choice(['fly','snake','snake'])))
				else:
					obstacle_group.add(Obstacle(choice(['fly','snail','snake'])))
		
		
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and (new_game_timer == 0 or score == 0) :
				game_active = True
				new_game_timer = 20
				start_time = int(pygame.time.get_ticks() / 1000)


	if game_active:

		draw_bg()
		score = display_score()

		bg_x -= 4 
		if abs(bg_x)> bg_theme_1.get_width():
			del bg_images[0]
			if score < 10:
				bg_images.append(bg_theme_1)
				theme = 1
			elif score < 20:
				bg_images.append(bg_theme_2)
				theme = 2
			elif score < 30:
				bg_images.append(bg_theme_3)
				them = 3
			else:
				bg_images.append(bg_theme_4)
				theme = 4
			bg_x = 0

		crosshair_group.draw(screen)
		crosshair_group.update()

		player.draw(screen)
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		game_active = collision_sprite()
		
	else:
		#Intro idle animation
		player_idle_index += 0.12
		if player_idle_index >= len(player_idle):player_idle_index = 0
		player_idle_image = player_idle[int(player_idle_index)]
		player_idle_image_rect = player_idle_image.get_rect(center = (400,200))

		#Intro world animation
		world_index += 0.12
		if world_index >= len(world):world_index = 0
		world_image = world[int(world_index)]
		world_image_rect = world_image.get_rect(center = (400,200))
		gradientRect( screen, (6,9,24), (9,19,25), pygame.Rect( 0,0, SCREEN_WIDTH, SCREEN_HEIGHT ) )
		screen.blit(world_image,world_image_rect)

		screen.blit(player_idle_image,player_idle_image_rect)
		score_message = test_font.render(f'Your score: {score}',False,(145, 54, 54))
		score_message_rect = score_message.get_rect(center = (400,330))
		screen.blit(game_name_surface,game_name_rect)
		screen.blit(game_name,game_name_rect)
	

		#initilize back to default values
		bg_x = 0
		player.remove()
		player.add(Player())
		theme = 1
		bg_images.clear()
		bg_images.append(bg_theme_1)
		bg_images.append(bg_theme_1)

		if score == 0: 
			screen.blit(game_message,game_message_rect)
		else: 
			screen.blit(score_message,score_message_rect)

		if new_game_timer > 0 :
			new_game_timer -= 1

	pygame.display.update()
	clock.tick(FPS)