#!/usr/bin/python

import json, re, sys, urllib2

from HTMLParser import HTMLParser
from pymarkovchain import MarkovChain
from random import randint

def sanitize( com ):
    retval = re.sub( r"\<.+\>", "", com )
    retval = retval.replace( "&quot;", "\"" )
    retval = retval.replace( "&#039;", "'" )
    retval = retval.replace( "&gt;", ">" )
    retval = retval.replace( "&lt;", "<" )
    return retval

def append_to_train_string( board, thread_id ):
    global mc, train_string

    response = urllib2.urlopen( 'http://a.4cdn.org' + board + 'thread/' + str( thread_id ) + '.json' )
    data = json.loads( response.read() )

    for post in data['posts']:
        if 'com' in post:
            sanitized = sanitize( post['com'] )
            train_string += u" {}".format( sanitized )

def analyze_board( board ):
    global train_string

    print( "Training... (may take a while)" )
    response = urllib2.urlopen( 'http://a.4cdn.org' + board + 'threads.json' )
    data = json.loads( response.read() )
    thread_ids = list()

    for page in data:
        for thread in page['threads']:
            append_to_train_string( board, thread['no'] )
            image_prop(board, thread['no'])

    mc.generateDatabase( train_string )

def image_prop( board, thread_id ):
    response = urllib2.urlopen( 'http://a.4cdn.org' + board + 'thread/' + str( thread_id ) + '.json' )
    data = json.loads( response.read() )

    global imageTimes = []
    global imageExt = []

    for post in data['posts']:
        if 'filename' in post:
            imageTimes.append( post['tim'] )
            imageExt.append( post['ext'] )


def image_grab( board ):
    randomNum = random.randint(0, len(imageTimes))
    image_url = 'http(s)://i.4cdn.org/' + board + '/' + imageTimes[randomNum] + '.' + imageExt[randomNum]


def shitpost_loop( board ):
    global mc, train_string

    read = ""
    used = set()

    print( "Hit enter to generate a shitpost, or enter ? for a list of valid commands." )

    while read != "exit":
        read = raw_input()

        if read == "?":
            print( "Hit enter to generate a shitpost." )
            print( "Enter 'exit' to exit the program." )
            print( "Enter 'train' to re-train the shitposter (this takes a while)." )
            print( "Enter 'board <board>' to switch to a different board (this takes a while)." )
        elif read == "train":
            train_string = u""
            analyze_board( board )
            print( "Re-training complete." )
        elif read == "exit":
            pass
        elif read.startswith( "board" ):
            try:
                board = read.split()[1]
            except ( IndexError ):
                print( "No board specified." )
                continue

            try:
                urllib2.urlopen( 'http://a.4cdn.org' + board + 'threads.json' )
            except ( urllib2.HTTPError ):
                print( "Invalid board." )
                continue

            analyze_board( board )
            print( "Switched to {}.".format( board ) )
        elif read:
            print( "Invalid input." )
        else:
            shitpost = mc.generateString()

            while shitpost in used:
                shitpost = mc.generateString()
                image =

            print( u">{}".format( shitpost ) )
            used.add( shitpost )

def main( args ):
    global mc, train_string

    mc = MarkovChain( "./shitpost_data" )
    train_string = u""
    board = ""

    print( "Enter the name of the board you would like to learn how to shitpost from." )
    print( "Ex. /a/, /fit/, /tv/, etc." )

    while not board:
        board = raw_input()

        try:
            urllib2.urlopen( 'http://a.4cdn.org' + board + 'threads.json' )
        except ( urllib2.HTTPError ):
            print( "Invalid board - try again." )
            board = ""

    analyze_board( board )
    image_grab( board )
    shitpost_loop( board )

if __name__ == "__main__":
    main( sys.argv[1:] )

