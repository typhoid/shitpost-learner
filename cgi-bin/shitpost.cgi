#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cgi
import cgitb
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

    response = urllib2.urlopen( 'http://a.4cdn.org' + board + 'threads.json' )
    data = json.loads( response.read() )

    for page in data:
        for thread in page['threads']:
            image_prop( images, board, thread['no'] )

    return images

def image_grab( images, board ):
    random_num = randint( 0, len( images ) )
    return 'http://i.4cdn.org' + board + images[random_num]  

def get_shitposts( board, num_posts ):
    mc = MarkovChain( '../data/{}'.format( board ) )
    retval = u''
    #images = get_board_images( board )
    
    for i in range( 0, num_posts ):
        #image = image_grab( images, board )
        shitpost = mc.generateString()

        #print( image )
        retval += u'>{}<br />'.format( shitpost )
    
    return retval

cgitb.enable()

print 'Content-Type: text/html;charset=utf-8'
print

fs = cgi.FieldStorage()
board = fs['board'].value
count = int( fs['count'].value )

html = ' \
    <html> \
    <head> \
    <title>/%s/-tier shitposts</title> \
    </head> \
    <body> \
        <font color=789922>%s</font> \
    </body> \
    </html>'

print html % ( board, get_shitposts( board, count ) )

