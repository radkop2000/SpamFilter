import utils
from corpus import Corpus


class MyFilter:

    def __init__(self):
        self.word_ratio_dict = utils.read_training_from_file("learned.txt")
        self.boundary = 5000

    def train(self, dir_path):
        final_dict = utils.get_final_dict(dir_path)
        for i in final_dict:
            if i in self.word_ratio_dict:
                self.word_ratio_dict[i] = (self.word_ratio_dict[i] + final_dict[i]) / 2
            else:
                self.word_ratio_dict[i] = final_dict[i]

    def test(self, dir_path):
        corpus = Corpus(dir_path)
        generator = corpus.emails()
        f = open(f"{dir_path}/!prediction.txt", "w", encoding="utf-8")
        for file_name, email in generator:
            email = utils.preprocess_email(email)
            value = 1
            for word in email:
                if word in self.word_ratio_dict:
                    value *= self.word_ratio_dict[word]
            if value > self.boundary:
                f.write(f"{file_name} SPAM\n")
            else:
                f.write(f"{file_name} OK\n")
        f.close()
