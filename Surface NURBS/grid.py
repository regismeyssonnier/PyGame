# coding=utf-8
import pygame
import time 
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.ARB.framebuffer_object import *
from OpenGL.GL.EXT.framebuffer_object import *
import random
import math
from trigo import *
from quaternion import *
from trackball import *


class Grid:

    def __init__(self, lr, lg, nbg, w, h):
        self.largeur = lr
        self.longueur = lg
        self.nb_quad = nbg
        self.line = []
        self.vertices = []
        self.indices = []
        self.colors = []
        self.nb_lines = 20
        self.size = 0.1*self.nb_lines
        self.v_program = 0
        self.Create_grid()
        self.trackball = Trackball(w, h)
        self.trackball.set_active(True)
        self.quat = Quaternion(0.0, 0.0, 0.0, 1.0)

    def add_color(self, r, g, b, a):
        self.colors.append(r)
        self.colors.append(g)
        self.colors.append(b)
        self.colors.append(a)

    def set_event(self, event):
        self.trackball.set_event(event)

    def set_active_trackball(self, a):
        self.trackball.set_active(a)

    def set_mouse_keyboard(self, a, k):
        self.trackball.set_mouse_keyboard(a, k)

    def Create_grid(self):

        xi = -1.0;
        yi = -0.25
        zi = -1.6
        inter = 0.1
        ind = 0
        """self.add_color(0.0, 0.0, 1.0, 1.0)
        self.add_color(0.0, 0.0, 1.0, 1.0)
        self.add_color(0.0, 0.0, 1.0, 1.0)
        self.add_color(0.0, 0.0, 1.0, 1.0)"""
        for i in range(self.nb_lines):
            #print(i)
            self.vertices.append(xi)
            self.vertices.append(yi)
            self.vertices.append(zi)
            xi += self.size
            self.vertices.append(xi)
            self.vertices.append(yi)
            self.vertices.append(zi)
            """self.vertices.append(xi)
            self.vertices.append(yi)
            self.vertices.append(zi+0.05)"""
            self.indices.append(ind)
            self.indices.append(ind+1)
            #self.indices.append(ind+2)
            self.add_color(0.5, 0.5, 0.7, 1.0)
            self.add_color(0.5, 0.5, 0.7, 1.0)
            #self.add_color(1.0, 0.0, 0.0, 1.0)
            xi -= self.size
            zi += inter
            ind += 2
            

        xi = -1.0
        yi = -0.25
        zi = -1.6
        for i in range(self.nb_lines):
            print(i)
            self.vertices.append(xi)
            self.vertices.append(yi)
            self.vertices.append(zi)
            zi += self.size
            self.vertices.append(xi)
            self.vertices.append(yi)
            self.vertices.append(zi)
            """self.vertices.append(xi+0.05)
            self.vertices.append(yi)
            self.vertices.append(zi)"""
            self.indices.append(ind)
            self.indices.append(ind+1)
            #self.indices.append(ind+2)
            self.add_color(0.5, 0.5, 0.7, 1.0)
            self.add_color(0.5, 0.5, 0.7, 1.0)
            #self.add_color(0.0, 0.0, 1.0, 1.0)
            zi -= self.size
            xi += inter
            ind += 2

        i = 0
        while i < (8*3):
            print(str(i) + " "+str(self.vertices[i]) + " " + str(self.vertices[i+1]) + " " + str(self.vertices[i+2]))
            i+=3

        """i = 0
        while i < len(self.indices):
            print(str(self.indices[i]) + " " + str(self.indices[i+1])+ " " + str(self.indices[i+2]))
            i+=3"""

    def Update_pos(self, diff_t):
        if(not self.trackball.get_update()):
            return
        vectq = self.trackball.get_vector()

        self.quat = Quaternion(0.0, vectq.x, vectq.y, vectq.z)

        x = 0
        y = 0
        z = 0
        for i in range(3):
            x += self.vertices[self.indices[i]*3]
            y += self.vertices[self.indices[i]*3+1]
            z += self.vertices[self.indices[i]*3+2]
        #print(str(x) + " " + str(y) + " " + str(z))
        x /= 3.0
        y /= 3.0
        z /= 3.0
        #for i in range(3):
	        #self.vertices[self.indices[i]*3] -= x
	        #self.vertices[self.indices[i]*3+1] -= y
            #self.vertices[self.indices[i]*3+2] -= -1.5

        #print(str(x) + " " + str(y) + " " + str(z))
        rot = self.quat.get_mat3x3(self.trackball.get_angle()*(diff_t * 0.1 / 100))
        i = 0
        ln = len(self.vertices)
        rVert = []
        while i  < ln:
	        for y in  range(3):
		        r = 0
		        for x in range(3):
			        r += rot[y][x] * self.vertices[i+x]

		        rVert.append(r);
	        i += 3

        #for i in range(3):
	        #rVert[vIndices[i]*3] += x
	        #rVert[vIndices[i]*3+1] += y
	        #rVert[self.indices[i]*3+2] += -1.5

        self.vertices = rVert;



    def Draw(self, v_program):

        self.v_program = v_program
        
        color = glGetAttribLocation(self.v_program, "c")
        verticesatt = glGetAttribLocation(self.v_program, "vert")

        fbo = 0
        glGenBuffers(1,fbo)
        cbo = 0
        glGenBuffers(1,cbo)

        
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, cbo)
        glVertexAttribPointer(color, 4, GL_FLOAT, GL_FALSE, 0, self.colors)
        glEnableVertexAttribArray(color)

        #self.vertices = [0.0, 0.25, 0.0, 1.1, 0.25, 0.0, 0.0, -0.25, -1.5, 1.0, -0.25, -1.5, 0.0, 1.0, 0.0, 1.1, 1.0, 0.0, 0.0, 0.6, -1.5, 1.0, 1.0, -1.5]
	
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, fbo)
        glVertexAttribPointer(verticesatt, 3, GL_FLOAT, GL_FALSE, 0, self.vertices)
        glEnableVertexAttribArray(verticesatt)
        #self.indices = [57,58,59]


        glDrawElements(GL_LINES, len(self.indices),  GL_UNSIGNED_INT, self.indices)
