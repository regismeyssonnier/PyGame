

class Grid:

    def __init__(self):
        self.case = [0]*9

    def set_case(self, case):
        for i in range(9):
            self.case[i] = case[i]

    def get_case_occupied(self, i):
        return self.case[i]

    def set_case_occupied(self, i, type):
        self.case[i] = type

    def _test_case(self, num):
        if self.case[0] == num and self.case[1] == num and self.case[2] == num:
            return 1
        if self.case[3] == num and self.case[4] == num and self.case[5] == num:
            return 1
        if self.case[6] == num and self.case[7] == num and self.case[8] == num:
            return 1
        if self.case[0] == num and self.case[3] == num and self.case[6] == num:
            return 1
        if self.case[1] == num and self.case[4] == num and self.case[7] == num:
            return 1
        if self.case[2] == num and self.case[5] == num and self.case[8] == num:
            return 1
        if self.case[0] == num and self.case[4] == num and self.case[8] == num:
            return 1
        if self.case[2] == num and self.case[4] == num and self.case[6] == num:
            return 1

        return 0


    def test_nullmatch(self):
        nullmatch = 1
        for i in range(9):
            if self.case[i] == 0:
                nullmatch = 0
        return nullmatch
 
    def analyze_grid(self):
        p1 = self._test_case(1)
        p2 = self._test_case(2)
        nullmatch = self.test_nullmatch()
        if p1: return 1
        if p2: return 2
        if nullmatch: return 3
        return -1

    def get_score(self, type):
        score = 0
        for i in range(3):
            c= 1
            for j in range(3):
                if self.case[i*3+j] == type:
                    c*=2

            score += c

        for j in range(3):
            c= 1
            for i in range(3):
                if self.case[i*3+j] == type:
                    c*=2

            score += c

        j = 0
        for i in range(3):
            c = 1
            if self.case[i*3+j] == type:
                    c*=2

            score += c
            j+=1

        j = 3
        for i in range(3):
            c = 1
            if self.case[i*3+j] == type:
                    c*=2

            score += c
            j-=1

        return score

    def get_score_def(self, typea):
        score = 0
        id = -1
        for i in range(3):
            c= 0
            empty = 0
            for j in range(3):
                if self.case[i*3+j] == typea:
                    empty = 1
                    id = i*3+j
                    c+=1

            if c == 2:
                score += 10000

        for j in range(3):
            c= 0
            empty = 0
           
            for i in range(3):
              
                if self.case[i*3+j] == typea:
                    empty = 1
                    id = i*3+j
                    c+=1

            if c == 2:
                score += 10000

        j = 0
        empty = 0
        c=0
        for i in range(3):
            
            if self.case[i*3+j] == typea:
                empty = 1
                id = i*3+j
                c+=1
                            
            j+=1
        if c == 2:
            score += 10000

        j = 3
        empty = 0
        c=0
        for i in range(3):
           
            if self.case[i*3+j] == typea:
                empty = 1
                id = i*3+j
                c+=1
            
            j-=1

        if c == 2:
                score += 10000

        return score


    def get_copy(self, c):
        for i in range(9):
            c.append(self.case[i])

    def get_full(self):
        full = 1
        for i in range(9):
            if self.case[i] == 0:
                full = 0

        return full

    def get_possible_move(self, indice):
        
        for i in range(9):
            if self.case[i] == 0:
                indice.append(i)

        return indice

    def display(self):
        s = ""
        for i in range(3):
            s=""
            for j in range(3):
                s += str(self.case[i*3+j])
            print (s)