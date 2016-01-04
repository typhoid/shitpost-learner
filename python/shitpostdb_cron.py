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

def thread_prop( board, thread_id ):
    try:
        response = urllib2.urlopen( 'http://a.4cdn.org' + board + 'thread/' + str( thread_id ) + '.json' )
    except ( urllib2.HTTPError ):
        return
    
    retval = u''
    data = json.loads( response.read() )

    for post in data['posts']:
        if 'com' in post:
            sanitized = sanitize( post['com'] )
            retval += u' {}'.format( sanitized )
    
    return retval

def analyze_board( mc, board ):
    train_string = u''

    response = urllib2.urlopen( 'http://a.4cdn.org' + board + 'threads.json' )
    data = json.loads( response.read() )
    thread_ids = list()

    for page in data:
        for thread in page['threads']:
            train_string += unicode( thread_prop( board, thread['no'] ) )

    mc.generateDatabase( train_string )

def main( args ):
    board = args[0]
    mc = MarkovChain( '../data/shitpost_data_' + board )
    analyze_board( mc, '/{}/'.format( board ) )
    mc.dumpdb()

if __name__ == '__main__':
    main( sys.argv[1:] )

