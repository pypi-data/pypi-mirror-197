from readvalid import ReadFiles


class SetOperations(ReadFiles):

    def __init__(self, file1, file2):
        self.hm1 = self.read_file(file1)
        self.hm2 = self.read_file(file2)

    def union(self):
        hm = {**self.hm1, **self.hm2}
        return hm

    def intersection(self):
        hm = {}
        if len(self.hm1) < len(self.hm2):
            s, b = self.hm1, self.hm2
            for i in b:
                if i in s:
                    hm[i] = True
            return hm
        elif len(self.hm1) > len(self.hm2):
            s, b = self.hm1, self.hm2
            for i in b:
                if i in s:
                    hm[i] = True
            return hm

    def minus(self):
        hm = {}
        if len(self.hm1) < len(self.hm2):
            s, b = self.hm1, self.hm2
            for i in s:
                if i not in b:
                    hm[i] = True
            return hm
        elif len(self.hm1) > len(self.hm2):
            s, b = self.hm1, self.hm2
            for i in s:
                if i not in b:
                    hm[i] = True
            return hm
