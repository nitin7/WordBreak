from PyDictionary import PyDictionary
dictionary = PyDictionary()

#Given a word return set of all possible POS tags from lexicon
def word_to_pos_lexicon(word):
    #If found in lexicon return its POS tag
    f = open('lexicon', 'r')
    possible_pos = set()
    for line in f:
        l = line.split()
        if word == l[2].lower():
        	possible_pos.add(l[0])
    return possible_pos

#Given a word return set of all possible POS tags from dictionary
def word_to_pos_any(word):
    #Third party bs to return the set of possible POS tags it can be 
    possible_pos = set()
    for tag in dictionary.meaning(word):
        possible_pos.add(str(tag))
    return possible_pos

#Terminality is determined by the lexicon
def is_terminal(tag):
    f = open('lexicon', 'r')
    all_pos = set()
    for line in f:
        all_pos.add(line.split()[0])
    return (tag in all_pos)

def exists(rule, tag):
    for t in rule:
        if t == tag:
            return True
    return False

#TODO: Maybe normalize weights beforehand
#Assumptions:
#-Chomsky Normal Formal
#-The grammar is well formed (ex. no rules like Nbar -> Nbar or S -> (nothing here))
#Functionality:
#Given two terminal tags output if tag2 is reachable from tag1
def reachable(tag1, tag2):
    #Initialize dict mapping path to cumulative prob score
    score = dict()
    #Initialize dict mapping pos tag to list of tuples
    #First element of tuple contains list with max size 2
    #Second element of tuple is just the weight assigned by the PCFG
    rules = dict()
    #Begin reading grammar into our pythonic representation 
    f = open('simple_grammar', 'r')
    for line in f:
        rule = line.split()
        weight = int(rule[-1])
        rule = rule[:-1]
        key_pos_tag = rule[0]
        if key_pos_tag not in rules:
            rules[key_pos_tag] = [([pos_tag for pos_tag in rule[2:]], weight)]
        else:
            rules[key_pos_tag] = rules[key_pos_tag] + [([pos_tag for pos_tag in rule[2:]], weight)]
    #End reading grammar

    #Initialize bookkeeping of cur_path and cur_path_score
    cur_path = ''
    cur_path_score = 0

    for start in rules:
        for rule, weight in rules[start]:
            #Identify all rules containing tag1 on arrow end
            if exists(rule, tag1):
                cur_path += tag1
                #Ignoring single children rules for now. Could maybe do something with them in the future
                if rule[0] == tag1 and len(rule) > 1 and rule[1] != start:
                    #Begin search
                    #For each rule two cases
                    #Case 1: tag1 is preceding terminal -> forward search on succeeding elem
                        #If succeeding elem is terminal
                            #return if tag2 is succeeding elem
                        #Else suceeding elem in non-terminal
                            #For each rule containing succeeding elem on arrow begin ignoring self-edges
                                #For each preceding elem that is tag2
                                    #score[cur_path + preceding elem] = cur_path_score + rule_score
                    if is_terminal(rule[1]):
                        if rule[1] == tag2:
                            cur_path += '->' + tag2
                            cur_path_score += weight
                            score[cur_path] = cur_path_score
                            #emptying cur_path is problematic but ok -----deal with this later
                            cur_path = tag1
                            cur_path_score = 0
                        #If the else case of the second if is reached then this rule did not tell us anything
                        #So it's logical to skip to the next rule containing tag1
                    else:
                        for start2 in rules:
                            if start2 == rule[1]:
                                for rule2, weight2 in rules[start2]:
                                    if rule2[0] == tag2:
                                        cur_path += '->' + start2 + '->' + tag2
                                        cur_path_score += weight + weight2
                                        score[cur_path] = cur_path_score
                                        cur_path = tag1
                                        cur_path_score = 0
                #Case 2: tag1 is "succeeding" terminal -> backward search on preceding elem
                #Note since we are given CNF, this case only applies when len(rule) == 1 ex. Noun Prep
                #So technically preceding element is just start
                #For each tag in rules[start] that is the preceding elem
                    #Initiate search on succeeding elem
                    #If succeeding elem is a terminal
                        #update score if tag2 is suceeding elem
                    #Else succeeding elem is non-terminal
                        #For each rule containing succeeding elem on arrow begin ignoring self-edges
                            #For each preceding elem that is tag2
                                #update score
                if len(rule) == 1 and rule[0] == tag1:
                    for rule2, weight2 in rules[start]:
                        if rule != rule2 and start == rule2[0] and len(rule2) > 1:
                            if is_terminal(rule2[1]):
                                if rule2[1] == tag2:
                                    cur_path += '->' + start + '->' + tag2
                                    cur_path_score += weight + weight2
                                    score[cur_path] = cur_path_score
                                    cur_path = tag1
                                    cur_path_score = 0
                            else:
                                for start2 in rules:
                                    if start2 == rule2[1]:
                                        for rule3, weight3 in rules[start2]:
                                            #Equality with tag2 implies terminality so we don't
                                            #check for that
                                            if rule3[0] == tag2:
                                                cur_path += '->' + start + '->' + start2 + '->' + tag2
                                                cur_path_score += weight + weight2 + weight3
                                                score[cur_path] = cur_path_score
                                                cur_path = tag1
                                                cur_path_score = 0
    return score

