import math

class Quaternion:

    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

        #self.normalize()

    def normalize(self):
        mag = math.sqrt(self.a*self.a + self.b*self.b + self.c*self.c + self.d*self.d)
        self.a = self.a / mag
        self.b = self.b / mag
        self.c = self.c / mag
        self.d = self.d / mag


    def get_mat3x3(self, angle):

        ang = angle * 3.1415926535897932384626433832795 / 180.0;

        self.a = math.cos(ang/2.0)
        self.b = self.b * math.sin(ang/2.0)
        self.c = self.c * math.sin(ang/2.0)
        self.d = self.d * math.sin(ang/2.0)

        self.normalize()

        a = self.a
        b = self.b
        c = self.c
        d = self.d

        q = []
        q.append([a*a+b*b-c*c-d*d, 2*b*c - 2*a*d, 2*a*c+2*b*d])
        q.append([2*a*d+2*b*c, a*a-b*b+c*c-d*d, 2*c*d-2*a*b])
        q.append([2*b*d-2*a*c, 2*a*b+2*c*d, a*a-b*b-c*c+d*d])

        return q



