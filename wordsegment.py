# -*- coding: utf-8 -*-

"""
English Word Segmentation in Python

Word segmentation is the process of dividing a phrase without spaces back
into its constituent parts. For example, consider a phrase like "thisisatest".
For humans, it's relatively easy to parse. This module makes it easy for
machines too. Use `segment` to parse a phrase into its parts:

>>> from wordsegment import segment
>>> segment('thisisatest')
['this', 'is', 'a', 'test']

In the code, 1024908267229 is the total number of words in the corpus. A
subset of this corpus is found in unigrams.txt and bigrams.txt which
should accompany this file. A copy of these files may be found at
http://norvig.com/ngrams/ under the names count_1w.txt and count_2w.txt
respectively.

Copyright (c) 2015 by Grant Jenks

Based on code from the chapter "Natural Language Corpus Data"
from the book "Beautiful Data" (Segaran and Hammerbacher, 2009)
http://oreilly.com/catalog/9780596157111/

Original Copyright (c) 2008-2009 by Peter Norvig
"""

import sys
from os.path import join, dirname, realpath
from math import log10
from functools import wraps
from datetime import datetime
import bisect
import pcfg
from wordsegment_pcfg import segment_method2
LIMIT = 24
MIN = -sys.float_info.max
if sys.hexversion < 0x03000000:
    range = xrange

def parse_file(filename):
    "Read `filename` and parse tab-separated file of (word, count) pairs."
    with open(filename) as fptr:
        lines = (line.split('\t') for line in fptr)
        return dict((word, float(number)) for word, number in lines)

basepath = join(dirname(realpath(__file__)), 'wordsegment_data')
unigram_counts = parse_file(join(basepath, 'unigrams.txt'))
bigram_counts = parse_file(join(basepath, 'bigrams.txt'))
max_bigram_prob = {}
def divide(text, limit=LIMIT):
    """
    Yield `(prefix, suffix)` pairs from `text` with `len(prefix)` not
    exceeding `limit`.
    """
    for pos in range(1, min(len(text), limit) + 1):
        yield (text[:pos], text[pos:])

def unigram_score(word):
    if word in unigram_counts:
        
        # Probability of the given word.
        
        return unigram_counts[word] / 1024908267229.0
    else:
        # Penalize words not found in the unigrams according
        # to their length, a crucial heuristic.
            
        return 10.0 / (1024908267229.0 * 10 ** len(word))

def bigram_score(word, prev=None):
    if prev is None:
        return None

    bigram = '{0} {1}'.format(prev, word)

    if bigram in bigram_counts and prev in unigram_counts:
        return bigram_counts[bigram] / 1024908267229.0 / score(prev)
    else:
        return None

def linear_interpolation(word, prev, lambda1, lambda2):
    #if bigram_score(word,prev) is None or prev is None:
    #    return unigram_score(word)
    #else:
    return lambda1*score(word)+lambda2*score(word,prev)

def score(word, prev=None):
    "Score a `word` in the context of the previous word, `prev`."

    if prev is None:
        if word in unigram_counts:

            # Probability of the given word.

            return unigram_counts[word] / 1024908267229.0
        else:
            # Penalize words not found in the unigrams according
            # to their length, a crucial heuristic.

            return 10.0 / (1024908267229.0 * 10 ** len(word))
    else:
        bigram = '{0} {1}'.format(prev, word)

        if bigram in bigram_counts and prev in unigram_counts and word in unigram_counts:

            # Conditional probability of the word given the previous
            # word. The technical name is *stupid backoff* and it's
            # not a probability distribution but it works well in
            # practice.
            return bigram_counts[bigram] / 1024908267229.0 / score(prev)
        else:
            # Fall back to using the unigram probability.

            return score(word)


def clean(text):
    "Return `text` lower-cased with non-alphanumeric characters removed."
    alphabet = set('abcdefghijklmnopqrstuvwxyz0123456789')
    return ''.join(letter for letter in text.lower() if letter in alphabet)

def clean1(text):
    "Return `text` lower-cased with non-alphanumeric characters removed."
    alphabet = set('abcdefghijklmnopqrstuvwxyz0123456789.')
    return ''.join(letter for letter in text.lower() if letter in alphabet)

