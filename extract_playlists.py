#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright 2017, François Revol <revol@free.fr>
#

import sys
import urllib.request
import json
import youtube_dl

url = 'http://webcast.berkeley.edu/itunesu_podcasts.js'

f = urllib.request.urlopen(url)
lines = f.readlines();
lines = [x.decode('utf-8') for x in lines]
start = lines.index('var itu_courses = [\n') + 1
end = lines.index('];\n')
lines = lines[start:end]
lines = ''.join(lines)
#fix last line
lines = lines.replace('"},\n\n\n', '"}')
lines = '[' + lines + ']'
# some hidden lines...
lines = lines.replace('//{', '{')
data = json.loads(lines)

ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})


for course in data:
    if course['youTube'] == '':
        print('skipping "%s" (no playlist)' % course['title'])
        continue
    #print(course)
    url = 'https://www.youtube.com/view_play_list?p=' + course['youTube']
    try:
        result = ydl.extract_info(url, download=False, process=False)
        #print(result)
        entries = list(result['entries'])
        course['playlist'] = entries
        #print(entries)
        for e in entries:
            #r = ydl.extract_info('https://www.youtube.com/watch?v='+e['url'], download=False, process=False)
            #print(r)
            if e['url'] != e['id']:
                print(e)
    except Exception as err:
        print(err)

with open('ucb_webcasts.json', 'w') as o:
    json.dump(data, o, indent=4)
