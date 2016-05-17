# -*- coding: utf-8 -*-
# nosetests --nocapture
import sys
import wordsegment_pcfg
from wordsegment_pcfg import segment, segment_method2
import wordsegment
def comp(s):
    res0 = wordsegment.segment_method1(s)
    res1 = segment_method2(s)
    print "Baseline:", res0 
    print "PCFG Heuristic:", res1
    assert res0[0] == res1[0]
    
def nodes_saved(s):
    res0 = wordsegment.segment(s)
    res1 = segment_method2(s)
    return res0[2], res1[2]

def test_segment_0():
    comp("thehuskdrinkssnakes")

def test_segment_1():
    comp("thatcornergrowsweight")

def test_segment_2():
    comp("eachlandridesthiswinter")

def test_segment_3():
    comp("thatkingcarriesanothermaster")

def test_segment_4():
    comp("ahuskhasthiscorner")

def test_segment_5():
    comp("thatfruitcarriesthisfruit")

def test_segment_6():
    comp("akingcoversacoconut")

def test_segment_7():
    comp("thatsovereigncoversDingo")

def test_segment_8():
    comp("nohomeisthisking")

def test_segment_9():
    comp("anotherquesthasthissovereign")

def test_segment_10():
    comp("nokingcoverseveryhorse")


def test_main():
    # main(['tests/test.txt'])
    import os

    l = ["thehuskdrinkssnake", "thatcornergrowsweight", "eachlandridesthiswinter", "thatkingcarriesanothermaster", "ahuskhasthiscorner", "thatfruitcarriesthisfruit", "akingcoversacoconut", "thatsovereigncoversDingo", "nohomeisthisking", "anotherquesthasthissovereign", "nokingcoverseveryhorse"]
    #l = ['thehuskdrinks']
    nodes_exapanded_original = 0
    nodes_exapanded_optimized = 0
    frac = 0.0
    for s in l:
        n1, n2 = nodes_saved(s)
        nodes_exapanded_original+=n1
        nodes_exapanded_optimized+=n2
        frac +=float(n2)/n1

    print "NODES SAVED of total:", 100*(1 - float(nodes_exapanded_optimized)/nodes_exapanded_original), " %"
    print "NODES SAVED per string:", 100*(1 - frac/len(l)), " %"
    # result = os.linesep.join(('choose spain', 'this is a test')) + os.linesep
    # assert sys.stdout.getvalue() == result
test_main()
