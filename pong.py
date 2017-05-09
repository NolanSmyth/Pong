import sys, pygame, math
from pygame.locals import *

WHITE = [255,255,255]
BLACK = [10, 10, 10]
paddle_speed = 16 #consant speed of each paddle
ball_speed = 10
ball_speed_inc = 1
disp_size = [800, 600]
paddle1_rect = (40, 230, 16, 140) #initial positions of paddles
paddle2_rect = (744, 230, 16, 140)
paddle_lim = 20 #how far from the edge the paddle can go
ball_lim = 20 #how far from the edge the ball can go
ball_size = 10 #dimensions of ball
ball_rect = [disp_size[0]/2, disp_size[1]/2, ball_size, ball_size] #initial ball position (middle of screen)
player1_score_location = [200,30]
player2_score_location = [550,30]

class Paddle1(object):
	#Determine how the ball reacts depending on where on the paddle it hits
	
	"""Define a player which has information about its size, position, and image"""
	def __init__(self, startx, starty, paddle_width, paddle_length):
		self.rect = Rect(startx, starty, paddle_width, paddle_length)
		self.angle_dict = { 
		-50: Rect(startx, starty, paddle_width, paddle_length/5),
		-20: Rect(startx, starty + paddle_length/5, paddle_width, paddle_length/5),
		0 : Rect(startx, starty + 2*paddle_length/5, paddle_width, paddle_length/5),
		20: Rect(startx, starty + 3*paddle_length/5, paddle_width, paddle_length/5),
		50: Rect(startx, starty + 4*paddle_length/5, paddle_width, paddle_length/5)
	}

	def update(self):
		key = pygame.key.get_pressed() #handle movement
		if key[pygame.K_w] and self.rect.top > paddle_lim:
			self.rect.y -= paddle_speed 
			for angle in self.angle_dict:
				self.angle_dict[angle].y -= paddle_speed
		if key[pygame.K_s] and self.rect.bottom < disp_size[1]-paddle_lim:
			self.rect.y += paddle_speed 
			for angle in self.angle_dict:
				self.angle_dict[angle].y += paddle_speed

class Paddle2(object):
	"""Define a player which has information about its size, position, and image"""
	def __init__(self, startx, starty, paddle_width, paddle_length):
		self.rect = Rect(startx, starty, paddle_width, paddle_length)
		self.angle_dict = { 
		-50: Rect(startx, starty, paddle_width, paddle_length/5),
		-20: Rect(startx, starty + paddle_length/5, paddle_width, paddle_length/5),
		0 : Rect(startx, starty + 2*paddle_length/5, paddle_width, paddle_length/5),
		20: Rect(startx, starty + 3*paddle_length/5, paddle_width, paddle_length/5),
		50: Rect(startx, starty + 4*paddle_length/5, paddle_width, paddle_length/5)
		}

	def update(self):
		key = pygame.key.get_pressed() #handle movement
		if key[pygame.K_UP] and self.rect.top > paddle_lim:
			self.rect.y -= paddle_speed 
			for angle in self.angle_dict:
				self.angle_dict[angle].y -= paddle_speed
		if key[pygame.K_DOWN] and self.rect.bottom < disp_size[1]-paddle_lim:
			self.rect.y += paddle_speed 
			for angle in self.angle_dict:
				self.angle_dict[angle].y += paddle_speed

class Ball(object):
	'''The pong ball. Has a postion and velocity which changes when interacting with paddles'''
	def __init__(self, startx, starty, width, height, speed):
		self.rect = Rect(startx, starty, width, height)
		self.vel = [speed, 0]
		self.speed = math.sqrt(self.vel[0]**2 + self.vel[1]**2)

	def update(self):
		if self.rect.top <= ball_lim or self.rect.bottom >= disp_size[1] - ball_lim:
			self.vel[1] = -self.vel[1]
		self.rect.x += self.vel[0]
		self.rect.y += self.vel[1]

	def reset_ball(self, x, y, width, height, speed):
		self.rect = Rect(x,y,width,height)
		self.vel = [speed, 0]
		self.speed = speed

class Pong(object):

	def detect_collision(self):
		if self.ball.rect.colliderect(self.paddle1.rect): 
			self.ball.speed += ball_speed_inc
			deflect_angle = math.radians(self.ball.rect.collidedict(self.paddle1.angle_dict,1)[0])
			self.ball.vel[0] = self.ball.speed*math.cos(deflect_angle)
			self.ball.vel[1] = self.ball.speed*math.sin(deflect_angle)
			self.ball.rect.x +=10
		if self.ball.rect.colliderect(self.paddle2.rect):
			self.ball.speed += ball_speed_inc
			deflect_angle = math.radians(self.ball.rect.collidedict(self.paddle2.angle_dict,1)[0])
			self.ball.vel[0] = -self.ball.speed*math.cos(deflect_angle)
			self.ball.vel[1] = self.ball.speed*math.sin(deflect_angle)
			self.ball.rect.x -=10

	def detect_score(self):
		if self.ball.rect.left <0:
			self.player2_score +=1
			self.ball.reset_ball(ball_rect[0],ball_rect[1],ball_rect[2],ball_rect[3],ball_speed)
		if self.ball.rect.right > disp_size[0]:
			self.player1_score +=1
			self.ball.reset_ball(ball_rect[0],ball_rect[1],ball_rect[2],ball_rect[3],ball_speed)

	def display_score(self):
		score_font = pygame.font.Font(None, 50)
		player1_score_img = score_font.render(str(self.player1_score), True, WHITE, BLACK)
		player2_score_img = score_font.render(str(self.player2_score), True, WHITE, BLACK)
		screen.blit(player1_score_img, player1_score_location)
		screen.blit(player2_score_img, player2_score_location)

	def main(self, screen):
		
		clock = pygame.time.Clock() #define global clock
		self.paddle1 = Paddle1(*paddle1_rect) #initialize paddles
		self.paddle2 = Paddle2(*paddle2_rect)
		self.ball = Ball(ball_rect[0],ball_rect[1],ball_rect[2],ball_rect[3],ball_speed) #initialize ball
		self.player1_score = 0 #inital score
		self.player2_score = 0
		
		while 1:
			dt = clock.tick(30) #tick 30fps

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return

			screen.fill(BLACK) #fill background
			screen.fill(WHITE, self.paddle1.rect)
			screen.fill(WHITE, self.paddle2.rect)
			screen.fill(WHITE, self.ball.rect)
			self.paddle1.update() 
			self.paddle2.update()
			self.ball.update()
			self.detect_collision()
			self.detect_score()
			self.display_score()
			pygame.display.flip()
			
if __name__ == "__main__":
	pygame.init()
	screen = pygame.display.set_mode(disp_size)
	Pong().main(screen)
