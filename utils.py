import os
from io import StringIO
from html.parser import HTMLParser
import collections


def read_classification_from_file(file_path):
    dictionary = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            name, classification = line.split()
            dictionary[name] = classification
    return dictionary

def get_emails(path, string):
    emails_dict = read_classification_from_file(path)
    target_emails = []
    for i in emails_dict:
        if emails_dict[i] == string:
            target_emails.append(i)
    return target_emails



def write_classification_to_file(dictionary, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for key in dictionary:
            file.write(key + ' ' + dictionary[key] + '\n')


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

class Corpus:

    def __init__(self, folder):
        self.folder = folder

    def emails(self, status):
        filenames = os.listdir(self.folder)
        for filename in filenames:
            if filename[0] == '!':
                continue
            if filename not in status:
                continue
            with open(os.path.join(self.folder, filename), 'r', encoding='utf-8') as file:
                yield filename, file.read()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def get_dict(path, status):
    empty_words = ['com', 'all', 'just', 'being', 'over', 'both', 'through', 'yourselves', 'its', 'before', 'herself', 'had', 'should', 'to', 'only', 'under', 'ours', 'has', 'do', 'them', 'his', 'very', 'they', 'not', 'during', 'now', 'him', 'nor', 'did', 'this', 'she', 'each', 'further', 'where', 'few', 'because', 'doing', 'some', 'are', 'our', 'ourselves', 'out', 'what', 'for', 'while', 'does', 'above', 'between', 't', 'be', 'we', 'who', 'were', 'here', 'hers', 'by', 'on', 'about', 'of', 'against', 's', 'or', 'own', 'into', 'yourself', 'down', 'your', 'from', 'her', 'their', 'there', 'been', 'whom', 'too', 'themselves', 'was', 'until', 'more', 'himself', 'that', 'but', 'don', 'with', 'than', 'those', 'he', 'me', 'myself', 'these', 'up', 'will', 'below', 'can', 'theirs', 'my', 'and', 'then', 'is', 'am', 'it', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', 'again', 'no', 'when', 'same', 'how', 'other', 'which', 'you', 'after', 'most', 'such', 'why', 'a', 'off', 'i', 'yours', 'so', 'the', 'having', 'once', 'net', 'org'
             , 'http', 'version', 'type', 'subject', 'www']
    fin = ""
    cp = Corpus(path)
    generator = cp.emails(status)
    finito3 = []
    for file_name, msg in generator:
        email = msg
        email = strip_tags(email)
        email = email.lower()
        for word in email.split():
            if '@' in word:
                finito3.append((word, file_name))
        stripped_email = ""
        for i in email:
            if i in ['$', ' ', '@']:
                stripped_email += i
                continue
            if not i.isalpha():
                i = ' '
            stripped_email += i
        fin += stripped_email
    finito = fin.split()
    finito2 = []
    for word in finito:
        if '@' in word:
            word = 'email'
        if '$' in word:
            word = 'dollar'
        if len(word) <= 2:
            continue
        if word not in empty_words:
            finito2.append(word)
    ret = collections.Counter(finito2)
    return ret


def get_final_dict(path):
    final_dict={}
    spam_list = get_emails(f"{path}/!truth.txt", "SPAM")
    ham_list = get_emails(f"{path}/!truth.txt", "OK")
    spam_dict = get_dict(path, spam_list)
    ham_dict = get_dict(path, ham_list)
    ratio = len(spam_list)/len(ham_list)
    for word in spam_dict:
        if word in ham_dict:
            final_dict[word] = (spam_dict[word] / ratio) / ham_dict[word]
        else:
            final_dict[word] = spam_dict[word]

    for word in ham_dict:
        if word not in final_dict:
            if word in spam_dict:
                final_dict[word] = (spam_dict[word] / ratio) / ham_dict[word]
            else:
                final_dict[word] = ham_dict[word] ** -1
    final_final_dict = {}
    for i in final_dict:
        if final_dict[i] != 1:
            final_final_dict[i] = final_dict[i]
    return final_final_dict




if __name__ == "__main__":
    # train
    e = get_final_dict("/Users/radovan/PycharmProjects/spam/spamfilter/data/1")
    # test





