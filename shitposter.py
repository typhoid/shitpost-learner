#!/usr/bin/python

import json, re, sys, urllib2

from HTMLParser import HTMLParser
from pymarkovchain import MarkovChain
from random import randint

def sanitize( com ):
    retval = re.sub( r"\<.+\>", "", com )
    retval = retval.replace( "&quot;", "\"" )
    retval = retval.replace( "&#039;", "'" )
    return retval

def train_on_thread( board, thread_id ):
    global mc
    
    response = urllib2.urlopen( 'http://a.4cdn.org/' + board + '/thread/' + str( thread_id ) + '.json' )
    data = json.loads( response.read() )
    
    for post in data['posts']:
        if 'com' in post:
            mc.generateDatabase( sanitize( post['com'] ) )

def analyze_board( board ):
    print( "Training... (may take a while)" )
    response = urllib2.urlopen( 'http://a.4cdn.org/' + board + '/threads.json' )
    data = json.loads( response.read() )
    thread_ids = list()
    
    # Doing all 10 pages takes a long time
    #for page in data:
        #for thread in page['threads']:
    
    for thread in data[randint( 0, 9 )]['threads']:
        train_on_thread( board, thread['no'] )

def shitpost_loop( board ):
    read = ''
    last = ''
    
    while read != "exit":
        print( "\nEnter a command. Enter ? for a list of valid commands." )
        read = raw_input()
        
        if read == "?":
            print( "\nValid input is:\nexit - Exit the program.\nprint - Generate a shitpost.\ntrain - Learn how to shitpost (takes a while)." )
        elif read == "train":
            analyze_board( board )
        elif read == "exit":
            pass
        elif read == "print":
            next = mc.generateString()
            
            while next == last:
                next = mc.generateString()
            
            print( next )
            last = next
        else:
            print( "Invalid input." )

def main( args ):
    global mc
    
    mc = MarkovChain( "./shitpost_data" )
    
    print( "Enter the name of the board you would like to learn how to shitpost from." )
    board = raw_input()
    analyze_board( board )
    shitpost_loop( board )

if __name__ == "__main__":
    main( sys.argv[1:] )

