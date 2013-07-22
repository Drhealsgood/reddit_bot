'''
Created on 23/07/2013

@author: luke
'''
import unittest
from bot import *


class TestRedditBot(unittest.TestCase):


    def setUp(self):
        self._bot   = RedditBot()


    def tearDown(self):
        self._bot   = None


    def testInit(self):
        """
        A bot should have:
            user_agent, rules, subreddits to run on,
            submissions checked alongside the rules the submission
            has been checked for, rules that have been run
        """
        pass
    
    def testRogueLike(self):
        self._bot.add_subreddit("roguelikes")
        subs    = self._bot._get_top_submissions("roguelikes", 100)
        for sub in subs:
            # comment on submission informing 
            # them it is not roguelike
            sub.add_comment("Not a roguelike")
            pprint(vars(sub))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()