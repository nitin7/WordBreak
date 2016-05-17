# -*- coding: utf-8 -*-
# nosetests --nocapture
import sys
from .context import wordsegment
from wordsegment import segment_method1, main, segment
from wordsegment_pcfg import segment_method2
def comp(s):
    res0 = segment(s)
    res1 = segment_method1(s)
    assert res0[0] == res1[0]
    
def nodes_saved(s):
    res0 = segment(s)
    res1 = segment_method1(s)
    return res0[2], res1[2]

def test_segment_0():
    comp('choosespain')
    # assert segment_method1('choosespain')[0] == ['choose', 'spain']

def test_segment_1():
    comp('thisisatest')
    # assert segment_method1('thisisatest')[0] == ['this', 'is', 'a', 'test']

def test_segment_2():
    comp('wheninthecourseofhumaneventsitbecomesnecessary')

def test_segment_3():
    comp('whorepresents')

def test_segment_4():
    comp('expertsexchange')

def test_segment_5():
    comp('speedofart')

def test_segment_6():
    comp('nowisthetimeforallgood')

def test_segment_7():
    comp('itisatruthuniversallyacknowledged')

def test_segment_8():
    comp('itwasabrightcolddayinaprilandtheclockswerestrikingthirteen')

def test_segment_9():
    comp('itwasthebestoftimesitwastheworstoftimesitwastheageofwisdomitwastheageoffoolishness')

def test_segment_10():
    comp('asgregorsamsaawokeonemorningfromuneasydreamshefoundhimselftransformedinhisbedintoagiganticinsect')

def test_segment_11():
    comp('inaholeinthegroundtherelivedahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresandyholewithnothinginittositdownonortoeatitwasahobbitholeandthatmeanscomfort')

def test_segment_12():
    comp('faroutintheunchartedbackwatersoftheunfashionableendofthewesternspiralarmofthegalaxyliesasmallunregardedyellowsun')

def test_main():
    # main(['tests/test.txt'])
    import os

    l = ["choosespain", 'thisisatest','wheninthecourseofhumaneventsitbecomesnecessary',   'whorepresents',    'expertsexchange',   'speedofart',    'nowisthetimeforallgood',  'itisatruthuniversallyacknowledged',    'itwasabrightcolddayinaprilandtheclockswerestrikingthirteen',   'itwasthebestoftimesitwastheworstoftimesitwastheageofwisdomitwastheageoffoolishness', 'asgregorsamsaawokeonemorningfromuneasydreamshefoundhimselftransformedinhisbedintoagiganticinsect','inaholeinthegroundtherelivedahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresandyholewithnothinginittositdownonortoeatitwasahobbitholeandthatmeanscomfort' , 'faroutintheunchartedbackwatersoftheunfashionableendofthewesternspiralarmofthegalaxyliesasmallunregardedyellowsun']
    nodes_exapanded_original = 0
    nodes_exapanded_optimized = 0
    frac = 0.0
    for s in l:
        n1, n2 = nodes_saved(s)
        print n1, n2
        nodes_exapanded_original+=n1
        nodes_exapanded_optimized+=n2
        frac +=float(n2)/n1

    print "NODES SAVED of total:", 100*(1 - float(nodes_exapanded_optimized)/nodes_exapanded_original), " %"
    print "NODES SAVED per string:", 100*(1 - frac/len(l)), " %"
    # result = os.linesep.join(('choose spain', 'this is a test')) + os.linesep
    # assert sys.stdout.getvalue() == result
test_main()
