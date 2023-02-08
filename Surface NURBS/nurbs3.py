from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.ARB.framebuffer_object import *
from OpenGL.GL.EXT.framebuffer_object import *
import random
import math
from trigo import *
from quaternion import *
from trackball import *
from shader import *


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
        self.shader = 0
        self.normal = []

        self.pt_normal =[]
        self.color_n = []
        self.indices_n = []

    def set_event(self, event):
        self.trackball.set_event(event)

    def set_active_trackball(self, a):
        self.trackball.set_active(a)

    def set_mouse_keyboard(self, a, k):
        self.trackball.set_mouse_keyboard(a, k)
        self.mouse = a
        self.keyboard = k

    def create_shader(self):
        self.shader =  Shader(False)

        frag_source = """
		varying vec3 N;
		varying vec4 vColor;
        varying vec4 v;
		void main(){
            vec3 normal = normalize(vec3(N.x, N.y, N.z));
            //gl_LightSource[0].position.xyz
            vec3 L = normalize(vec3(0.0, 0.5, 5.5) - vec3(v.x, v.y, v.z));
            vec3 L2 = normalize(vec3(0.0, 4.0, 0.0) - vec3(v.x, v.y, v.z));
            vec3 L3 = normalize(vec3(5.5, 0.5, -1.5) - vec3(v.x, v.y, v.z));
            vec3 L4 = normalize(vec3(-2.5, 0.5, -1.5) - vec3(v.x, v.y, v.z));
            vec3 E = normalize(-v);  
            vec3 R = normalize(-reflect(L,N));

            float distance = length(L);

            float angl = dot(N, L);

            vec3 specular = pow(dot(N, L), 50.0) * vec3(1.0, 0.0, 1.0);
            specular = max(specular, 0.0);

            vec3 specular2 = pow(dot(N, L2), 10.0) * vec3(1.0, 1.0, 1.0);
            specular2 = max(specular2, 0.0);

            vec3 specular3 = pow(dot(N, L3), 10.0) * vec3(1.0, 0.0, 1.0);
            specular3 = max(specular3, 0.0);

            vec3 specular4 = pow(dot(N, L4), 10.0) * vec3(1.0, 0.0, 1.0);
            specular4 = max(specular4, 0.0);

            float ambientStrength = 0.2;
            vec4 ambient = ambientStrength * vColor;

            float ambientStrength2 = 0.1;
            vec4 ambient2 = ambientStrength2 * vColor;

            float ambientStrength3 = 0.1;
            vec4 ambient3 = ambientStrength3 * vColor;

            float ambientStrength4 = 0.1;
            vec4 ambient4 = ambientStrength4 * vColor;

            float diff = max(dot(N, L), 0.0);
            vec4 diffuse = diff * vColor;
            diffuse = clamp(diffuse, 0.0, 1.0);
            vec4 res = (ambient + diffuse + vec4(specular.xyz, 1.0) );
            res = clamp(res, 0.0, 1.0);

            float diff2 = max(dot(N, L2), 0.0);
            vec4 diffuse2 = diff2 * vColor;
            diffuse2 = clamp(diffuse2, 0.0, 1.0);
            vec4 res2 = (ambient2 + diffuse2 + vec4(specular2.xyz, 1.0) );
            res2 = clamp(res2, 0.0, 1.0);

            float diff3 = max(dot(N, L3), 0.0);
            vec4 diffuse3 = diff3 * vColor;
            diffuse3 = clamp(diffuse3, 0.0, 1.0);
            vec4 res3 = (ambient3 + diffuse3+ vec4(specular3.xyz, 1.0) );
            res3 = clamp(res3, 0.0, 1.0);

            float diff4 = max(dot(N, L4), 0.0);
            vec4 diffuse4 = diff4 * vColor;
            diffuse4 = clamp(diffuse4, 0.0, 1.0);
            vec4 res4 = (ambient4 + diffuse4 + vec4(specular4.xyz, 1.0) );
            res2 = clamp(res4, 0.0, 1.0);
                                    
            
            /*if(res.r <= 0.4 && res.g <= 0.4 && res.b <= 0.4){
                res = vColor;
                res.a = 1.0;
            }*/
            //vec4 res = vColor;
            
            //res *= vec4(vColor.xyz+E.xyz, 1.0);
			gl_FragColor = clamp(res*0.5+res2+res4+res3, 0.0, 1.0) ;
		
		 
		}"""
	
	
	
        vertex_source="""
        attribute vec3 n;
        varying vec3 N;
        attribute vec4 c;
        attribute vec4 vert;
        varying vec4 v;
        varying vec4 vColor;
        
		void main(void)
		{

			//v = gl_ModelViewMatrix * gl_Vertex;
			//N = gl_NormalMatrix * gl_Normal;
            N = n;//vec3(0.0, 1.0, 0.0);
            v = vec4(gl_ModelViewMatrix * vert);
            //v = vert;
			gl_PointSize = 10;
			gl_Position = gl_ModelViewProjectionMatrix * vert;
			gl_FrontColor = gl_Color;
			vColor = c;
			// gl_TexCoord[0]=gl_TextureMatrix[0] * gl_MultiTexCoord0;
		}
		"""

        self.shader.set_new_shader(vertex_source, frag_source)
        


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

    def update_pos_line_normal_curve(self, diff_t):
        if(not self.trackball.get_update()):
            return
        vectq = self.trackball.get_vector()

        self.quat = Quaternion(0.0, vectq.x, vectq.y, vectq.z)

        if self.mouse:
            ln = len(self.pt_normal)

            x = 0.0
            y = 0.0
            z = 0.0
            i=0
            c = 0
            while i < ln:
                x += self.pt_normal[i]
                #y += self.point_c[i+1]
                z += self.pt_normal[i+2]
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
                self.pt_normal[i+2] -= -1.6
                i+=3
   
        rot = self.quat.get_mat3x3(self.trackball.get_angle()*(diff_t * 0.1 / 100))
        i = 0
            
        rVert = []
        lnp = len(self.pt_normal)
        while i  < lnp:
	        for y in  range(3):
		        r = 0
		        for x in range(3):
			        r += rot[y][x] * self.pt_normal[i+x]

		        rVert.append(r);
	        i += 3
                            
            
        if self.mouse:
            ln = len(self.pt_normal)
                       
            i=0
            while i < ln:
                #print(self.point_c[self.indices_ptc[i]*3+2])
                #rVert[i] += x
                #rVert[i+1] += y
                rVert[i+2] += -1.6
                i+=3
                    
        self.pt_normal = rVert;

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

    def add_color_n(self, r, g, b, a):
        self.color_n.append(r)
        self.color_n.append(g)
        self.color_n.append(b)
        self.color_n.append(a)

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

        #self.point_c[1] += 1.8
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
        """for i in range(len(self.pt_curve)):
            print(str(i) + " "+ str(self.pt_curve[i]))"""

    def compute_normal(self):
        lnp = len(self.pt_curve)
        x=0.0
        y=0.0
        z=0.0
        i=0
        while i < lnp:
            x+=self.pt_curve[i]
            y+=self.pt_curve[i+1]
            z+=self.pt_curve[i+2]
            i+=3
        x /= (lnp/3)
        y /= (lnp/3)
        z /= (lnp/3)

        c = Point3(x, y, z)
        
        ln = int(len(self.pt_curve));
        for i in range(ln/3):
            self.normal.append(1.0)
            self.normal.append(1.0)
            self.normal.append(1.0)

        nb_line = int(0.8/self.steps)
        i = 0
        indn = 0
        ind = 0
        while i < nb_line-1:
            ind = (i * 3 * nb_line)
            for j in range(nb_line-1):

                #print(i)
                p1 = Point3(self.pt_curve[ind], self.pt_curve[ind+1], self.pt_curve[ind+2])
                p2 = Point3(self.pt_curve[ind+3], self.pt_curve[ind+4], self.pt_curve[ind+5])
                p22 = Point3(self.pt_curve[ind+nb_line*3], self.pt_curve[ind+nb_line*3+1], self.pt_curve[ind+nb_line*3+2])
                ind+=3
                #p1 = Point3(p1.x+1000.0, p1.y+1000.0, p1.z+1000.0)
                #p2 = Point3(p2.x+1000.0, p2.y+1000.0, p2.z+1000.0)
                #p22 = Point3(p22.x+1000.0, p22.y+1000.0, p22.z+1000.0)
                pp = Point3(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)
                pq = Point3(p22.x - p1.x, p22.y - p1.y, p22.z - p1.z)
                ppn = normalize3(pp)
                pqn = normalize3(pq)
                p3 = cross3(ppn, pqn)
                p4 = cross3(pqn, ppn)
                #print("p3" + str(p3.x)  + " " + str(p3.y) + " " + str(p3.z))
                #print("p4" + str(p4.x)  + " " + str(p4.y) + " " + str(p4.z))

                p5 = Point3(p1.x + p3.x/10.0, p1.y + p3.y/10.0, p1.z + p3.z/10.0)
                p6 = Point3(p1.x + p4.x/10.0, p1.y + p4.y/10.0, p1.z + p4.z/10.0)

                d1 = distance3(p5, c)
                d2 = distance3(p6, c)
                #print("dist" + str(i)  + " " + str(d1) + " " + str(d2))

                if d1 < d2:
                    self.normal[ind] =p4.x
                    self.normal[ind+1] =p4.y
                    self.normal[ind+2] =p4.z
                else:
                    self.normal[ind] = p3.x
                    self.normal[ind+1] = p3.y
                    self.normal[ind+2] = p3.z
            i+=1

        i = 0

        lnn = len(self.normal)
        while i < lnn:
            
            p = Point3(self.normal[i], self.normal[i+1], self.normal[i+2])
            pn = normalize3(p)
            self.normal[i] = pn.x
            self.normal[i+1] = pn.y
            self.normal[i+2] = pn.z

            print(str(self.normal[i]) + " " + str(self.normal[i+1]) + " " + str(self.normal[i+2]))
            i+=3
            

        print(lnp)
        print(len(self.indices_t))
        print(lnn)

    def create_line_normal(self):

        ln = len(self.normal)
        ind = 0
        i = 0;
        while i < ln:
            self.pt_normal.append(self.pt_curve[i]  )
            self.pt_normal.append(self.pt_curve[i+1]  )
            self.pt_normal.append(self.pt_curve[i+2] )
            self.indices_n.append(ind)
            self.add_color_n(1.0, 0.0, 0.0, 1.0)
            ind += 1
            self.pt_normal.append(self.pt_curve[i] + self.normal[i]/10.0  )
            self.pt_normal.append(self.pt_curve[i+1] + self.normal[i+1]/10.0 )
            self.pt_normal.append(self.pt_curve[i+2] + self.normal[i+2]/10.0 )
            self.indices_n.append(ind)
            self.add_color_n(1.0, 0.0, 0.0, 1.0)
            ind += 1


            i+=3


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
                #if alt:
                self.add_color_t(1.0, 1.0, 0.0, 1.0)
                self.add_color_t(1.0, 1.0, 0.0, 1.0)
                """else:
                    self.add_color_t(0.0, 1.0, 1.0, 1.0)
                    self.add_color_t(0.0, 1.0, 1.0, 1.0)"""
                self.indices_t.append(ind+nb_line)
                #if not alt:
                self.add_color_t(1.0, 1.0, 0.0, 1.0)
                #else:
                 #   self.add_color_t(0.0, 1.0, 1.0, 1.0)

                self.indices_t.append(ind+1)
                self.indices_t.append(ind+nb_line+1)
                """if alt:
                    self.add_color_t(0.0, 1.0, 1.0, 1.0)
                    self.add_color_t(0.0, 1.0, 1.0, 1.0)
                else:"""
                self.add_color_t(1.0, 1.0, 0.0, 1.0)
                self.add_color_t(1.0, 1.0, 0.0, 1.0)
                    
                self.indices_t.append(ind+nb_line)
                """if not alt:
                    self.add_color_t(0.0, 1.0, 1.0, 1.0)
                else:"""
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

    def use_program(self):
        self.shader.use_program()

    def draw_triangle_curve(self):
        v_program = self.shader.get_v_program()
        
        normalatt = glGetAttribLocation(v_program, "n")
        color = glGetAttribLocation(v_program, "c")
        verticesatt = glGetAttribLocation(v_program, "vert")
        #print("normlalatt" + str(color)) 
        #print(self.shader.print_vf())
        
        nbo = 0
        glGenBuffers(1,nbo)

        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, nbo)
        glVertexAttribPointer(normalatt, 3, GL_FLOAT, GL_FALSE, 0, self.normal)
        glEnableVertexAttribArray(normalatt)
        
        cbo = 0
        glGenBuffers(1,cbo)
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, cbo)
        glVertexAttribPointer(color, 4, GL_FLOAT, GL_FALSE, 0, self.color_t)
        glEnableVertexAttribArray(color)

        fbo = 0
        glGenBuffers(1,fbo)
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, fbo)
        glVertexAttribPointer(verticesatt, 3, GL_FLOAT, GL_FALSE, 0, self.pt_curve)
        glEnableVertexAttribArray(verticesatt)
       
        glDrawElements(GL_TRIANGLES, len(self.indices_t),  GL_UNSIGNED_INT, self.indices_t)

    def draw_triangle_normal(self):
        v_program = self.shader.get_v_program()
        
        #normalatt = glGetAttribLocation(v_program, "n")
        color = glGetAttribLocation(v_program, "c")
        verticesatt = glGetAttribLocation(v_program, "vert")
        #print("normlalatt" + str(color)) 
        #print(self.shader.print_vf())
        
        """nbo = 0
        glGenBuffers(1,nbo)

        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, nbo)
        glVertexAttribPointer(normalatt, 3, GL_FLOAT, GL_FALSE, 0, self.normal)
        glEnableVertexAttribArray(normalatt)"""
        
        cbo = 0
        glGenBuffers(1,cbo)
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, cbo)
        glVertexAttribPointer(color, 4, GL_FLOAT, GL_FALSE, 0, self.color_n)
        glEnableVertexAttribArray(color)

        fbo = 0
        glGenBuffers(1,fbo)
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, fbo)
        glVertexAttribPointer(verticesatt, 3, GL_FLOAT, GL_FALSE, 0, self.pt_normal)
        glEnableVertexAttribArray(verticesatt)
       
        glDrawElements(GL_LINES, len(self.indices_n),  GL_UNSIGNED_INT, self.indices_n)

