from io import StringIO
from html.parser import HTMLParser
import collections
import corpus

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

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def function():
    words = ['com', 'all', 'just', 'being', 'over', 'both', 'through', 'yourselves', 'its', 'before', 'herself', 'had', 'should', 'to', 'only', 'under', 'ours', 'has', 'do', 'them', 'his', 'very', 'they', 'not', 'during', 'now', 'him', 'nor', 'did', 'this', 'she', 'each', 'further', 'where', 'few', 'because', 'doing', 'some', 'are', 'our', 'ourselves', 'out', 'what', 'for', 'while', 'does', 'above', 'between', 't', 'be', 'we', 'who', 'were', 'here', 'hers', 'by', 'on', 'about', 'of', 'against', 's', 'or', 'own', 'into', 'yourself', 'down', 'your', 'from', 'her', 'their', 'there', 'been', 'whom', 'too', 'themselves', 'was', 'until', 'more', 'himself', 'that', 'but', 'don', 'with', 'than', 'those', 'he', 'me', 'myself', 'these', 'up', 'will', 'below', 'can', 'theirs', 'my', 'and', 'then', 'is', 'am', 'it', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', 'again', 'no', 'when', 'same', 'how', 'other', 'which', 'you', 'after', 'most', 'such', 'why', 'a', 'off', 'i', 'yours', 'so', 'the', 'having', 'once']
    fin = ""
    cp = corpus.Corpus("data/1")
    generator = cp.emails()
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
        if len(word) <= 2:
            continue
        if word not in words:
            finito2.append(word)
    print(collections.Counter(finito3).most_common(10))


    ret = collections.Counter(finito2).most_common(50)
    return ret

print(function())



