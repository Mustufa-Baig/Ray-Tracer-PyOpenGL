import pygame
from OpenGL.GL import *
import numpy
import ctypes
from OpenGL.GL.shaders import compileShader,compileProgram

WIDTH,HEIGHT=700,400

class App:
	def __init__(self):
		pygame.init()
		pygame.display.set_mode((WIDTH,HEIGHT),pygame.OPENGL|pygame.DOUBLEBUF)
		self.clock=pygame.time.Clock()
		glClearColor(0.1,0.1,0.1,1)
		self.shader=self.createShader("shaders/vertex.txt","shaders/fragment.txt")
		glUseProgram(self.shader)

		#self.triangle=Triangle()
		self.quad=Quad()

		self.frame_count = 0
		self.fbos = glGenFramebuffers(2)
		self.textures = glGenTextures(2)

		for i in range(2):
			glBindFramebuffer(GL_FRAMEBUFFER, self.fbos[i])
			glBindTexture(GL_TEXTURE_2D, self.textures[i])
			glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, 700, 400, 0, GL_RGBA, GL_FLOAT, None)
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
			glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.textures[i], 0)

		glBindFramebuffer(GL_FRAMEBUFFER, 0)
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
		
		res_addr =glGetUniformLocation(self.shader,"u_resolution")
		frame_addr = glGetUniformLocation(self.shader, "u_frameCount")
		accum_tex_addr = glGetUniformLocation(self.shader, "u_accumTexture")

		while run:
			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					run=False

			read_idx = self.frame_count % 2
			write_idx = (self.frame_count + 1) % 2

			
			glBindFramebuffer(GL_FRAMEBUFFER, self.fbos[write_idx])

			glUseProgram(self.shader)
			
			glUniform2f(res_addr, WIDTH, HEIGHT)
			glUniform1f(frame_addr, float(self.frame_count))

			glActiveTexture(GL_TEXTURE0)
			glBindTexture(GL_TEXTURE_2D, self.textures[read_idx])
			glUniform1i(accum_tex_addr, 0)

			
			glBindVertexArray(self.quad.vao)
			glDrawArrays(GL_TRIANGLES, 0, self.quad.vertex_count)

			
			glBindFramebuffer(GL_READ_FRAMEBUFFER, self.fbos[write_idx])
			glBindFramebuffer(GL_DRAW_FRAMEBUFFER, 0)
			glBlitFramebuffer(0, 0, 700, 400, 0, 0, 700, 400, GL_COLOR_BUFFER_BIT, GL_NEAREST)


			
			glBindVertexArray(self.quad.vao)
			glDrawArrays(GL_TRIANGLES, 0, self.quad.vertex_count)

			pygame.display.flip()
			self.frame_count+=1
			self.clock.tick(60)

		#self.triangle.destroy()
		self.quad.destroy()
		glDeleteProgram(self.shader)
		glDeleteFramebuffers(2, self.fbos)
		glDeleteTextures(2, self.textures)
		pygame.quit()


class Quad:
    def __init__(self):
        # Two triangles forming a quad
        self.vertices = numpy.array([
            # pos               # color
            -1.0, -1.0, 0.0,     1.0, 1.0, 0.0,
             1.0, -1.0, 0.0,     0.0, 1.0, 1.0,
             1.0,  1.0, 0.0,     1.0, 0.0, 1.0,

            -1.0, -1.0, 0.0,     1.0, 1.0, 0.0,
             1.0,  1.0, 0.0,     1.0, 0.0, 1.0,
            -1.0,  1.0, 0.0,     0.0, 1.0, 0.0,
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