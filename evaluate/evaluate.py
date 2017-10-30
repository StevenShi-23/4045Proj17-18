"""

    This program aims to find the precision, recall and f1 value of regular expression tokenizer.

    Usage: python evaluate.py test_file train_file

"""
import sys
import codecs
import re
from collections import Counter


def evaluate(test, train):
    true_positive = 0
    for token in train:
        if token not in test:
            continue
        else:
            true_positive += min(train[token], test[token])
    false_positive = sum(train.values()) - true_positive
    false_negative = sum(test.values()) - true_positive
    return true_positive / (true_positive+false_positive), true_positive / (true_positive + false_negative)


def main(test_path="../Training/posts_annotated.txt", train_path='../posts/posts_training_clean_codeAnno_textAnno.txt'):

    test_source = codecs.open(test_path, encoding='UTF-8').read()
    train_source = codecs.open(train_path, encoding='UTF-8').read()


    # regular expression to extract code and text token
    re_code = re.compile("<c>(.*?)</c>", flags = re.S|re.M)
    re_text = re.compile("<t>(.*?)</t>", flags = re.S|re.M)

    # regular expression to split each post
    re_post = re.compile('(\d+)\|(.*?)\n"', flags = re.S|re.M)

    # find all tokens in train and test
    train_tokens = re_text.findall(train_source) + re_code.findall(train_source)
    test_tokens = re_text.findall(test_source) + re_code.findall(test_source)

    # print(len(train_tokens))
    # print(len(test_tokens))

    # count token
    train_tokens_count = Counter(train_tokens)
    test_tokens_count = Counter(test_tokens)

    # compute precision
    precision, recall = evaluate(test_tokens_count, train_tokens_count)
    f1 = 2 * recall * precision / (recall + precision)
    print('Precision: ', precision)
    print('Recall:    ', recall)
    print('F1 score:  ', f1)


    # train_post_list = re_post.findall(train_source)
    # test_post_list = re_post.findall(test_source)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    else:
        test = sys.argv[1]
        train = sys.argv[2]
        main(test, train)