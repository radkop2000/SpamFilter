import os
from io import StringIO
from html.parser import HTMLParser
import collections
import corpus


def read_classification_from_file(file_path):
    dictionary = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            name, classification = line.split()
            dictionary[name] = classification
    return dictionary


def read_training_from_file(file_path):
    dictionary = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            name, classification = line.split(" ")
            dictionary[name] = float(classification)
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
            file.write(key + ' ' + str(dictionary[key]) + '\n')


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


def get_dict(path, status):
    fin = []
    cp = corpus.Corpus(path)
    generator = cp.sorted_emails(status)
    for fname, email in generator:
        e = preprocess_email(email)
        for i in range(len(e)):
            fin.append(e[i])
    # print(collections.Counter(fin).most_common(50))
    return collections.Counter(fin)


def preprocess_email(email):
    email = strip_tags(email)
    empty_words = ['com', 'all', 'just', 'being', 'over', 'both', 'through', 'yourselves', 'its', 'before', 'herself',
                   'had', 'should', 'to', 'only', 'under', 'ours', 'has', 'do', 'them', 'his', 'very', 'they', 'not',
                   'during', 'now', 'him', 'nor', 'did', 'this', 'she', 'each', 'further', 'where', 'few', 'because',
                   'doing', 'some', 'are', 'our', 'ourselves', 'out', 'what', 'for', 'while', 'does', 'above',
                   'between', 't', 'be', 'we', 'who', 'were', 'here', 'hers', 'by', 'on', 'about', 'of', 'against', 's',
                   'or', 'own', 'into', 'yourself', 'down', 'your', 'from', 'her', 'their', 'there', 'been', 'whom',
                   'too', 'themselves', 'was', 'until', 'more', 'himself', 'that', 'but', 'don', 'with', 'than',
                   'those', 'he', 'me', 'myself', 'these', 'up', 'will', 'below', 'can', 'theirs', 'my', 'and', 'then',
                   'is', 'am', 'it', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', 'again', 'no', 'when',
                   'same', 'how', 'other', 'which', 'you', 'after', 'most', 'such', 'why', 'a', 'off', 'i', 'yours',
                   'so', 'the', 'having', 'once', 'net', 'org', 'http', 'version', 'type', 'subject', 'mon', 'tue',
                   'wed', 'thu', 'fri', 'sat', 'sun', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep',
                   'oct', 'nov', 'dec']
    prefixes = ['un']
    suffixes = ['less', 'es', 's', 'ship', 'ing', 'les', 'ly']
    words = []

    for word in email.split():
        word = word.lower()
        if "@" in word:
            word = 'email'
        elif "//" in word or "www" in word:
            word = "hypertext"
        elif "$" in word:
            word = "dollar"
        if not word.isalpha():
            for i in word:
                if not i.isalpha():
                    word = word.replace(i, ' ', 1)
        if len(word) <= 2:
            continue
        elif word in empty_words:
            continue
        for suffix in suffixes:
            word = remove_suffix(word, suffix)
        for prefix in prefixes:
            word = remove_prefix(word, prefix)
        for i in word.split():
            if len(i) <= 2:
                continue
            if i in empty_words:
                continue
            for suffix in suffixes:
                i = remove_suffix(i, suffix)
            for prefix in prefixes:
                i = remove_prefix(i, prefix)
            words.append(i)
    return words


def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string


def remove_prefix(input_string, prefix):
    if input_string.startswith(prefix):
        return input_string[len(prefix):]
    return input_string
#


def get_final_dict(path):
    final_dict = {}
    spam_list = get_emails(f"{path}/!truth.txt", "SPAM")
    ham_list = get_emails(f"{path}/!truth.txt", "OK")
    spam_dict = get_dict(path, spam_list)
    ham_dict = get_dict(path, ham_list)
    ratio = len(spam_list)/len(ham_list)
    for word in spam_dict:
        if word in ham_dict:
            final_dict[word] = round(
                (spam_dict[word] / ratio) / ham_dict[word], 4)
        else:
            final_dict[word] = round(spam_dict[word], 4)

    for word in ham_dict:
        if word not in final_dict:
            if word in spam_dict:
                final_dict[word] = round(
                    (spam_dict[word] / ratio) / ham_dict[word], 4)
            else:
                final_dict[word] = round(ham_dict[word] ** -1, 4)
    final_final_dict = {}
    for i in final_dict:
        if final_dict[i] != 1:
            final_final_dict[i] = final_dict[i]
    return final_final_dict


if __name__ == "__main__":
    # train
    e = get_final_dict("/Users/radovan/PycharmProjects/spam/spamfilter/data/1")
    # test
