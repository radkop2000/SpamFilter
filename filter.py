import collections

import utils
from termcolor import colored
from corpus import Corpus
from html.parser import HTMLParser
import quality
import os

class MyFilter:

    def __init__(self):
        self.final_dict = {}

    def train(self, dir_path):
        final_dict = utils.get_final_dict(dir_path)
        print(list(collections.Counter(final_dict))[:-100])
        for i in final_dict:
            if i in self.final_dict:
                self.final_dict[i] = (self.final_dict[i] + final_dict[i]) / 2
            else:
                self.final_dict[i] = final_dict[i]

    #
    def test(self, dir_path):
        corpus = Corpus(dir_path)
        generator = corpus.emails()
        f = open(f"{dir_path}/!prediction.txt", "w")
        for file_name, email in generator:
            email = utils.preprocess_email(email)
            value = 1
            for word in email:
                if word in self.final_dict:
                    value *= self.final_dict[word]
            if value > 40000:
                f.write(f"{file_name} SPAM\n")
            else:
                f.write(f"{file_name} OK\n")




if __name__ == "__main__":
    filter = MyFilter()
    filter.train("data/3/3")
    # filter.train("data/3/")

    filter.test("data/1")
    print(quality.compute_quality_for_corpus(os.path.join("data", "1")))
