import os


class Corpus:

    def __init__(self, folder):
        self.folder = folder

    def emails(self):
        filenames = os.listdir(self.folder)
        for filename in filenames:
            if filename[0] == '!':
                continue
            with open(os.path.join(self.folder, filename), 'r', encoding='ISO-8859-1') as file:
                yield filename, file.read()

    def sorted_emails(self, status):
        filenames = os.listdir(self.folder)
        for filename in filenames:
            if filename[0] == '!':
                continue
            if filename not in status:
                continue
            with open(os.path.join(self.folder, filename), 'r', encoding='ISO-8859-1') as file:
                yield filename, file.read()


if __name__ == '__main__':
    cp = Corpus("1")
    generator = cp.emails()
    print(next(generator))
