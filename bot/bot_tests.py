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
        attrs       = vars(self._bot)
        expected    = {'__rules':       (),
                       '__subreddits':  (),
                       '__done':        {},
                       '__rules_run':   [],
                       '__id'       :   ID
                       }
        for val in expected:
            if val == '__id':
                self.assertEqual(attrs['_RedditBot'+val],expected[val]+1,
                            "got {0} for {1}, expected {2}".format(attrs['_RedditBot'+val],
                                                                    val, expected[val]))
            else:
                self.assertEqual(attrs['_RedditBot'+val],expected[val],
                                 "got {0} for {1}, expected {2}".format(attrs['_RedditBot'+val],
                                                                        val, expected[val]))
            
    def testInitWithParams(self):
        """
            this test is designed to test the init function
            when we have runs, rules, subreddits, and checked 
        """
        pass
    
    def testRules(self):
        """
            rules is expected to return the rules that RedditBot
            will check and take action upon
        """
        # when a bot is first initalised with no parameters
        # it's expected there are no rules enabled
        self.assertEqual(self._bot.rules,())
        
    def testAddRule(self):
        """
            When we add a rule it should be inserted into 
            rules so the bot knows to check for it
        """
        self._bot.add_rule(LaughRule(self._bot))
        self.assertIn(LaughRule(self._bot),self._bot.rules)
        self.assertEqual(len(self._bot.rules),1)
        
    def testSubreddits(self):
        """
            Returns subreddits bot is watching
            should also be able to set subreddits to some subreddits
        """
        subs                = ("funny","python")
        self.assertEqual(self._bot.subreddits,())
        self._bot.subreddits= subs
        for sub in subs:
            self.assertIn(sub, self._bot.subreddits)
        self.assertEqual(len(self._bot.subreddits),len(subs))
                            
    
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()