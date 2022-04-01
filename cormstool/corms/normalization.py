import math
import operator
def normalize_in_place(d):
    if math.fsum(d.values()) != 0:
        factor=1.0/math.fsum(d.values())
        for k in d:
            d[k] = d[k]*factor
        key_for_max = max(d.items(), key=operator.itemgetter(1))[0]
        diff = 1.0 - math.fsum(d.values())
        #print "discrepancy = " + str(diff)
        d[key_for_max] += diff