def clean2(text):
    "Return `text` lower-cased with non-alphanumeric characters removed."
    alphabet = set('abcdefghijklmnopqrstuvwxyz0123456789. ')
    return ''.join(letter for letter in text.strip().lower() if letter in alphabet)

def make_score_max():
    max_bigram_prob = {}
    for key in bigram_counts:
        prev = key.split()[0]+" "+key.split()[1][0]
        if prev not in max_bigram_prob:
            max_bigram_prob[prev] = bigram_counts[key]
        else:
            max_bigram_prob[prev] = max(bigram_counts[key], max_bigram_prob[prev])

    for prev in max_bigram_prob:
        max_bigram_prob[prev] = max_bigram_prob[prev] / 1024908267229.0/ score(prev.split()[0])

    return max_bigram_prob

max_bigram_prob = make_score_max()

def score_max(prev):
    if prev not in max_bigram_prob:
        return 1
    else:
        return max_bigram_prob[prev]

def segment(text):
    "Return a list of words that is the best segmenation of `text`."

    memo = dict()
    nodes = [0]
    def search(text, prev='<s>'):
        if text == '':
            return 0.0, []
        def candidates():
            cans = []
            sorted_list = []
            for prefix, suffix in divide(text):
                # sorted_list.append((log10(score(prefix, prev))+upper_bound(suffix, prefix, memo_upper_bound), prefix, suffix))
                bisect.insort_left(sorted_list,(log10(score(prefix, prev)), prefix, suffix) )
            #     # # print sorted_list
                
            for s in sorted_list[::-1]:
                (score_total, prefix, suffix) = s
                prefix_score = log10(score(prefix, prev))
                prefix_score = log10(score(prefix, prev))
                s1 = upper_bound(suffix, prefix)
                pair = (suffix, prefix)
                if pair not in memo:
                    memo[pair] = search(suffix, prefix)
                nodes[0]+=1
                suffix_score, suffix_words = memo[pair]
                cans.append((prefix_score + suffix_score, [prefix] + suffix_words))
            return cans
        return max(candidates())

    result_score, result_words = search(clean(text))
    # print "NODES NOOB EXPANDED:", nodes[0]
    return result_words, result_score, nodes[0]

def upper_bound(text, prev='<s>', memo_upper_bound={}):
    # return  log10(unigram_counts[max(unigram_counts, key=unigram_counts.get)]/ 1024908267229.0 )
    # print text
    if not text:
        # print "OYE", prev
        return 0.0
    else:
        # return 0.0
        # return log10(1.0)
        # print log10(max( score(prev), score_max(prev))), prev
        return log10( score_max(prev+" "+text[0]))

def get_goal(text, paths, best_score):
    "Return a list of words that is the best segmenation of `text`."
    
    memo = dict()
    memo_upper_bound = dict()
    #doing this for refrences "SORRY!"
    best_score = [MIN]
    best_path = [[]]
    nodes = [0]
    nodes_pruned =[0]
    def search(text, prev='<s>', path_score = 0.0):
        if text == '':
            best_score[0] = max(best_score[0], path_score)
            return 0.0, [] 
        def candidates(path_score):
            # nodes[0]+=1
            # print "153",path_score
            cans = []
            p_score_bigram = []
            p_score_unigram = []
            sorted_list = []
            # print prev
            flag = False
            for prefix, suffix in divide(text):
                # sorted_list.append((log10(score(prefix, prev))+upper_bound(suffix, prefix, memo_upper_bound), prefix, suffix))
                bisect.insort_left(sorted_list,(log10(score(prefix, prev))+upper_bound(suffix, prefix, memo_upper_bound), prefix, suffix) )
            #     # # print sorted_list
                
            for s in sorted_list[::-1]:
                (score_total, prefix, suffix) = s
                prefix_score = log10(score(prefix, prev))

                # prefix_score -= upper_bound(suffix, prefix, path_score + prefix_score)
                # TODO: If current path has been visited before or has score less than best score prune
                # if score of this path is less than
                # pruning logic
                # print prefix
                if path_score+prefix_score+upper_bound(suffix, prefix, memo_upper_bound)<best_score[0]:
                    nodes_pruned[0]+=1
                    break
                else:
                    pair = (suffix, prefix)
                    if pair not in memo:
                        temp =  search(suffix, prefix, path_score + prefix_score)
                        if not temp:
                            nodes[0]+=1
                            continue
                        memo[pair] = temp
                    nodes[0]+=1
                    suffix_score, suffix_words = memo[pair]
                    # print suffix_score
                    # print prefix+" "+suffix, suffix_score
                    best_score[0] = max(best_score[0], path_score + prefix_score +suffix_score)
                    cans.append((prefix_score + suffix_score, [prefix] + suffix_words))

                    # yield (prefix_score + suffix_score, [prefix] + suffix_words)
            return cans
        # temp_list = list(candidates(path_score))
        try:
            candidates_score = max(candidates(path_score))
        except ValueError, e:
            return None
        best_score[0] = max(best_score[0], path_score + candidates_score[0])
        return candidates_score
    temp = search(clean(text))
    if not temp:
        temp = best_score[0],best_path[0]
    result_score, result_words = temp
    paths[str(result_words)] = True
    # print "NODES MASTER EXPANDED:", nodes[0]
    return result_words, result_score, nodes[0]

