import pygame
from sys import exit
from random import randint, choice

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 60

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Chicken Little')
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False

start_time = 0
score = 0
bg_x = 0

bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.1)
bg_music.play(loops = -1)


# sky_surface = pygame.image.load('graphics/plx-1.png').convert()
sky_surface = pygame.transform.scale(pygame.image.load('graphics/plx-1.png').convert_alpha(),(800, 400))
#para1_surface = pygame.transform.scale(pygame.image.load('graphics/plx-2.png').convert_alpha(),(800, 400))
#para2_surface = pygame.transform.scale(pygame.image.load('graphics/plx-3.png').convert_alpha(),(800, 400))
#para3_surface = pygame.transform.scale(pygame.image.load('graphics/plx-4.png').convert_alpha(),(800, 400))
ground_surface = pygame.image.load('graphics/ground-1.png').convert_alpha()
ground_width = ground_surface.get_width()
ground_height = ground_surface.get_height()
#bg_rect_list = [para1_surface.get_rect(topright = (0,0))]

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_walk_1 = pygame.transform.scale(pygame.image.load('graphics/player/ChikBoy_run1.png').convert_alpha(),(84, 84))
		player_walk_2 = pygame.transform.scale(pygame.image.load('graphics/player/ChikBoy_run2.png').convert_alpha(),(84, 84))
		player_walk_3 = pygame.transform.scale(pygame.image.load('graphics/player/ChikBoy_run3.png').convert_alpha(),(84, 84))
		player_walk_4 = pygame.transform.scale(pygame.image.load('graphics/player/ChikBoy_run4.png').convert_alpha(),(84, 84))
		player_walk_5 = pygame.transform.scale(pygame.image.load('graphics/player/ChikBoy_run5.png').convert_alpha(),(84, 84))
		player_walk_6 = pygame.transform.scale(pygame.image.load('graphics/player/ChikBoy_run6.png').convert_alpha(),(84, 84))
		player_walk_7 = pygame.transform.scale(pygame.image.load('graphics/player/ChikBoy_run7.png').convert_alpha(),(84, 84))
		player_walk_8 = pygame.transform.scale(pygame.image.load('graphics/player/ChikBoy_run8.png').convert_alpha(),(84, 84))
		player_walk_9 = pygame.transform.scale(pygame.image.load('graphics/player/ChikBoy_run9.png').convert_alpha(),(84, 84))
		player_walk_10 = pygame.transform.scale(pygame.image.load('graphics/player/ChikBoy_run10.png').convert_alpha(),(84, 84))

		self.player_walk = [player_walk_1, player_walk_2, player_walk_3, player_walk_4, player_walk_5, player_walk_6, player_walk_7, player_walk_8, player_walk_9, player_walk_10]
		self.player_index = 0
		#self.player_jump = pygame.image.load('graphics/player/ChikBoy_jump.png').convert_alpha()
		self.player_jump = pygame.transform.scale(pygame.image.load('graphics/player/ChikBoy_jump.png').convert_alpha(),(84, 84))
		

		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (80,SCREEN_HEIGHT - ground_height))
		self.gravity = 0

		#self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
		#self.jump_sound.set_volume(0.5)

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= (SCREEN_HEIGHT - ground_height):
			self.gravity = -20
			#self.jump_sound.play()

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= (SCREEN_HEIGHT - ground_height):
			self.rect.bottom = (SCREEN_HEIGHT - ground_height)

	def animation_state(self):
		if self.rect.bottom < (SCREEN_HEIGHT - ground_height): 
			self.image = self.player_jump
			#self.image = pygame.transform.scale(self.player_jump,(84, 84))

		else:
			self.player_index += 0.3
			if self.player_index >= len(self.player_walk):self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]
			#self.image = pygame.transform.scale(self.player_walk[int(self.player_index)],(84, 84))

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
			y_pos = (SCREEN_HEIGHT - ground_height) - 90
		else:
			snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
			snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
			self.frames = [snail_1,snail_2]
			y_pos  = (SCREEN_HEIGHT - ground_height)

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

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
	score_rect = score_surf.get_rect(center = (400,50))
	screen.blit(score_surf,score_rect)
	return current_time

def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
		obstacle_group.empty()
		return False
	else: return True


#to store parallax images
bg_images = []
for i in range(1,6):
	bg_image = pygame.transform.scale(pygame.image.load(f"graphics/plx-{i}.png").convert_alpha(),(800, 400))
	bg_images.append(bg_image)
bg_width = bg_images[0].get_width()

#to draw para background
def draw_bg():
  #redraw image 5 times beside each other
  for x in range(5):
    speed = 3.5
    for i in bg_images:
      screen.blit(i, ((x * bg_width) - bg_x * speed, 0))
      speed += 0.2

def draw_ground():
  for x in range(15):
    screen.blit(ground_surface, ((x * ground_width) - bg_x * 6.5, SCREEN_HEIGHT - ground_height))


# Intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Pixel Runner',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)


#Game loop
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if game_active:
			if event.type == obstacle_timer:
				obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
		
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)


	if game_active:

		draw_bg()
		draw_ground()
		#if len(bg_rect_list) <= 3:
		#	bg_rect_list.append(para1_surface.get_rect(topright = (0,0)))

		
		#screen.blit(sky_surface,(0,0))
		#screen.blit(para1_surface,(bg_x,0))
		bg_x += 0.5
		#screen.blit(para2_surface,(bg2_x,0))
		#bg2_x -= 0.8
		#screen.blit(para3_surface,(bg3_x,0))
		#bg3_x -= 1
		#screen.blit(ground_surface,(0,300))
		score = display_score()
		
		player.draw(screen)
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		#bg_rect_list = bg_movement(bg_rect_list)

		game_active = collision_sprite()
		
	else:
		screen.fill((94,129,162))
		screen.blit(player_stand,player_stand_rect)

		score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
		score_message_rect = score_message.get_rect(center = (400,330))
		screen.blit(game_name,game_name_rect)

		if score == 0: screen.blit(game_message,game_message_rect)
		else: screen.blit(score_message,score_message_rect)

	pygame.display.update()
	clock.tick(FPS)