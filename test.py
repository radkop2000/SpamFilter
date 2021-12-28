import os
from io import StringIO
from html.parser import HTMLParser
import collections


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


def function(path, status):
    words = ['com', 'all', 'just', 'being', 'over', 'both', 'through', 'yourselves', 'its', 'before', 'herself', 'had', 'should', 'to', 'only', 'under', 'ours', 'has', 'do', 'them', 'his', 'very', 'they', 'not', 'during', 'now', 'him', 'nor', 'did', 'this', 'she', 'each', 'further', 'where', 'few', 'because', 'doing', 'some', 'are', 'our', 'ourselves', 'out', 'what', 'for', 'while', 'does', 'above', 'between', 't', 'be', 'we', 'who', 'were', 'here', 'hers', 'by', 'on', 'about', 'of', 'against', 's', 'or', 'own', 'into', 'yourself', 'down', 'your', 'from', 'her', 'their', 'there', 'been', 'whom', 'too', 'themselves', 'was', 'until', 'more', 'himself', 'that', 'but', 'don', 'with', 'than', 'those', 'he', 'me', 'myself', 'these', 'up', 'will', 'below', 'can', 'theirs', 'my', 'and', 'then', 'is', 'am', 'it', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', 'again', 'no', 'when', 'same', 'how', 'other', 'which', 'you', 'after', 'most', 'such', 'why', 'a', 'off', 'i', 'yours', 'so', 'the', 'having', 'once', 'net', 'org'
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
        if word not in words:
            finito2.append(word)
    # print(collections.Counter(finito3).most_common(20))
    ret = collections.Counter(finito2)
    return ret

truth = open("/Users/radovan/PycharmProjects/spam/spamfilter/data/1/!truth.txt", 'r')

spam = []
ham = []

for line in truth.readlines():
    flag = False
    name = ''
    status = ''
    for i in line:
        if flag:
            status += i
        elif i == ' ':
            flag = True
        else:
            name += i
    status = status[:-1]
    if status == "SPAM":
        spam.append(name)
    else:
        ham.append(name)

ratio = len(spam) / len(ham)
print(ratio)

spam_dict = function("data/1", spam)
ham_dict = function("data/1", ham)

final_dict = {}

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

final_dict2 = {}

for i in final_dict:
    if final_dict[i] != 1:
        final_dict2[i] = final_dict[i]


final_dict = {}
final_dict = final_dict2


print(sorted(final_dict.items()))




corps = Corpus("data/1")
generator = corps.emails(spam)

how_good = 0
count_emails = 0

for filename, emaill in generator:
    finish = []
    email = strip_tags(emaill)
    stripped_email = ""
    for i in email:
        if i in ['$', ' ', '@']:
            stripped_email += i
            continue
        if i.isalpha():
            stripped_email += i
    finish = stripped_email.split()
    value = 1
    for word in finish:
        if word in final_dict:
            value *= final_dict[word]
    if value > 40:
        how_good += 1
    count_emails+=1



print("i catched " ,how_good, " out of " ,count_emails, " spam emails.")
print("ratio: ", round((how_good/count_emails)*100, 2), "%")

corps = Corpus("data/1")
generator = corps.emails(ham)
how_good = 0
count_emails = 0

for filename, emaill in generator:
    finish = []
    email = strip_tags(emaill)
    stripped_email = ""
    for i in email:
        if i in ['$', ' ', '@']:
            stripped_email += i
            continue
        if i.isalpha():
            stripped_email += i
    finish = stripped_email.split()
    value = 1
    for word in finish:
        if word in final_dict:
            value *= final_dict[word]
            if final_dict[word] > 10:
                print(word, final_dict[word])
    if value > 1e+30:
        print(email)
    if value < 40:
        how_good += 1
    count_emails+=1

print("i catched " ,how_good, " out of " ,count_emails, " ham emails.")
print("ratio: ", round((how_good/count_emails)*100, 2), "%")


# print(function())

