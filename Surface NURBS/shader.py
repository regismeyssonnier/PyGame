# coding=utf-8
import pygame
import time 
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.ARB.framebuffer_object import *
from OpenGL.GL.EXT.framebuffer_object import *

#--------------------[(+)] WARNING [(+)] ------------------------------------
class Shader:


	def __init__(self, b):
		self.vertexShader = 0
		self.fragShader = 0

		self.frag_source = """
		
		varying vec4 vColor;
		void main(){
			gl_FragColor = vColor ;
		
		 
		}"""
	
		frag_source2 = """
	
		varying vec4 vColor;
		void main(){
			gl_FragColor = gl_Color;
		 
		}"""		
			
	
		self.vertex_source="""//varying vec3 v;
		//varying vec3 N;
		attribute vec4 c;
		attribute vec4 vert;
		varying vec4 vColor;

		void main(void)
		{

			//v = gl_ModelViewMatrix * gl_Vertex;
			//N = gl_NormalMatrix * gl_Normal;
			gl_PointSize = 10;
			gl_Position = gl_ModelViewProjectionMatrix * vert;
			gl_FrontColor = gl_Color;
			vColor = c;
			// gl_TexCoord[0]=gl_TextureMatrix[0] * gl_MultiTexCoord0;
		}
		"""

		if b:
			self.shader = [self.vertexShader, self.vertex_source, self.fragShader, self.frag_source]
			self.v_program = self.Create_Shader()

	def set_new_shader(self, verts, frags):
		self.vertexShader = 0
		self.fragShader = 0
		self.frag_source = frags
		self.vertex_source = verts
		self.shader = [self.vertexShader, self.vertex_source, self.fragShader, self.frag_source]
		self.v_program = self.Create_Shader()


	def Create_Shader(self):
		self.shader[0] = glCreateShader(GL_VERTEX_SHADER)

		source = self.shader[1]
		glShaderSource(self.shader[0], source)

		glCompileShader(self.shader[0]);
		status = glGetShaderiv(self.shader[0], GL_COMPILE_STATUS)
		#print (glGetShaderInfoLog(shader[0]))

		self.shader[2] = glCreateShader(GL_FRAGMENT_SHADER)

		source = self.shader[3]
		glShaderSource(self.shader[2], source)

		glCompileShader(self.shader[2]);
		status = glGetShaderiv(self.shader[2], GL_COMPILE_STATUS)
		#print (glGetShaderInfoLog(shader[1]))
	
		v_program=glCreateProgram()
		glAttachShader(v_program,self.shader[0])
		glAttachShader(v_program,self.shader[2])
		glLinkProgram(v_program)
	
		print("vprog" + str(v_program))
		return v_program

	def get_v_program(self):
		return self.v_program

	def use_program(self):
		try:
			glUseProgram(self.v_program)   
		except OpenGL.error.GLError:
			print (glGetProgramInfoLog(self.v_program))
			print (glGetShaderInfoLog(self.vertexShader))
			raise
		
	def print_vf(self):
		print(self.frag_source)
		print(self.vertex_source)
	


	
#--------------------[(+)] END WARNING [(+)] ------------------------------------