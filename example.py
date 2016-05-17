from wordsegment import segment_method1, segment, clean
import sys



def main(arg="iamtoocoolforthis"):

    s = clean(arg)
    print "CLEANED STRING:", s
    print "======================RUNNING OPTIMIZED==================="
    print segment_method1(s)
    print "======================RUNNING VANILLA==================="
    print segment(s)



if __name__ == '__main__':
    main(sys.argv[1])