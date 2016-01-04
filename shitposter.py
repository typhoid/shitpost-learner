#!/usr/bin/python

import json
import re
import sys
import urllib2

from HTMLParser import HTMLParser
from pymarkovchain import MarkovChain
from random import randint

html_rep = {
    '&amp;' : '&',
    '&quot;' : '"',
    '&#039;' : "'",
    '&gt;' : '>',
    '&lt;' : '<'
}

def sanitize( com ):
    retval = re.sub( r'\<.+\>', '', com )
    
    for sym in html_rep:
        retval = retval.replace( sym, html_rep[sym] )
    
    return retval

def thread_prop( images, board, thread_id ):
    try:
        response = urllib2.urlopen( 'http://a.4cdn.org' + board + 'thread/' + str( thread_id ) + '.json' )
    except ( urllib2.HTTPError ):
        return
    
    data = json.loads( response.read() )
    retval = u''

    for post in data['posts']:
        if 'com' in post:
            sanitized = sanitize( post['com'] )
            retval += u' {}'.format( sanitized )
        
        if 'filename' in post:
            images.append( str( post['tim'] ) + post['ext'] )
    
    return retval

def analyze_board( mc, board ):
    train_string = u''
    images = []

    print( 'Training... (may take a while)' )
    response = urllib2.urlopen( 'http://a.4cdn.org' + board + 'threads.json' )
    data = json.loads( response.read() )
    thread_ids = list()

    for page in data:
        for thread in page['threads']:
            train_string += unicode( thread_prop( images, board, thread['no'] ) )

    mc.generateDatabase( train_string )
    return images

def image_grab( images, board ):
    random_num = randint( 0, len( images ) )
    return 'http://i.4cdn.org' + board + images[random_num]

def shitpost_loop( mc, images, board ):
    read = ''
    print( 'Hit enter to generate a shitpost, or enter ? for a list of valid commands.' )

    while read != 'exit':
        read = raw_input()

        if read == '?':
            print( 'Hit enter to generate a shitpost.' )
            print( "Enter 'exit' to exit the program." )
            print( "Enter 'train' to re-train the shitposter (this takes a while)." )
            print( "Enter 'board <board>' to switch to a different board (this takes a while)." )
        elif read == 'train':
            images = analyze_board( mc, board )
            print( 'Re-training complete.' )
        elif read == 'exit':
            pass
        elif read.startswith( 'board' ):
            try:
                board = read.split()[1]
            except ( IndexError ):
                print( 'No board specified.' )
                continue

            try:
                urllib2.urlopen( 'http://a.4cdn.org' + board + 'threads.json' )
            except ( urllib2.HTTPError ):
                print( 'Invalid board.' )
                continue

            images = analyze_board( mc, board )
            print( 'Switched to {}.'.format( board ) )
        elif read:
            print( 'Invalid input.' )
        else:
            image = image_grab( images, board )
            shitpost = mc.generateString()

            print( image )
            print( u'>{}'.format( shitpost ) )

def main( args ):
    mc = MarkovChain( './shitpost_data' )
    board = ''

    print( 'Enter the name of the board you would like to learn how to shitpost from.' )
    print( 'Ex. /a/, /fit/, /tv/, etc.' )

    while not board:
        board = raw_input()

        try:
            urllib2.urlopen( 'http://a.4cdn.org' + board + 'threads.json' )
        except ( urllib2.HTTPError ):
            print( "Invalid board - try again." )
            board = ''

    images = analyze_board( mc, board )
    shitpost_loop( mc, images, board )

if __name__ == '__main__':
    main( sys.argv[1:] )

