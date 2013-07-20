'''
Created on 20/07/2013

@author: luke
'''
import time
import praw
import string
from getpass import getpass
USERNAME    = ""

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

    def __init__(self,rules,subreddits):
        # log in
        self.__reddit.login(USERNAME,getpass())
        self.__rules        = rules
        self.__subreds      = subreddits
        # submission: comments
        self.__submissions  = {}
        
    @property
    def submissions(self):
        return self.__submissions
    
    @property
    def rules(self):
        return self.__rules
    
    def add_rule(self, rule):
        self.__rules.append(rule)
    
    @property
    def subreddits(self):
        return self.__subreds
    
    @subreddits.setter
    def subreddits(self,new_subreddits):
        self.__subreddits   = new_subreddits
    
    def add_subreddit(self,subreddit):
        self.__subreds.append(subreddit)
        
    def _get_submissions(self,subreddit,n):
        """
            returns top n submissions from
            subreddit
        """
        return self.__reddit.get_subreddit(subreddit).get_top(limit=n)