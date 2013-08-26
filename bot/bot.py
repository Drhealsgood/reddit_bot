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
import random
import pickle
import re
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
            
    @todo:
        implement properties for hot_submissions and top_submissions.
           - Should scan all subreddits bot is applied to.
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
                        # added to rules_run, maybe not needed
        # submission.id : submission submissions checked
        try:
            with open(self.__checked,'rb') as f:
                self.__done = pickle.load(f) 
        except:
            self.__done     = {}
            
    def _clear_data(self):
        # reset rules, subreddits, rules_run to nothing
        self.__rules        = ()
        self.__subreddits   = ()
        self.__rules_run    = []
        self.__done         = {}
        
    @property
    def rules(self):
        return self.__rules
    
    def add_rule(self, *args):
        for arg in args:
            self.__rules += (arg,) 
    
    @property
    def subreddits(self):
        """
        Returns subreddits the bot will watch
        """
        return self.__subreddits
    
    @subreddits.setter
    def subreddits(self,new_subreddits):
        """
        Set a new set of subreddits to watch
        """
        self.__subreddits   = new_subreddits
    
    def add_subreddit(self,*args):
        """
        Add a subreddit to watch
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
        
    def _get_hot_submissions(self,subreddit,n):
        """
            returns top hot n submissions from
            subreddit
        """
        return self.__reddit.get_subreddit(subreddit).get_hot(limit=n)
    
    def _get_new_top_submissions(self,subreddit,submission,n):
        """
            returns n top submisons submitted later than
            submission passed
        """
        return self.__reddit.get_subreddit(subreddit).get_hot(limit=None,
                                                              place_holder=submission.id)
    
    def _reply_to_comment(self,comment,msg):
        """
        replies to comment with msg
        """
        comment.reply(msg)
        
    def _gather_links(self,submission):
        regex       = re.compile("\[.*\]\(http(|s)://.*\..*\)")
        # gather comments and self text
        comments    = praw.helpers.flatten_tree(submission.comments)
        selftext    = submission.selftext
        # collect links in unordered fashion
        self_links  = re.finditer(regex,selftext)
        comm_links  = []
        for comment in comments:
            comm_links.append(re.finditer(regex,comment.body))
        return [s_link for s_link in self_links],[c_link for group in comm_links for c_link in group]
        
    @classmethod
    def _display_submission_info(cls,submission):
        pprint(vars(submission))
        
    def __repr__(self):
        return "RedditBot({1}); Rules:{0}".format(self.__rules,self.__subreddits)
    
    
class Rule(metaclass=ABCMeta):
    __name      = "Rule"
    
    @abstractproperty
    def name(self):
        return self.__name
    
    @abstractmethod
    def __init__(self):
        pass
        
    @abstractmethod
    def condition(self):
        """
        condition checks to see if submission
        meets condition
        """
        return True
    
    @abstractmethod
    def action(self):
        """
        action to take if rule condition is met
        """
        return True
    
    def __repr__(self):
        return "{0}".format(self.__class__)
    
class BaseRule(Rule):
    __name   = "BaseRule"
    
    def __init__(self,subreddits):
        """
        @param subreddits: The subreddits that this rule will apply to
        """
        self.__active_subreddits    = subreddits

    @property
    def name(self):
        return self.__name

    def condition(self, submission):
        """
        Condition based upon a submission. Always TruE?
        """
        return True

    def action(self, submission):
        return submission

    @property
    def subreddits_allowed(self):
        return self.__active_subreddits
    
    def __eq__(self,other):
        return (self.name==other.name) and (
                    self.subreddits_allowed==other.subreddits_allowed)
        
class LaughRule(BaseRule):
    """
    Comments with a laugh if parent comment contains a laugh
    """
    __name      = "LaughRule"
    
    @property
    def name(self):
        return self.__name
    
    key_words   = ["laugh","lol","rofl","haha"]
    
    def __init__(self,bot,subreddits=["funny"]):
        super().__init__(subreddits)
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
    
    def action(self,data):
        # respond to data with one of choices
        choices     = ["Not even funny bro","Hah, you wish you were this funny",
                   "STAHP LAUGHING","I show you humour."]
        choice      = random.choice(choices)
        if isinstance(data,praw.objects.Submission):
            data.add_comment(choice)
        elif isinstance(data,praw.objects.Comment):
            data.reply(choice)
        
class GatherLinkRule(BaseRule):
    """
    GatherLinkRule collects all the links posted in the comment section and the post section of a submission to Reddit
    and puts a comment on the submission of all the links gathered
    """
    __name      = "GatherLinkRule"
    __post_temp = lambda num, title, link, author: "{num}: {title} {link} {author}".format(num=num,
                                                title=title, link=link, author=author)
    __regex_links = re.compile("\[.*\]\(http(|s)://.*\..*\)")
    
    
    def __init__(self,bot,subreddits):
        super().__init__(subreddits)
        self._bot   = bot
        self.__links= {}
        
    def condition(self,submission):
        """
        If there are any links in the post or comments the links will be linked to the rule
        and condition will be met
        """
        # clear self._links of any previous links
        self._links = {}
        self_links,comm_links = self.__bot._gather_links(submission)
        # check if any links contained
        if (len(self_links) > 0 or len(comm_links) > 0):
            self._links['selftext']     = self_links
            self._links['comm_links']   = comm_links
            return True
        # failure if this point is reached
        return False
    
    def action(self):
        """
        Respond to post with all links
        """
        response = ""
        if 'selftext' in self._links.keys():
            response += "Submission Links: \n\n"
            if len(self._links['selftext'])==0:
                response += "None \n\n\n"
            for i,link in enumerate(self._links['selftext']):
                # get title and link from link and take author from Comment?
                response = response + GatherLinkRule.__post_temp(i,link.group(0),"nyi",'NYI') + "\n"
        if 'comm_links' in self._links.keys():
            response += "\n\nComment Links: \n\n"
            if len(self._links['comm_links'])==0:
                response += "None \n\n\n"
            for i,link in enumerate(self._links['comm_links']):
                response = response + GatherLinkRule.__post_temp(i,link.group(0),"nyi","nyi") + "\n"
        # return the response for now
        return response
        
        
#if __name__ == "__main__":
#    x       = RedditBot((),["python","funny"]) 
#    x.add_rule(LaughRule(("funny"),x))
#    subs    = x._get_hot_submissions(x.subreddits[1], 200)
#    subs    = [sub for sub in subs if sub.selftext!="" and sub not in x.submissions_checked]