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


    def __init__(self,rules):
        