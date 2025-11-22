import pygame
from OpenGL.GL import *

class App:
	def __init__(self):
		pygame.init()
		pygame.display.set_mode((500,500),pygame.OPENGL|pygame.DOUBLEBUF)
		self.clock=pygame.time.Clock()
		glClearColor(0.1,0.1,0.1,1)
		self.mainloop()

	def mainloop(self):
		run=True
		while run:
			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					run=False

			glClear(GL_COLOR_BUFFER_BIT)
			pygame.display.flip()
			self.clock.tick(60)
		pygame.quit()


App()