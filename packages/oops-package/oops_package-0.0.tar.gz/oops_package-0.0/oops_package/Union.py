from readvalid import *
from operations import *
from parsearg import *
import sys, time


class ResultFile:
    def __init__(self, file3, func):
        self.file3 = file3
        self.func = func

    def return_file(self):
        with open(self.file3, 'w') as file:
            definition = self.func()
            for i in definition:
                file.write(i)
        with open(self.file3, 'r') as file:
            line = file.readlines()
            return line


if __name__ == "__main__":
    try:
        args = Args(file1, file2).arg_parse()
        if len(sys.argv) == 4:
            start_time = time.time()
            operations = SetOperations(sys.argv[1], sys.argv[2])
            functions = [operations.union, operations.intersection, operations.minus]
            if sys.argv[0] == "Union.py":
                h3 = ResultFile(sys.argv[3], functions[0]).return_file()
            elif sys.argv[0] == "Intersection.py":
                h3 = ResultFile(sys.argv[3], functions[1]).return_file()
            elif sys.argv[0] == "Minus.py":
                h3 = ResultFile(sys.argv[3], functions[2]).return_file()
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Output: {sys.argv[1]}: {len(operations.hm1)} emails, {sys.argv[2]}: {len(operations.hm2)} emails, {sys.argv[3]}: {len(h3)} emails; Time taken: {int(elapsed_time)} seconds")
        else:
            raise IndexError
    except IndexError:
        print("Arguments Validation Failed", "\n", "use syntax like: '<set-operation>.py L1.txt L2.txt R.txt'")