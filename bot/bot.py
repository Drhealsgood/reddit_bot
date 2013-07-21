'''
Created on 20/07/2013

@author: luke
'''
import time
import praw
import string
import pickle
from pprint import pprint
from getpass import getpass
from abc import ABCMeta, abstractmethod, abstractproperty
USERNAME    = "Drhealsgood"

class RedditBot(object):
    """
    https://praw.readthedocs.org/en/latest/pages/writing_a_bot.html
    RedditBot: 
        Configurations
            tracks subreddits to check rules in
            has a list of rules for making comments
        Should not reply to the same thread twice
        tracks all replies made
        abilities:
            make a comment
            cehck subreddits to attempt to find a place to comment
            check if URL is a comment on reddit
            login as user x
    """
    # set unique and descriptive user_agent
    __user_agent    = "reddit_bot_test v0.0 by /u/drhealsgood and /u/"
    # create Reddit object
    __reddit        = praw.Reddit(__user_agent)
    __checked       = "../resources/checked.txt"

    # might be better to read rules and subreddits in via pickle
    def __init__(self,rules=(),subreddits=[]):
        # log in and set variables
        self.__reddit.login(USERNAME,getpass())
        self.__rules        = rules
        self.__subreds      = subreddits
        # submission: comments
        self.__submissions  = {}
        # submission.id : submission
        try:
            with open(self.__checked,'rb') as f:
                self.__done = pickle.load(f) 
        except:
            self.__done     = {}
        
    @property
    def submissions(self):
        return self.__submissions
    
    @property
    def rules(self):
        return self.__rules
    
    def add_rule(self, rule):
        pass 
    
    @property
    def subreddits(self):
        return self.__subreds
    
    @subreddits.setter
    def subreddits(self,new_subreddits):
        self.__subreddits   = new_subreddits
    
    def add_subreddit(self,subreddit):
        self.__subreds.append(subreddit)
    
    @property
    def submissions_checked(self):    
        """
        Returns checked submissions
        """
        return self.__done
    
    def add_submission_checked(self,sub):    
        self.__done.setdefault(sub.id,[]).append(sub)
        
    def _save_dict(self,dictionary,location):
        """
        pickle dump the dictionary to location
        """
        pickle.dump(dictionary,location)
        
    def _get_top_submissions(self,subreddit,n):
        """
            returns top n submissions from
            subreddit
        """
        return self.__reddit.get_subreddit(subreddit).get_top(limit=n)
    
    def _get_new_submissions(self,subreddit,submission):
        """
            returns top submisons submitted later than
            submission passed
        """
        return self.__reddit.get_subreddit(subreddit).get_top(limit=None,
                                                              place_holder=submission.id)
    
    def _reply_to_comment(self,comment,msg):
        """
        replies to comment with msg
        """
        comment.reply(msg)
        
    @classmethod
    def _display_submission_info(cls,submission):
        pprint(vars(submission))
        
    def __repr__(self):
        return "RedditBot({0},{1})".format(self.__rules,self.__subreds)
    
    
class Rule(metaclass=ABCMeta):
    
    @abstractmethod
    def __init__(self,subreddits):
        """
        @param subreddits: The subreddits that this rule will apply to
        """
        self._subreddits    = subreddits
    
    def subreddits_allowed(self):
        return self._subreddits
        
    @abstractmethod
    def condition(self,submission):
        """
        condition checks to see if submission
        meets condition
        """
        pass
    
    @abstractmethod
    def action(self):
        """
        action to take if rule condition is met
        """
        pass
    
    def __repr__(self):
        return self.__class__
    
class LaughRule(Rule):
    """
    Comments with a laugh if parent comment contains a laugh
    """
    
    key_words   = ["laugh","lol","rofl","haha"]
    
    def __init__(self,subreddits,bot):
        super().__init__(subreddits)
        # I think it is terrible design.... probably
        # need to rethink it
        self._bot   = bot
    
    def condition(self,submission):
        """
        @todo:
        consider return (submission.id not in self._bot.submissions and any(key in submission.selftext for key in self.key_words)
        """
        meets       = any(key in submission.selftext for key in self.key_words)
        # have we done this submission?
        if submission.id not in self._bot.submissions:
            # mark submission as checked
            self._bot.add_submission_checked(submission)
            return meets
        return False
    
    def action(self):
        print("Hit laugh rule action")
    
    
        
if __name__ == "__main__":
    x       = RedditBot((),["python","funny"]) 
    x.add_rule(LaughRule(("funny"),x))
    subs    = x._get_top_submissions(x.subreddits[1], 200)
    subs    = [sub for sub in subs if sub.selftext!="" and sub not in x.submissions_checked]