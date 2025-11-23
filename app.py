import pygame
from OpenGL.GL import *
import numpy
import ctypes
from OpenGL.GL.shaders import compileShader,compileProgram

class App:
	def __init__(self):
		pygame.init()
		pygame.display.set_mode((700,400),pygame.OPENGL|pygame.DOUBLEBUF)
		self.clock=pygame.time.Clock()
		glClearColor(0.1,0.1,0.1,1)
		self.shader=self.createShader("shaders/vertex.txt","shaders/fragment.txt")
		glUseProgram(self.shader)

		self.triangle=Triangle()
		self.quad=Quad()
		self.mainloop()

	def createShader(self,vertex_path,fragment_path):
		with open(vertex_path,'r') as file:
			vertex_src = file.readlines()
		
		with open(fragment_path,'r') as file:
			fragment_src = file.readlines()

		shader = compileProgram(
			compileShader(vertex_src,GL_VERTEX_SHADER),
			compileShader(fragment_src,GL_FRAGMENT_SHADER)
			)

		return shader

	def mainloop(self):
		run=True
		while run:
			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					run=False

			glClear(GL_COLOR_BUFFER_BIT)

			glUseProgram(self.shader)

			#glBindVertexArray(self.triangle.vao)
			#glDrawArrays(GL_TRIANGLES,0,self.triangle.vertex_count)
			
			glBindVertexArray(self.quad.vao)
			glDrawArrays(GL_TRIANGLES, 0, self.quad.vertex_count)

			pygame.display.flip()
			self.clock.tick(60)

		self.triangle.destroy()
		self.quad.destroy()

		glDeleteProgram(self.shader)
		pygame.quit()


class Quad:
    def __init__(self):
        # Two triangles forming a quad
        self.vertices = numpy.array([
            # pos               # color
            -0.5, -0.5, 0.0,     1.0, 1.0, 0.0,
             0.5, -0.5, 0.0,     0.0, 1.0, 1.0,
             0.5,  0.5, 0.0,     1.0, 0.0, 1.0,

            -0.5, -0.5, 0.0,     1.0, 1.0, 0.0,
             0.5,  0.5, 0.0,     1.0, 0.0, 1.0,
            -0.5,  0.5, 0.0,     0.0, 1.0, 0.0,
        ], dtype=numpy.float32)

        self.vertex_count = 6

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        # Position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

        # Color
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))

class Triangle:
	def __init__(self):
		self.verticies=(
			-0.5,-0.5,0.0, 1.0,0.0,0.0,
			 0.5,-0.5,0.0, 0.0,1.0,0.0,
			 0.0, 0.5,0.0, 0.0,0.0,1.0
		)

		self.verticies = numpy.array(self.verticies,dtype=numpy.float32)

		self.vertex_count = 3

		self.vao = glGenVertexArrays(1)
		glBindVertexArray(self.vao)
		self.vbo = glGenBuffers(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
		glBufferData(GL_ARRAY_BUFFER,self.verticies.nbytes,self.verticies,GL_STATIC_DRAW)

		glEnableVertexAttribArray(0)
		glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(0))
		
		glEnableVertexAttribArray(1)
		glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(12))



	def destroy(self):
		glDeleteVertexArrays(1,(self.vao,))
		glDeleteBuffers(1,(self.vbo,))

App()