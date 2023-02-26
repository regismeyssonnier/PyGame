

class Grid:

    def __init__(self):
        self.case = [0]*9

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