def segment_method1(text):
    paths = dict()
    best_score = float('-inf')
    # while paths does not have prefix of every single possible path
    (goal_text, best_score, nodes) = get_goal(text, paths, best_score)

    return goal_text, best_score, nodes

def precision_recall(original, test):
    real_splits = []
    test_splits = []
    # print original, test
    for i in range(len(original)):
        if original[i].isspace():
            real_splits.append(i-len(real_splits))
    for i in range(len(test)):
        if test[i].isspace():
            test_splits.append(i-len(test_splits))
    if len(test_splits) ==0 and len(real_splits)==0:
        return 1.0,1.0
    elif len(test_splits)==0:
        return 0.0, 0.0
    elif len(real_splits)==0:
        return 0.0, 0.0
    # print real_splits,  test_splits
    precision = float(len(set(real_splits).intersection(test_splits)))/len(test_splits)
    recall = float(len(set(real_splits).intersection(test_splits)))/len(real_splits)
    return precision, recall

def main(args=''):
    """
    Command-line entry-point. Parses args into in-file and out-file then
    reads lines from infile, segments the lines, and writes the result
    to outfile. Input and output default to stdin and stdout respectively.
    """
    import os, argparse

    print precision_recall("for this"," ".join(segment_method1("forthis")[0]))
    FUNCTION_MAP = {'0' : segment,
                    '1' : segment_method1,
                     '2' : segment_method2}
    parser = argparse.ArgumentParser(description='English Word Segmentation')

    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout)
    parser.add_argument('method', nargs='?', choices = FUNCTION_MAP.keys())
    args = parser.parse_args(args)
    func = FUNCTION_MAP[args.method]

    nodes = 0
    TotalTime = datetime.now()
    TotalTime -=TotalTime
    lines =["in 1927 silent film star george valentin is posing for pictures outside the premiere of his latest hit film when a young woman peppy miller accidentally bumps into him."]
    precision_sum = 0.0
    recall_sum = 0.0
    n = 0
    for line in args.infile:
        n += 1
    # for line in lines:
        clean_line = clean2(line)
        # print clean_line
        tstart = datetime.now()
        x = func(clean_line)
        tend = datetime.now()
        TotalTime += tend- tstart
        precision, recall = precision_recall(clean_line," ".join(x[0]) )
        precision_sum += precision
        recall_sum += recall
        # if precision <0.1 or recall <0.1:
        print precision, recall
        nodes +=x[2]
        args.outfile.write(' '.join(x[0]))
        args.outfile.write(os.linesep)
    precision_sum /= n
    recall_sum /= n
    print "Precision", precision_sum, "Recall", recall_sum
    print nodes
    print TotalTime
if __name__ == '__main__':
    main(sys.argv[1:])

__title__ = 'wordsegment'
__version__ = '0.5.2'
__build__ = 0x000502
__author__ = 'Grant Jenks'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2015 Grant Jenks'