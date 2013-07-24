'''
Created on 20/07/2013

@author: luke

@todo: when a new rule is introduced we need to check submissions for that
rule too, even if they are in checked_submissions
@todo: when gathering submissions should only gather those that have not been
checked yet. should always run through n submissions though
something like, take len of checked, add that to n, take n+len(checked) subs
and that should give all the unchecked as well
'''
import time
import praw
import string
import pickle
from pprint import pprint
from getpass import getpass
from abc import ABCMeta, abstractmethod, abstractproperty
USERNAME,PASSWORD   = "a_shitty_bot","hahaha"
ID                  = 0

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
    __checked       = "../resources/"+str(ID)+"_checked.txt"
    

    # might be better to read rules and subreddits in via pickle
    def __init__(self,subreddits=(),id=None):
        global ID
        # log in and set variables
        #self.__reddit.login(USERNAME,getpass())
        if not id:
            self.__id       = ID
            ID              = self.__id + 1
        else:
            self.__id       = id
        self.__reddit.login(USERNAME,PASSWORD)
        self.__rules        = ()
        self.__subreddits   = subreddits # subreddits to run in
        self.__rules_run    = [] # when a rule has been run succesfully it will be
                        # added to rules_run
        # submission.id : submission submissions checked
        try:
            with open(self.__checked,'rb') as f:
                self.__done = pickle.load(f) 
        except:
            self.__done     = {}
        
    @property
    def rules(self):
        return self.__rules
    
    def add_rule(self, *args):
        for arg in args:
            self.__rules += (arg,) 
    
    @property
    def subreddits(self):
        return self.__subreddits
    
    @subreddits.setter
    def subreddits(self,new_subreddits):
        self.__subreddits   = new_subreddits
    
    def add_subreddit(self,*args):
        """
        Adds all subreddits in args to __subreddits
        """
        for subred in args:
            self.__subreddits += (subred,)
    
    @property
    def submissions_checked(self):    
        """
        Returns checked submissions
        """
        return self.__done
    
    def _add_submission_checked(self,sub):    
        """
        adds sub  to submissions checked
        """
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
        subs    = self.__reddit.get_subreddit(subreddit).get_top(limit=n)
        print(subs)
        return self.__reddit.get_subreddit(subreddit).get_top(limit=n)
    
    def _get_new_top_submissions(self,subreddit,submission,n):
        """
            returns n top submisons submitted later than
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
        return "RedditBot({1}); Rules:{0}".format(self.__rules,self.__subreddits)
    
    
class Rule(metaclass=ABCMeta):
    __name      = "BaseRule"
    
    @abstractproperty
    def name(self):
        return self.__name
    
    @abstractmethod
    def __init__(self,subreddits):
        """
        @param subreddits: The subreddits that this rule will apply to
        """
        self.__active_subreddits    = subreddits
    
    def subreddits_allowed(self):
        return self.__active_subreddits
        
    @abstractmethod
    def condition(self,submission):
        """
        condition checks to see if submission
        meets condition
        """
        return True
    
    @abstractmethod
    def action(self,submission):
        """
        action to take if rule condition is met
        """
        return submission
    
    def __repr__(self):
        return "{0}".format(self.__class__)
    
    def __eq__(self,other):
        return self.name == other.name
    
class LaughRule(Rule):
    """
    Comments with a laugh if parent comment contains a laugh
    """
    __name      = "LaughRule"
    
    def name(self):
        return self.__name
    
    key_words   = ["laugh","lol","rofl","haha"]
    
    def __init__(self,bot,subreddits=["funny"]):
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
    
    def action(self,submission):
        print(submission.id,"Hit laugh rule action")
    
    
        
#if __name__ == "__main__":
#    x       = RedditBot((),["python","funny"]) 
#    x.add_rule(LaughRule(("funny"),x))
#    subs    = x._get_top_submissions(x.subreddits[1], 200)
#    subs    = [sub for sub in subs if sub.selftext!="" and sub not in x.submissions_checked]