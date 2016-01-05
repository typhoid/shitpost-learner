#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import cgi
import cgitb
import json
import pickle
import re
import sys
import urllib.error
import urllib.request

from datetime import date
from pymarkovchain import MarkovChain
from random import choice

def load_board( board ):
    mc_path = '../data/{}-data'.format( board )
    images_path = '../data/{}-images'.format( board )

    mc = MarkovChain( mc_path )
    
    with open( images_path, 'rb' ) as images_file:
        images = pickle.load( images_file )

    return mc, images

def get_shitposts( board, num_posts ):
    mc, images = load_board( board )
    image_grab = lambda : 'http://i.4cdn.org/' + board + '/' + choice( images )
    retval = u''
    
    for i in range( 0, num_posts ):
        image = image_grab()
        shitpost = mc.generateString()

        retval += '<a href={}>{}</a><br />'.format( image, image )
        retval += u'>{}<br /><br />'.format( shitpost )
    
    return retval

cgitb.enable()

print( 'Content-Type: text/html;charset=utf-8' )
print()

fs = cgi.FieldStorage()
html = u' \
    <!doctype html> \
    <html> \
    <head> \
        <meta charset="utf-8" /> \
        <title>/{}/-tier shitposts</title> \
        <link rel="stylesheet" type="text/css" href="../styles.css" /> \
    </head> \
    <body> \
        <article> \
            <i>Shitposts from /{}/</i> \
            <br /> \
            <br /> \
            <font color=789922>{}</font> \
            <a href="../index.php">&#8617; Shitpost Again</a> \
        </article> \
    </body> \
    </html>'

try:
    board = fs['board'].value
except ( KeyError ):
    print( html.format( '?', '?', '>{}<br />>not entering a board<br /><br />'.format( date.today().year ) ) )
    sys.exit( 0 )

try:
    count = int( fs['count'].value )
except ( KeyError ):
    count = 7

print( html.format( board, board, get_shitposts( board, count ) ) )

