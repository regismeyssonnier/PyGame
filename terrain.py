from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.ARB.framebuffer_object import *
from OpenGL.GL.EXT.framebuffer_object import *
from Bande import *

import pygame
import time
import numpy
import math

pygame.init()

dis_width=1700
dis_height=800

dis2 = pygame.display.set_mode((dis_width, dis_height))
dis = pygame.display.set_mode((dis_width,dis_height), pygame.OPENGL|pygame.DOUBLEBUF)


score_font = pygame.font.SysFont("comicsansms", 35)

blue = (0, 0, 255)
red = (255, 0, 0)
dark_red = (120, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
g70 = (70, 70, 70)
yellow = (255, 255, 102)
green = (0, 255, 0)
purple = (200, 0, 255)
cyan = (0, 120, 255)
gray = (50, 50, 50)

clock = pygame.time.Clock()
game_speed = 120

def FPS(t):
	t = t * 0.12
	value = score_font.render("fps : " + str(t) , True, yellow)
	dis2.blit(value, [0, 0]) 
	
def Create_Shader(shader):
	shader[0] = glCreateShader(GL_VERTEX_SHADER)

	source = shader[1]
	glShaderSource(shader[0], source)

	glCompileShader(shader[0]);
	status = glGetShaderiv(shader[0], GL_COMPILE_STATUS)
	#print (glGetShaderInfoLog(shader[0]))

	shader[2] = glCreateShader(GL_FRAGMENT_SHADER)

	source = shader[3]
	glShaderSource(shader[2], source)

	glCompileShader(shader[2]);
	status = glGetShaderiv(shader[2], GL_COMPILE_STATUS)
	#print (glGetShaderInfoLog(shader[1]))
	
	v_program=glCreateProgram()
	glAttachShader(v_program,shader[0])
	glAttachShader(v_program,shader[2])
	glLinkProgram(v_program)
	
	return v_program
	
	
def Rotation_Y(v, a):
	
	ry = [math.cos(a*math.pi/180), 0, math.sin(a*math.pi/180),   0, 1, 0,  -math.sin(a*math.pi/180), 0, math.cos(a*math.pi/180)]
	vv = []
	
	for i in range(0, len(v), 3):
		vv.append(ry[0] * v[i] + ry[1] * v[i+1] + ry[2] * v[i+2])
		vv.append(ry[3] * v[i] + ry[4] * v[i+1] + ry[5] * v[i+2])
		vv.append(ry[6] * v[i] + ry[7] * v[i+1] + ry[8] * v[i+2])
		
	for i in range(0, len(v)):
		v[i] = vv[i]
	 
def Translate(v, x, y, z):

	vv = []
	for i in range(0, len(v), 3):
		vv.append(v[i] + x)
		vv.append(v[i+1] + y)
		vv.append(v[i+2] + z)
		
	for i in range(0, len(v)):
		v[i] = vv[i]
		
def centre(v):
	c = []
	x = 0
	y = 0
	z = 0
	for i in range(0, len(v), 3):
		x += v[i] 
		y += v[i+1] 
		z += v[i+2]
		
	cx = x / len(v)
	cy = y / len(v)
	cz = z / len(v)	
	
	for i in range(0, len(v), 3):
		v[i] -= cx
		v[i+1] -= cy
		v[i+2] -= cz
		
	c.append(cx)
	c.append(cy)
	c.append(cz)
	
	return c
	
def add_centre(v, c):
	for i in range(0, len(v), 3):
		v[i] += c[0]
		v[i+1] += c[1]
		v[i+2] += c[2]
			
		
def bande(x, y, z, vVertices, vIndices, vColors, vi):
	
	I = len(vIndices)	
	vv = [x, y+1.0, z, x+1.0, y+1.0, z,    x, y+1.0, z-0.5,   x+1.0, y+1.0, z-0.5]
	for v in vv:
		vVertices.append(v)
	
	
	for v in vi:
		vIndices.append(v)
	
	vc = [0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0]
	for v in vc:
		vColors.append(v)
	
	alter = False
	
	y += 0.0
	z -= 0.5
	for i in range(2):
		vVertices.append(x)
		vVertices.append(y+1.0)
		vVertices.append(z-0.5)
		vVertices.append(x+1.0)
		vVertices.append(y+1.0)
		vVertices.append(z-0.5)
		for j in range(I, I+6):
			vIndices.append(vIndices[j]+2)
			if alter == False:
				vColors.append(0.0)
				vColors.append(1.0)
				vColors.append(0.0)
				vColors.append(1.0)
				alter = True
			else:
				vColors.append(0.0)
				vColors.append(0.5)
				vColors.append(0.0)
				vColors.append(1.0)
				alter = False
				
		y += 0.0
		z -= 0.5
		I += 6
		
	return I + 12
	


	

def gameLoop():
	game_over = False
	
	angle = 0
	
	"""fbo = 0
	glGenBuffers(1,fbo)
	cbo = 0
	glGenBuffers(1,cbo)
	ibo = 0
	glGenBuffers(1,ibo)"""
	
	frag_source = """
		
	varying vec4 vColor;
	void main(){
		gl_FragColor = vColor ;
		
		 
	}"""
	
	frag_source2 = """
	
	varying vec4 vColor;
	void main(){
		gl_FragColor = gl_Color;
		 
	}"""		
			
	
	vertex_source="""//varying vec3 v;
	//varying vec3 N;
	attribute vec4 c;
	attribute vec4 vert;
	varying vec4 vColor;

	void main(void)
	{

	   //v = gl_ModelViewMatrix * gl_Vertex;
	   //N = gl_NormalMatrix * gl_Normal;

	   gl_Position = gl_ModelViewProjectionMatrix * vert;
	   gl_FrontColor = gl_Color;
	   vColor = c;
	  // gl_TexCoord[0]=gl_TextureMatrix[0] * gl_MultiTexCoord0;
	}
	"""
	
	lines = []	
	line = []
	line2 = []
	li = []
	
	x = 0
	y = 0
	z = 0
	"""vVertices = []
	vIndices = []
	vColors = []"""
	
	"""vi = [0, 1, 2, 1, 2, 3]
	i = bande(x, y, z, vVertices, vIndices, vColors, vi)
	print(len(vVertices))
	#print(i)
	i = len(vIndices)
	for i in vIndices:
		print( i)"""
	#, Bande(x+1.0, y, z, 20)

	b = [Bande(x, y, z, 20)]
	x+= 1.0
	y = 0.0
	z = 0.0
	
	for i in range(20):
		b.append(Bande(x, y, z, 20))
		x += 1.0
		
	
	
	alt = True
	for ba in b:
		ba.Create(alt)
		if alt == True:
			alt = False
		else:
			alt = True
			
	nb = 0	
	for ba in b:
		nb += len(ba.Get_buffer_V())
	print(nb)
	
	b[0].Set_color([0.0, 0.0, 0.0, 1.0])
	b[3].Set_color([1.0, 0.0, 0.0, 1.0])
	
	h = 0.0
	hmax = 6.0
	nmax = 22
	h2 = 0.2
	I = 0
	hh = 0.0
	hh2 = h2
	for ii in range(len(b)):
		j = 0
		k = 0
		#c = centre(ba.Get_buffer_V())
		for i in range(22):
			ind = b[ii].Get_buffer_I()
			v = b[ii].Get_buffer_V()
			v[k*(6)+4] += math.cos(h)*2.0 #droite
			v[j*(6)+1] += math.cos(h2)*2.0#gauche
			h += math.sin(k / math.pi )  *0.1
			h2 += math.sin(j / math.pi)  *0.1
			k += 1
			j += 1 
		
		#add_centre(ba.Get_buffer_V(), c)
		hh -= 0.2
		hh2 -= 0.2
		h =  hh
		h2 = hh2
		 		
		
		
	#v = b[0].Get_buffer_V()	
	#v[0*(6)+4] =15.0
	
	
	"""vi = [i, i+1, i+2, i+1, i+2, i+3]
	bande(x+3.0, y+1.0, z, vVertices, vIndices, vColors, vi)
	print(len(vVertices))
	for i in vIndices:
		print( i)"""
	
	x1_change = 0
	y1_change = 0
	#size
	x1 = dis_width / 2
	y1 = dis_height / 2
	Z = -3
	Z_speed = 0.1
	Z_change = 0
	
	X = 0
	X_speed = 0.1
	X_change = 0
	
	Y = 0
	Y_speed = 0.1
	Y_change = 0
	
	angle = 0.0 
	angle_speed = 1.0
	angle_change = 0  
	
	""" Keyboard """
	d_up = False
	d_down = False
	d_left = False
	d_right = False
	d_dgright = False
	d_dgleft = False
	d_high = False
	d_low = False
	k_space = False
	mb_down = False
	k_b = False
	k_i = False
	
	fps = 0
		
	while not game_over:
	
		for event in pygame.event.get():
			#print(event)
			if event.type == pygame.QUIT:
				game_over = True
			
			if event.type == pygame.KEYDOWN:				
				if event.key == pygame.K_KP4:
					d_left = True
					d_right = False
					angle_change = -angle_speed
						
				elif event.key == pygame.K_KP6:
					d_right = True
					d_left = False
					angle_change = angle_speed
						
				elif event.key == pygame.K_KP9:
					d_dgright = True
					d_dgleft = False
					X_change = -X_speed
					
				elif event.key == pygame.K_KP7:
					d_dgleft = True
					d_dgright = False
					X_change = X_speed
					
				elif event.key == pygame.K_KP1:
					d_high = True
					d_low = False
					Y_change = -Y_speed
					
				elif event.key == pygame.K_KP3:
					d_low = True
					d_high = False
					Y_change = Y_speed
					
				elif event.key == pygame.K_KP8:
					d_up = True
					d_down = False
					Z_change = Z_speed
						
				elif event.key == pygame.K_KP5:
					d_down = True
					d_up = False
					Z_change = -Z_speed
					
				elif event.key == pygame.K_SPACE:
					k_space = True
					
				elif event.key == pygame.K_b:
					k_b = True
					
				elif event.key == pygame.K_i:
					k_i = True
										
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_KP4:
					d_left = False
						
				elif event.key == pygame.K_KP6:
					d_right = False
					
				elif event.key == pygame.K_KP9:
					d_dgright = False
										
				elif event.key == pygame.K_KP7:
					d_dgleft = False
					
				elif event.key == pygame.K_KP1:
					d_high = False
										
				elif event.key == pygame.K_KP3:
					d_low = False
																
				elif event.key == pygame.K_KP8:
					d_up = False
						
				elif event.key == pygame.K_KP5:
					d_down = False
					
				elif event.key == pygame.K_SPACE:
					k_space = False
					
				elif event.key == pygame.K_b:
					k_b = False
					
				elif event.key == pygame.K_i:
					k_i = False

		if d_up == True or d_down == True:
			Z = Z_change
			
		if d_dgleft == True or d_dgright == True:
			X = X_change
			
		if d_high == True or d_low == True:
			Y = Y_change
			
		if d_left == True or d_right == True:
			angle = angle_change
			
		glEnable(GL_DEPTH_TEST)
		glClearColor(0.0, 0.0, 0.5, 1.0)
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		
		glMatrixMode(GL_PROJECTION)
		glViewport(0, 0, dis_width, dis_height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(45, (dis_width / dis_height), 0.1, 500.0)
		glMatrixMode (GL_MODELVIEW)
		glLoadIdentity()

		#vVertices = (0.0,  0.5, 0.0, -0.5, -0.5, 0.0, 0.5, -0.5,  0.0);
		#vColors = (0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0)
		#vIndices = [0, 1, 2];
		#vIndices = numpy.array([0, 1, 2], dtype='int32')
					
				
		vertexShader = 0
		fragShader = 0
		shader = [vertexShader, vertex_source, fragShader, frag_source]
		v_program = Create_Shader(shader)
		
		for ba in b:
			ba.Set_program(v_program)
		try:
			glUseProgram(v_program)   
		except OpenGL.error.GLError:
			print glGetProgramInfoLog(v_program)
			print (glGetShaderInfoLog(vertexShader))
			raise

		color = glGetAttribLocation(v_program, "c")
		vertices = glGetAttribLocation(v_program, "vert")
	
		
		
		"""if d_left == True or d_right == True:
			Rotation_Y(vVertices, angle)
		
		#glTranslatef(0,0,-3)
		#glRotatef(angle, 0.0, 1.0, 0.0)
		if d_high == True or d_low == True:
			Translate(vVertices, 0, Y, 0)
		if d_dgleft == True or d_dgright == True:
			Translate(vVertices, X, 0, 0)
		if d_up == True or d_down == True:
			Translate(vVertices, 0, 0, Z)
		#glTranslatef(0,0,Z)
		#print(Z)"""
		
		if d_left == True or d_right == True:
			for ba in b:
				Rotation_Y(ba.Get_buffer_V(), angle)
		
		#glTranslatef(0,0,-3)
		#glRotatef(angle, 0.0, 1.0, 0.0)
		if d_high == True or d_low == True:
			for ba in b:
				Translate(ba.Get_buffer_V(), 0, Y, 0)
		if d_dgleft == True or d_dgright == True:
			for ba in b:
				Translate(ba.Get_buffer_V(), X, 0, 0)
		if d_up == True or d_down == True:
			for ba in b:
				Translate(ba.Get_buffer_V(), 0, 0, Z)
		
		"""glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, cbo)
		glVertexAttribPointer(color, 4, GL_FLOAT, GL_FALSE, 0, vColors)
		glEnableVertexAttribArray(color)
				
		glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, fbo)
		glVertexAttribPointer(vertices, 3, GL_FLOAT, GL_FALSE, 0, vVertices)
		glEnableVertexAttribArray(vertices)
		
		
		glDrawElements(GL_TRIANGLES, len(vIndices),  GL_UNSIGNED_INT, vIndices)"""
		for ba in b:
			ba.Draw()
		
		FPS(fps)
	    
		pygame.display.flip()
		fps = clock.tick(game_speed)
		
		

gameLoop()

