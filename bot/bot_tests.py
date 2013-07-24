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
        
    def testAddSubreddit(self):
        """
        When adding a subreddit for the bot to watch it should be added
        to the subreddits attribute of the bot
        """
        subredlen       = lambda: len(self._bot.subreddits)
        curr            = subredlen()
        self._bot.add_subreddit('datgap')
        self.assertIn('datgap',self._bot.subreddits)
        self.assertEqual(subredlen(),curr+1)
        
    def testSubmissionsChecked(self):
        """
            Upon initialisation of a bot no submission should be checked
            @todo: tests with submissions checked
        """
        self.assertEqual(self._bot.submissions_checked,{})
        
    def testAddSubmissionChecked(self):
        """
        when a submission is checked it should be added to
        the checked submissions dict
        """
        # get submission
        # add submission to checked
        # ensure submission is in checked
        pass
    
    def testGetTopSubmissions(self):
        """
            returns top n submissions from whichever subreddit passed
            @todo: if a subreddit has less than n submissions, what do?
        """
        n           = 1
        topSubs     = self._bot._get_top_submissions('bottesting', 50)
        for sub in topSubs:
            print(sub)
        self.assertEqual(len(list(topSubs)),2)
        
    def testSaveDict(self):
        """
        Saves the dictionary passed to the location passed via pickle
        """
        pass
    
    def testGetNewSubmissions(self):
        """
        returns n new submissions from the subreddit passed
        """
        n           = 1
        newSubs     = self._bot._get_new_top_submissions('bottesting', submission, n)
    
    def testReplyToComment(self):
        """
        Replies to a comment with msg passed
        if passed comment is not a comment will (raise typeerror)?
        """
        pass
    
    def testReplyToPos(self):
        """
        Replies to a post with msg passed
        if passed post is not a post will (raise typeerror)?
        """
        pass
                            
    
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()