#Using simple_grammar
def reachable_tests():
    print 'These should be reachable'
    print reachable('Det', 'Noun')
    print reachable('Noun', 'Prep')
    print reachable('Prep', 'Det')
    print reachable('Prep', 'Proper')
    print reachable('VerbT', 'Det')
    print reachable('VerbT', 'Proper')
    print 'These should not be reachable'
    print reachable('Det', 'Det')
    print reachable('Det', 'Proper')
    print reachable('Noun', 'Noun')
    print reachable('Prep', 'Prep')
    print reachable('VerbT', 'Noun')
    print reachable('VerbT', 'Prep')



#Mention case in report where if LCA of word and prev is S score will be bad
def score_pcfg(word, prev):
    #Get POS tag sets of word and prev
    word_tset = word_to_pos_lexicon(word)
    prev_tset = word_to_pos_lexicon(prev)

    # if prev == '<s>' and word_tset:
    #     return 10.0 / 1024908267229.0 * 10
    # if prev == '<s>' and not word_tset:
    #     return 10.0 / (1024908267229.0 * 100 ** len(word))
    #If either set is empty
        #Penalize heavily
    #Else
        #Determine if word reachable from prev according to PCFG
            #If reachable (when reachable returns non empty dictionary)
                #Pick path with the highest score and return that score
            #Not reachable (when reachable returns empty dictionary)
                #Penalize a lot but not as much as in the case where the tagsets were empty

    if not word_tset and not prev_tset:
        return pow(10.0 / (1024908267229.0 * 10 ** len(word)), 2)
    if not prev_tset:
        return 10.0 / (1024908267229.0 * 10 ** len(prev))
    if not word_tset:
        return 10.0 / (1024908267229.0 * 10 ** len(word))

    score = reachable(next(iter(prev_tset)), next(iter(word_tset)))
    if score:
        return 10*max(score.iteritems(), key=score.get)[1] / (1024908267229.0)
    else:
        return 10.0 / (1024908267229.0 * 10)

test = 'thehuskdrinkssnakes'

def score_pcfg_tests():
    print 'Scores should be in non-increasing order'
    print score_pcfg('husk', 'the')
    #The following case won't really happen but this is testing reachability indirectly rather than
    #PCFG scoring
    print score_pcfg('drink', 'the')
    print score_pcfg('snakes', 'drinks')
    print score_pcfg('drinks', 'husk')
    print score_pcfg('snakes', 'thehuskdrinks')
    print score_pcfg('es', 'thehuskdrinkssnak')
    print score_pcfg('huskdrinkssnakes', 'the')
    print score_pcfg('ehuskdrinkssnakes', 'th')

# score_pcfg_tests()


