import pygame
import os
from colors import *

class Block(pygame.sprite.Sprite):
	
	def __init__(self,color = blue, width = 64, height = 64):
		
		super(Block,self).__init__()
		self.image = pygame.Surface((width,height))
		self.image.fill(color) 
		
		#self.rect(left,top,width,height)
		
		self.hSpeed = 0
		self.vSpeed = 0
		
		self.setProp()
		self.sound = pygame.mixer.Sound("C:\\Users\\iamza\\Desktop\\Python\\Works\\PygameTest\\gong.wav")
		
	def setProp(self):
		self.rect = self.image.get_rect()
		self.originX = self.rect.centerx
		self.originY = self.rect.centery
		
		self.speed = 5
		
	def changeSpeed(self,hSpeed,vSpeed):
		self.hSpeed += hSpeed
		self.vSpeed += vSpeed
		
	def setPosition(self,x,y):
		self.rect.x = x - self.originX
		self.rect.y = y - self.originY
		
	def setImage(self,filename = None):
		if filename != None:
			self.image = pygame.image.load(filename)
			self.rect = self.image.get_rect()
			self.setProp()
			
	def playSound(self):
		self.sound.play
	
	def update(self,collidable = pygame.sprite.Group(), event = None):
	
		self.gravity()
		
		self.rect.x += self.hSpeed
		
		collisionList = pygame.sprite.spritecollide(self, collidable, False)
		
		for collidedObject in collisionList:
			if (self.hSpeed > 0):
				self.rect.right = collidedObject.rect.left
			elif (self.hSpeed < 0):
				self.rect.left = collidedObject.rect.right
		
		self.rect.y += self.vSpeed
		
		collisionList = pygame.sprite.spritecollide(self, collidable, False)
		
		for collidedObject in collisionList:
			if (self.vSpeed > 0):
				self.rect.bottom = collidedObject.rect.top
				self.vSpeed = 0
			elif (self.vSpeed < 0):
				self.rect.top = collidedObject.rect.bottom
				self.vSpeed = 0
				
		if not (event == None):
			if (event.type == pygame.KEYDOWN):
				if (event.key == pygame.K_LEFT):
					self.changeSpeed(-(self.speed),0)
				if (event.key == pygame.K_RIGHT):
					self.changeSpeed((self.speed),0)	
				if (event.key == pygame.K_UP):
					if (len(collisionList) >= 1):
						self.changeSpeed(0,-(self.speed)*2)
				if (event.key == pygame.K_DOWN):
					pass
			if (event.type == pygame.KEYUP):
				if (event.key == pygame.K_LEFT):
					if (self.hSpeed != 0): self.hSpeed = 0
				if (event.key == pygame.K_RIGHT):
					if (self.hSpeed != 0): self.hSpeed = 0	
				if (event.key == pygame.K_UP):
					#if (self.vSpeed != 0): self.vSpeed = 0
					pass
				if (event.key == pygame.K_DOWN):
					#if (self.vSpeed != 0): self.vSpeed = 0
					pass
					
	def gravity(self, gravity = .35):
		if (self.vSpeed == 0): self.vSpeed = 1
		else: self.vSpeed += gravity
		

def setMessage(text):
	global message, previousMessage
	message = font.render(text, True, black, white)
	previousMessage = message
		
if (__name__ == "__main__"):
	pygame.init()
	
	window_size = window_width, window_height = 640, 480
	window = pygame.display.set_mode(window_size, pygame.RESIZABLE)
	
	pygame.display.set_caption("Yolo")

	window.fill(white)
	
	clock = pygame.time.Clock()
	framesPerSecond = 60
	
	blockGroup = pygame.sprite.Group()
	
	aBlock = Block()
	aBlock.setImage("C:\\Users\\iamza\\Desktop\\Python\\Works\\PygameTest\\brick.png")
	aBlock.setPosition(window_width/2-150, window_height/2-100)
	
	anotherBlock = Block(red)
	anotherBlock.setPosition(window_width/2,window_height/2+80)
	
	moreBlock = Block(blue, 300, 20)
	moreBlock.setPosition(window_width/2, window_height/2+200)
	
	blockGroup.add(moreBlock,anotherBlock,aBlock)
	
	blockGroup.draw(window)
	aBlock.playSound()

	#SysFont("name",size,bold=False,italic=False)
	font = pygame.font.SysFont(None, 30)
	
	message = previousMessage = None
	setMessage("")
	
	collidableObjects = pygame.sprite.Group()
	collidableObjects.add(anotherBlock,moreBlock)
	
	running = True
	
	while (running):
		for event in pygame.event.get():
			if (event.type == pygame.QUIT) or \
			(event.type == pygame.KEYDOWN and \
			(event.key == pygame.K_ESCAPE or event.key == pygame.K_q)):
				running = False

		clock.tick(framesPerSecond)
		
		window.fill(white)
		
		aBlock.update(collidableObjects, event)
		event = None
		
		if (pygame.sprite.collide_rect(aBlock, anotherBlock)):
			setMessage("There is a collision!")
		else:
			setMessage("")

		if (message != previousMessage):
			setMessage(message)
		
		blockGroup.draw(window)
		window.blit(message, (window_width/2 - message.get_rect().width/2, window_height/2 - 100))
		
		pygame.display.update()
		
	pygame.quit()