'''
Created on 23/07/2013

@author: luke
'''
import unittest
from bot import *
from mock import Mock
import re

def gather_data():
    global REDDIT
    ua      = "test_bot"
    REDDIT  = praw.Reddit(ua)
    REDDIT.login(USERNAME,PASSWORD)
    
# Reddit will be the praw Reddit agent
gather_data()


class TestRedditBot(unittest.TestCase):
    _bot   = RedditBot()

    def setUp(self):
        pass


    def tearDown(self):
        # clear the clutter
        self._bot._clear_data()

        
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
        self.assertTrue(False)
    
    def testGetHotSubmissions(self):
        """
            returns top n submissions from whichever subreddit passed
            @todo: if a subreddit has less than n submissions, what do?
            should scan all subreddits bot is applied to.
        """
        topSubs     = self._bot._get_hot_submissions('drsbottesting', 3)
        self.assertEqual(len(list(topSubs)),3)
        
    def testSaveDict(self):
        """
        Saves the dictionary passed to the location passed via pickle
        """
        self.assertTrue(False)
    
    def testGetNewSubmissions(self):
        """
        returns n new submissions from the subreddit passed
        """
        self.assertTrue(False)
        n           = 1
        submission  = next(REDDIT.get_subreddit("drsbottesting").get_hot())
        newSubs     = self._bot._get_new_top_submissions('drsbottesting', submission, n)
        
    
    def testReplyToComment(self):
        """
        Replies to a comment with msg passed
        if passed comment is not a comment will (raise typeerror)?
        """
        self.assertTrue(False)
    
    def testReplyToPos(self):
        """
        Replies to a post with msg passed
        if passed post is not a post will (raise typeerror)?
        """
        self.assertTrue(False)
    
    def testClearData(self):
        """
        The purpose of clear data is to clear all the
        data stored in our bot - a soft reset so to speak.
        """
        # all rules, subreddits, rules_run, and submissions checked
        # should be set to blank slate
        expected= {'rules':(),'subreddits':(),
                   'rules_run':[],'done':{},}    
        actual  = {'rules':self._bot.rules,
                   'subreddits':self._bot.subreddits,
                   'rules_run':self._bot.rules_run,
                   'done':self._bot.submissions_checked,
                   }    
        for val in expected:
            self.assertEqual(expected[val],actual[val],
                "Expected {0} but got {1}".format(expected[val],actual[val]))
            

class TestBaseRule(unittest.TestCase,metaclass=ABCMeta):
    """
    A Rule should have a name;
    active subreddits; a condition;
    and an action.
    A rule should have equailty.
    """
    _submission    = REDDIT.get_new()
    
    @abstractmethod
    def setUp(self):
        self._rule  = BaseRule(subreddits="drsbottesting")
        
    @abstractmethod
    def tearDown(self):
        self._rule  = None
        
    @abstractmethod
    def testEq(self):
        """
        Each rule type should have a unique name as an
        identifier to the rule type
        The equality should also be based upon the subreddits
        a rule has
        """
        other   = BaseRule(subreddits="drsbottesting")
        self.assertEqual(self._rule,other)
        self.assertNotEqual(self._rule,BaseRule(subreddits="funny"))
        self.assertEqual(self._rule.name,other.name)
        self.assertEqual(self._rule.subreddits_allowed,other.subreddits_allowed)
        
    @abstractmethod
    def testCondition(self):
        """
        A condition should eventually return True or False
        the base Rule will simply return True
        """
        self.assertTrue(self._rule.condition(self._submission))
    
    @abstractmethod
    def testAction(self):
        """
        The BaseRule will simply return the submission
        as it has passed the condition
        """
        self.assertEqual(self._rule.action(self._submission),self._submission)
    
class TestLaughRule(TestBaseRule):
    
        def setUp(self):
            pass


        def tearDown(self):
            pass

        def testEq(self):
            self.assertFalse(True)

        def testCondition(self):
            pass


        def testAction(self):
            return TestBaseRule.testAction(self)
        
class TestGatherLinkRule(TestBaseRule):
    _reddit_bot     = RedditBot()
    
    def testGatherLinks(self):
        submission = self._reddit_bot._get_hot_submissions('drsbottesting', 1)
        sub         = next(submission)
        # make sure it is link post
        self.assertRegex(sub.selftext, '\[.*\]\(http(|s)://.*\..*\)', 
                         "Expected link in submission selftext")
        flat        = praw.helpers.flatten_tree(sub.comments)
        # gather links
        comm_links  = []
        pattern     = re.compile('\[.*\]\(http(|s)://.*\..*\)')
        sub_lins    = re.finditer(pattern,sub.selftext)
        for comment in flat:
            comm_links.append(re.finditer(pattern,comment.body))
        all_links   = [link for link in sub_lins],[link for group in comm_links for link in group]
        
        # Uncomment this and remove other code when gather_links has been moved
#        self.assertEqual(len(all_links),len(self._reddit_bot._gather_links(submission)))
        for i in range(2):
            self.assertEqual(len(all_links[i]),len(self._rule._gather_links(sub)[i]))
    
    def setUp(self):
        self._rule  = GatherLinkRule(self._reddit_bot,'drsbottesting')
        
    def tearDown(self):
        self._rule  = None
    
    def testEq(self):
        self.assertTrue(False)


    def testCondition(self):
        self.assertTrue(False)


    def testAction(self):
        """
        GatherLinkRule acts by gathering all links in submission selftext,
        all links in comments text, and posts a comment with all links
        @todo: proper test - just checking action here, needs to be implemented
        with bot for proper testing.
        """
        
            
        submissions  = self._reddit_bot._get_hot_submissions('drsbottesting', 1)
        # add rule to bot
        self._reddit_bot.add_rule(self._rule)
        # check submission has a link
        for submission in submissions:
            helper(submission)
        self.assertTrue(False)
        """
            @todo
            """
        
    def testExecution(self):
        submissions  = self._reddit_bot._get_hot_submissions('drsbottesting', 1)
        # add rule to bot
        self._reddit_bot.add_rule(self._rule)
        # check submission has a link
        for submission in submissions:
            # gather links via condition
            result  = self._rule.condition(submission)
            """
            @todo
            """
        self.assertTrue(False)
            
            
            

def load_tests(loader):
    suite = unittest.loader.makeSuite(TestLaughRule)
    v       = unittest.TextTestRunner()
    v.verbosity = 1
    v.run(suite)
    suite   = unittest.loader.makeSuite(TestGatherLinkRule)
    v.run(suite)
    suite   = unittest.loader.makeSuite(TestRedditBot)
    v.run(suite)
    
    
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    load_tests(unittest.loader)
