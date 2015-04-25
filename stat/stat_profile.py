#!/usr/bin/python
import pstats
import sys
p = pstats.Stats(str(sys.argv[1]))
p.sort_stats('cumulative').print_stats(20)
