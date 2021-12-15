import utils
from termcolor import colored

class MyFilter:

    def __init__(self):
        self.final_dict = {}

    def train(self, dir_path):
        final_dict = utils.get_final_dict(dir_path)
        for i in final_dict:
            if i in self.final_dict:
                self.final_dict[i] *= final_dict[i]
            else:
                self.final_dict[i] = final_dict[i]

    def test(self, dir_path):
        pass

if __name__ == "__main__":
    filter = MyFilter()
    filter.train("data/1")
    print(colored(filter.final_dict, "green"))
    filter2 = MyFilter()
    filter2.train("data/2")
    print(colored(filter2.final_dict, "blue"))
    filter.train("data/2")
    print(colored(filter.final_dict, "red"))