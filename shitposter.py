#!/usr/bin/python

import json
import re
import sys
import urllib2

from HTMLParser import HTMLParser
from pymarkovchain import MarkovChain
from random import randint

def image_prop( images, board, thread_id ):
    try:
        response = urllib2.urlopen( 'http://a.4cdn.org' + board + 'thread/' + str( thread_id ) + '.json' )
    except ( urllib2.HTTPError ):
        return
    
    data = json.loads( response.read() )

    for post in data['posts']:
        if 'filename' in post:
            images.append( str( post['tim'] ) + post['ext'] )

def get_board_images( board ):
    images = []

    print( 'Gathering images... (may take a while)' )
    response = urllib2.urlopen( 'http://a.4cdn.org' + board + 'threads.json' )
    data = json.loads( response.read() )

    for page in data:
        for thread in page['threads']:
            image_prop( images, board, thread['no'] )

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
        elif read == 'exit':
            pass
        elif read:
            print( 'Invalid input.' )
        else:
            image = image_grab( images, board )
            shitpost = mc.generateString()

            print( image )
            print( u'>{}'.format( shitpost ) )

def main( args ):
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

    mc = MarkovChain( './shitpost_data_{}'.format( board[1:-1] ) )
    images = get_board_images( board )
    shitpost_loop( mc, images, board )

if __name__ == '__main__':
    main( sys.argv[1:] )

