import sys
import os
# from pcfg import *
import random
from wordsegment import *

# States: Features of prefix current split: boolean vector stating whether they are valid words, if not gigantic negative reward for any action that leads to such a split

# Actions: A split in the suffix

# Rewards: Any completely valid split (goal), -score, action leading to invalid split -inf, else 0

pos_list = ['5WS', 'Adj', 'Adv', 'Aux', 'Conj', 'Det', 'INT', 'Misc', 'Modal', 'Noun', 'Prep', 'Pronoun', 'Proper', 'VerbT']

def build_dict(file):
    dict = {}
    with open(file,'r') as f:
        for line in f.readlines():
            dict[line.split()[0]] = 1
    return dict

def check_valid(state, dict):
    # state: (prefix, suffix)
    prefix = state[0]
    suffix = state[1]
    
    words = prefix.split()
    res = (True, True)
    for w in words:
        if (not w in dict) and w != '<s>':
            res = (False, res[1])
    if len(suffix) == 0:
        res = (res[0],False)
    else:
        if suffix in dict:
            res = (res[0],False)
    #print prefix, "---", suffix
    #print res
    return res

def stop_now(state,dict, res):
    # res = check_valid(state,dict)
    # If it is a complete parse or no split left, stop
    if res[0] and res[1]:
        # print "FALSE"
        return False
    else:
        print "TRUE", state[0], "---", state[1]
        return True

def get_reward(state, dict):
    res = check_valid(state,dict)
    prefix = state[0]
    suffix = state[1]
    if not res[0]:
        return -100
    else:
        pref_words = prefix.split()
        reward = 0.0
        for i in range(0, len(pref_words)-1):
            reward += log10(score(pref_words[i], pref_words[i+1]))
    if not res[1] and suffix in dict:
        return 100000-((reward + log10(score(pref_words[-1],suffix)))/(len(pref_words)+1))
    else:
        return 100000-(reward/len(pref_words))

def get_best_action(prefix, suffix, positions):
    a = -1
    bestQValue = float('-inf')
    for i in range(0,positions):
        #new_prefix = prefix+str(suffix[:i+1])
        #new_suffix = suffix[i+1:]
        #feature_vect = get_feature_vector(new_prefix,new_suffix)
        q = score(prefix.split()[-1], str(suffix[:i+1]))
        if q > bestQValue:
            bestQValue = q
            a = i
    return a

def pick_action(prefix, suffix, positions):
    epsilon = random.random()
    if epsilon < 0.1:
        # Random action
        i = random.randint(0,positions)
    else:
        # Greedy, Best action based on current policy
        i = get_best_action(prefix, suffix, positions)
    return i

def get_feature_vector(prefix, suffix):
    words = prefix.split()
    vect = word_to_pos_lexicon(words[-1])
    feature_vect = [0.0]*len(pos_list)
    for v in vect:
        feature_vect[pos_list.index(v)] = 1.0
    return vect1

def calculate_sigmoid(feature_vect, theta, n):
    for k in range(0,n):
        dotProd += theta[k]*feature_vect[k]
    return dotProd

def calculate_sigmoid_gradient(feature_vect, n):
    return 1.0


def main(args):
    unigram_file = args[0]
    bigram_file = args[1]
    train_file = args[2]
    # test_file = args[3]
    dict = build_dict(args[0])
    n = len(pos_list)
    theta = [0.0]*n
    gamma = 0.1
    lamb = 0.1
    alpha = 0.1
    with open(train_file,'r') as f:
        for string in f.readlines():
            #print string
            for i in range(0,100000):
                prefix = "<s>"
                suffix = string
                # s0 = {"prefix": "<s>", "suffix": string, "feature_vect": []}
                a = pick_action(prefix, suffix, len(suffix))
                #print a
                res = check_valid((prefix,suffix),dict)
                count = 0
                while not stop_now((prefix,suffix),dict, res):
                    count +=1
                    #print prefix, "---", suffix
                    #if count >10:
                    #    break
                    e = [1.0] * n
                
                    #feature_vect = get_feature_vector(new_prefix,new_suffix)
                    q_a = score(prefix.split()[-1], str(suffix[:a+1]))
                    prefix = prefix + " " + str(suffix[:a+1])
                    suffix = suffix[a+1:]
                
                    # q_a = calculate_sigmoid(feature_vect, len(new_prefix.split())+1)
                    # sigmoid_grad = calculate_sigmoid_gradient(feature_vect, len(new_prefix.split())+1)

                    reward = get_reward((prefix, suffix),dict)
                    #print reward
                    delta = reward - q_a

                    a = pick_action(prefix, suffix, len(suffix))
                    q_a_prime = score(prefix.split()[-1], str(suffix[:a+1]))
                    prefix = prefix + " " + str(suffix[:a+1])
                    suffix = suffix[a+1:]

                    state = (prefix, suffix)
                    res = check_valid(state,dict)
                    #feature_vect = get_feature_vector(new_prefix,new_suffix)
                    #q_a_prime = calculate_sigmoid(feature_vect, len(new_prefix.split())+1)

                    delta += gamma * q_a_prime;
                    for k in range(0,n):
                        theta[k] += alpha*delta*e[k] #*sigmoid_grad
                        e[k] = gamma * lamb * e[k];

if __name__ == '__main__':
    main(sys.argv[1:])





