from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.ARB.framebuffer_object import *
from OpenGL.GL.EXT.framebuffer_object import *
import random
import math
from trigo import *
from quaternion import *
from trackball import *



class Nurbs3:

    def __init__(self, k, tu, tv, ptc, st, w, wi, h):
        self.k = k
        self.tu = tu
        self.tv = tv
        self.point_c = ptc
        self.steps = st
        self.w = w
        self.size_quad = 1.0
        self.nb_quadsx = 3
        self.nb_quadsz = 3
        self.indices_ptc = []
        self.color_ptc = []
        self.v_program = 0
        self.trackball = Trackball(wi, h)
        self.trackball.set_active(True)
        self.quat = Quaternion(0.0, 0.0, 0.0, 1.0)
        self.mouse = False
        self.keyboard = True
        self.pt_curve = []
        self.indices_ptcu = []
        self.color_ptcu = []

        self.pt_line = []
        self.indices_l = []
        self.color_l = []

        self.indices_t = []
        self.color_t = []

    def set_event(self, event):
        self.trackball.set_event(event)

    def set_active_trackball(self, a):
        self.trackball.set_active(a)

    def set_mouse_keyboard(self, a, k):
        self.trackball.set_mouse_keyboard(a, k)
        self.mouse = a
        self.keyboard = k

    def update_pos_point_c(self, diff_t):
        if(not self.trackball.get_update()):
            return
        vectq = self.trackball.get_vector()

        self.quat = Quaternion(0.0, vectq.x, vectq.y, vectq.z)

        if self.mouse:
            ln = len(self.point_c)

            x = 0.0
            y = 0.0
            z = 0.0
            i=0
            c = 0
            while i < ln:
                x += self.point_c[i]
                #y += self.point_c[i+1]
                z += self.point_c[i+2]
                i+=3
                c+=1

            
            #x /= c
            #y /= c
            z /= c
            #print(str(x) + " "+ str(y) + " " + str(z) +"")
            
            i=0
            while i < ln:
                #print(self.point_c[self.indices_ptc[i]*3+2])
                #self.point_c[i] -= x
                #self.point_c[i+1] -= y
                self.point_c[i+2] -= -1.6
                i+=3
   
        rot = self.quat.get_mat3x3(self.trackball.get_angle()*(diff_t * 0.1 / 100))
        i = 0
            
        rVert = []
        lnp = len(self.point_c)
        while i  < lnp:
	        for y in  range(3):
		        r = 0
		        for x in range(3):
			        r += rot[y][x] * self.point_c[i+x]

		        rVert.append(r);
	        i += 3
                            
            
        if self.mouse:
            ln = len(self.point_c)
                       
            i=0
            while i < ln:
                #print(self.point_c[self.indices_ptc[i]*3+2])
                #rVert[i] += x
                #rVert[i+1] += y
                rVert[i+2] += -1.6
                i+=3
                    
        self.point_c = rVert;

    def update_pos_point_curve(self, diff_t):
        if(not self.trackball.get_update()):
            return
        vectq = self.trackball.get_vector()

        self.quat = Quaternion(0.0, vectq.x, vectq.y, vectq.z)

        if self.mouse:
            ln = len(self.pt_curve)

            x = 0.0
            y = 0.0
            z = 0.0
            i=0
            c = 0
            while i < ln:
                x += self.pt_curve[i]
                #y += self.point_c[i+1]
                z += self.pt_curve[i+2]
                i+=3
                c+=1

            
            #x /= c
            #y /= c
            z /= c
            #print(str(x) + " "+ str(y) + " " + str(z) +"")
            
            i=0
            while i < ln:
                #print(self.point_c[self.indices_ptc[i]*3+2])
                #self.point_c[i] -= x
                #self.point_c[i+1] -= y
                self.pt_curve[i+2] -= -1.6
                i+=3
   
        rot = self.quat.get_mat3x3(self.trackball.get_angle()*(diff_t * 0.1 / 100))
        i = 0
            
        rVert = []
        lnp = len(self.pt_curve)
        while i  < lnp:
	        for y in  range(3):
		        r = 0
		        for x in range(3):
			        r += rot[y][x] * self.pt_curve[i+x]

		        rVert.append(r);
	        i += 3
                            
            
        if self.mouse:
            ln = len(self.pt_curve)
                       
            i=0
            while i < ln:
                #print(self.point_c[self.indices_ptc[i]*3+2])
                #rVert[i] += x
                #rVert[i+1] += y
                rVert[i+2] += -1.6
                i+=3
                    
        self.pt_curve = rVert;

    def cox_de_boor(self, k, t, i, u):
        #k degre
        #t vecteur nodaux
        #index
        #point d'evaluation
        if k == 0:
            if t[i] <= u < t[i+1]:
                return 1
            else:
                return 0
        else:
            denom1 = t[i+k] - t[i]
            if denom1 == 0:
                c1 = 0
            else:
                c1 = (u - t[i]) / denom1 * self.cox_de_boor(k-1, t, i, u)
        
            denom2 = t[i+k+1] - t[i+1]
            if denom2 == 0:
                c2 = 0
            else:
                c2 = (t[i+k+1] - u) / denom2 * self.cox_de_boor(k-1, t, i+1, u)
        
            return c1 + c2

    def add_color_ptc(self, r, g, b, a):
        self.color_ptc.append(r)
        self.color_ptc.append(g)
        self.color_ptc.append(b)
        self.color_ptc.append(a)

    def add_color_ptcu(self, r, g, b, a):
        self.color_ptcu.append(r)
        self.color_ptcu.append(g)
        self.color_ptcu.append(b)
        self.color_ptcu.append(a)

    def add_color_l(self, r, g, b, a):
        self.color_l.append(r)
        self.color_l.append(g)
        self.color_l.append(b)
        self.color_l.append(a)

    def add_color_t(self, r, g, b, a):
        self.color_t.append(r)
        self.color_t.append(g)
        self.color_t.append(b)
        self.color_t.append(a)

    def create_grid_base(self):

        xi = -1.0;
        yi = -0.15
        zi = -1.6
        inter = 0.5
        interz = 0.2
        ind = 0
        for i in range(self.nb_quadsx+1):
            xi = -1.0;
            for j in range(self.nb_quadsz+1):
                self.point_c.append(xi)
                self.point_c.append(yi)
                self.point_c.append(zi)
                self.indices_ptc.append(ind)
                ind += 1
                self.add_color_ptc(1.0, 0.0, 0.0, 1.0)
                xi += inter

            zi += interz

        self.point_c[16] += 0.8
        self.point_c[19] += 0.8
        self.point_c[28] += 0.8
        self.point_c[31] += 0.8


    def compute(self):

        self.pt_curve = []
        u = 0.1
        mu = self.nb_quadsx+1
        mv = self.nb_quadsz+1
        nu = self.k
        nv = self.k
        ind = 0
        alt = True
        while u <= 0.9:
            v = 0.1
            
            while v <= 0.9:
                rx = 0.0
                ry = 0.0
                rz = 0.0
                rdx = 0.0
                
                for i in range(mu):
                    for j in range(mv):
                        ni = float(self.cox_de_boor(nu, self.tu, i, u))
                        nj = float(self.cox_de_boor(nv, self.tv, j, v))
                        #print("ind " + str(i*mv + j) )
                        rx += ni * nj * self.w[i*mv+j] * self.point_c[(i*mv + j)*3 ]
                        ry += ni * nj * self.w[i*mv+j] * self.point_c[(i*mv + j)*3 + 1]
                        rz += ni * nj * self.w[i*mv+j] * self.point_c[(i*mv + j)*3 + 2]
                        rdx += ni * nj * self.w[i*mv+j]
                
                v += self.steps
                
                if rdx != 0.0 and (rx != 0.0 and ry != 0.0 and rz != 0.0):
                    """self.pt_curve.append(rx)
                    self.pt_curve.append(ry)
                    self.pt_curve.append(rz)
                else:"""
                    self.pt_curve.append(rx/rdx)
                    self.pt_curve.append(ry/rdx)
                    self.pt_curve.append(rz/rdx)
                    self.indices_ptcu.append(ind)
                    ind+=1
                    if alt:
                        self.add_color_ptcu(0.0, 1.0, 0.0, 1.0)
                    else:
                        self.add_color_ptcu(0.0, 0.0, 1.0, 1.0)

                    alt = not alt   

                

            u += self.steps

        print("len ptcurve " + str(len(self.pt_curve)))
        for i in range(len(self.pt_curve)):
            print(str(i) + " "+ str(self.pt_curve[i]))

    def create_line(self):
        i = 0
        nb_line = int(0.8/self.steps)
        ind = 0
        alt = True
        for i in range(nb_line):

            for j in range(nb_line):
                self.indices_l.append(ind)
                if j %2 == 1 and j < nb_line-1:   
                    self.indices_l.append(ind)
                    self.indices_l.append(ind+1)
                ind+=1
                if alt:
                    self.add_color_l(0.0, 1.0, 0.0, 1.0)
                else:
                    self.add_color_l(0.0, 0.0, 1.0, 1.0)

                alt = not alt  

        alt = True
        ind = 0
        ln = len(self.indices_l)
        indc = 0
        for j in range(nb_line):
            ind = j
            for i in range(nb_line):
                self.indices_l.append(ind)
                if i %2 == 1 and i < nb_line-1:   
                    self.indices_l.append(ind)
                    id = ind + nb_line
                    if(id >= j+nb_line*nb_line):
                        id = j
                    #if id >= ln:
                     #   id = j
                    self.indices_l.append(id)
                ind+=nb_line
                #if(ind >= ln):
                #        ind = j
                if alt:
                    self.add_color_l(1.0, 1.0, 0.0, 1.0)
                else:
                    self.add_color_l(0.0, 1.0, 1.0, 1.0)

                alt = not alt

        #for i in range(len(self.indices_l)):
         #   print(self.indices_l[i])

    def create_triangle(self):
        nb_line = int(0.8/self.steps)
        ind = 0
        alt = True
        for i in range(nb_line-1):
            ind = i * nb_line
            for j in range(nb_line-1):
                self.indices_t.append(ind)
                self.indices_t.append(ind+1)
                if alt:
                    self.add_color_t(1.0, 1.0, 0.0, 1.0)
                    self.add_color_t(1.0, 1.0, 0.0, 1.0)
                else:
                    self.add_color_t(0.0, 1.0, 1.0, 1.0)
                    self.add_color_t(0.0, 1.0, 1.0, 1.0)
                self.indices_t.append(ind+nb_line)
                if not alt:
                    self.add_color_t(1.0, 1.0, 0.0, 1.0)
                else:
                    self.add_color_t(0.0, 1.0, 1.0, 1.0)

                self.indices_t.append(ind+1)
                self.indices_t.append(ind+nb_line+1)
                if alt:
                    self.add_color_t(0.0, 1.0, 1.0, 1.0)
                    self.add_color_t(0.0, 1.0, 1.0, 1.0)
                else:
                    self.add_color_t(1.0, 1.0, 0.0, 1.0)
                    self.add_color_t(1.0, 1.0, 0.0, 1.0)
                    
                self.indices_t.append(ind+nb_line)
                if not alt:
                    self.add_color_t(0.0, 1.0, 1.0, 1.0)
                else:
                    self.add_color_t(1.0, 1.0, 0.0, 1.0)
                    
                ind += 1

            


    def draw_point_control(self, v_program):
              
        self.v_program = v_program
        
        color = glGetAttribLocation(self.v_program, "c")
        verticesatt = glGetAttribLocation(self.v_program, "vert")

        fbo = 0
        glGenBuffers(1,fbo)
        cbo = 0
        glGenBuffers(1,cbo)

        
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, cbo)
        glVertexAttribPointer(color, 4, GL_FLOAT, GL_FALSE, 0, self.color_ptc)
        glEnableVertexAttribArray(color)

       
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, fbo)
        glVertexAttribPointer(verticesatt, 3, GL_FLOAT, GL_FALSE, 0, self.point_c)
        glEnableVertexAttribArray(verticesatt)
       
        glDrawElements(GL_POINTS, len(self.indices_ptc),  GL_UNSIGNED_INT, self.indices_ptc)


    def draw_pt_curve(self, v_program):
              
        self.v_program = v_program
        
        color = glGetAttribLocation(self.v_program, "c")
        verticesatt = glGetAttribLocation(self.v_program, "vert")

        fbo = 0
        glGenBuffers(1,fbo)
        cbo = 0
        glGenBuffers(1,cbo)

        
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, cbo)
        glVertexAttribPointer(color, 4, GL_FLOAT, GL_FALSE, 0, self.color_ptcu)
        glEnableVertexAttribArray(color)

       
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, fbo)
        glVertexAttribPointer(verticesatt, 3, GL_FLOAT, GL_FALSE, 0, self.pt_curve)
        glEnableVertexAttribArray(verticesatt)
       
        glDrawElements(GL_POINTS, len(self.indices_ptcu),  GL_UNSIGNED_INT, self.indices_ptcu)

    def draw_line_curve(self, v_program):
              
        self.v_program = v_program
        
        color = glGetAttribLocation(self.v_program, "c")
        verticesatt = glGetAttribLocation(self.v_program, "vert")

        fbo = 0
        glGenBuffers(1,fbo)
        cbo = 0
        glGenBuffers(1,cbo)

        
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, cbo)
        glVertexAttribPointer(color, 4, GL_FLOAT, GL_FALSE, 0, self.color_l)
        glEnableVertexAttribArray(color)

       
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, fbo)
        glVertexAttribPointer(verticesatt, 3, GL_FLOAT, GL_FALSE, 0, self.pt_curve)
        glEnableVertexAttribArray(verticesatt)
       
        glDrawElements(GL_LINES, len(self.indices_l),  GL_UNSIGNED_INT, self.indices_l)


    def draw_triangle_curve(self, v_program):
              
        self.v_program = v_program
        
        color = glGetAttribLocation(self.v_program, "c")
        verticesatt = glGetAttribLocation(self.v_program, "vert")

        fbo = 0
        glGenBuffers(1,fbo)
        cbo = 0
        glGenBuffers(1,cbo)

        
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, cbo)
        glVertexAttribPointer(color, 4, GL_FLOAT, GL_FALSE, 0, self.color_t)
        glEnableVertexAttribArray(color)

       
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, fbo)
        glVertexAttribPointer(verticesatt, 3, GL_FLOAT, GL_FALSE, 0, self.pt_curve)
        glEnableVertexAttribArray(verticesatt)
       
        glDrawElements(GL_TRIANGLES, len(self.indices_t),  GL_UNSIGNED_INT, self.indices_t)



