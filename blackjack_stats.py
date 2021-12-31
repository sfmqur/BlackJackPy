# this file is an analysis of blackjack statistics. While basic strategy tells one story.
# it sometimes is worth understanding the stats oneself.

from gameFunctions import *

base = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
base_num = [1,2,3,4,5,6,7,8,9,10,10,10,10]
deck_nums = base_num * 4*6
deck_nums.sort()

mode = 10 # this much should be obvious
average = sum(deck_nums)/(52*6)
median = 0.5* (deck_nums[52*3] + deck_nums[52*3-1])
print(average)
print(median)


