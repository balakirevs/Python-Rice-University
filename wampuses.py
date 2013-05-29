# http://www.codeskulptor.org/#user15_Gv7Ump0X0b6NtK9.py
pop_slow_no = 1000
pop_fast = 1
while pop_slow_no > pop_fast:
      pop_slow_no = (2 * pop_slow_no) - (2 * pop_slow_no * 0.40)
      pop_fast = (2 * pop_fast) - (2 * pop_fast * 0.30)  
      print "Slow Wumpuses = ", pop_slow_no, "Fast Wumpuses = ", pop_fast