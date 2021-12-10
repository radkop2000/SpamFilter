import os


def read_classification_from_file(file_path):
    dictionary = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            name, classification = line.split()
            dictionary[name] = classification
    return dictionary


def write_classification_to_file(dictionary, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for key in dictionary:
            file.write(key + ' ' + dictionary[key] + '\n')


if __name__ == "__main__":
    path = os.path.join("1", "!truth.txt")
    file_dict = read_classification_from_file(path)
    write_classification_to_file(file_dict, "!test.txt")
