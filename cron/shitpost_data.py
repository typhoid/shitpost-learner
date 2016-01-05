#!/usr/bin/env python3

import json
import pickle
import re
import sys
import urllib.error
import urllib.request

from pymarkovchain import MarkovChain

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
    retval = u''
    
    try:
        response = urllib.request.urlopen( 'http://a.4cdn.org/' + board + '/thread/' + str( thread_id ) + '.json' )
    except ( urllib.error.HTTPError ):
        return retval
    
    data = json.loads( response.readall().decode('utf-8') )

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
    
    response = urllib.request.urlopen( 'http://a.4cdn.org/' + board + '/threads.json' )
    data = json.loads( response.readall().decode('utf-8') )

    for page in data:
        for thread in page['threads']:
            train_string += thread_prop( images, board, thread['no'] )

    mc.generateDatabase( train_string )
    mc.dumpdb()
    
    with open('../data/{}-images'.format( board ), 'wb') as db_file:
        pickle.dump( images, db_file )

def main( args ):
    board = args[0].replace( '/', '' )
    
    if not os.path.isdir( '../data' ):
        os.mkdir( '../data' )
    
    mc = MarkovChain( '../data/{}-data'.format( board ) )
    analyze_board( mc, board )

if __name__ == '__main__':
    main( sys.argv[1:] )

