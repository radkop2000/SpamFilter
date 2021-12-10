import os
import utils
import confmat


def quality_score(tp, tn, fp, fn):
    score = (tp + tn)/(tp + tn + 10*fp + fn)
    return score


def compute_quality_for_corpus(path):
    truth_dict = utils.read_classification_from_file(
        os.path.join(path, '!truth.txt'))
    pred_dict = utils.read_classification_from_file(
        os.path.join(path, '!prediction.txt'))
    cm = confmat.BinaryConfusionMatrix(pos_tag='SPAM', neg_tag='OK')
    cm.compute_from_dicts(truth_dict, pred_dict)
    return quality_score(**cm.as_dict())


if __name__ == "__main__":
    compute_quality_for_corpus(os.path.join("data", "1"))
