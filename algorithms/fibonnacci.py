from __future__ import division

import math


def fib(val):
   if val < 0:
      print "ERROR: Invalid input value"
      return
   if val == 0:
       return 0
   if val == 1:
       return 1
   else:
       fibc = 0
       fib = [0,1]
       ii = 1
       while ii < val:
           fibc = fib[0] + fib[1]
           fib[0] = fib[1]
           fib[1] = fibc
           ii += 1
           
   return fibc