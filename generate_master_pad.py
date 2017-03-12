#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright 2017, François Revol <revol@free.fr>
#

import sys
import urllib.request
import json
import youtube_dl

pad_base = '' # etherpad base URL

md = ''
i = 0

with open('ucb_webcasts.json', 'r') as f:
    data = json.load(f)

    for course in data:
        md += "# %s\n" % course['title']
        md += "Department: %s\n\n" % course['dept']
        md += "Semester: %s\n\n" % course['semester']
        md += "Lecturer: %s\n\n" % course['lecturer']
        md += course['descr']
        md += '\n\n'


        #print(course)
        if not 'playlist' in course:
            md += '*(no playlist)*\n\n'
        else:
            md += 'Playlist: https://www.youtube.com/view_play_list?p=' + course['youTube'] + '\n\n'
            for item in course['playlist']:
                md += "## %s\n" % item['title']
                md += 'URL: https://www.youtube.com/watch?v=%s\n\n' % item['url']
                md += 'Pad: %s/UCB_Webcasts_CC_%s\n\n' % (pad_base, item['url'])
                md += 'Done: 0%\n\n'
                md += '\n'

        md += '\n\n'

        # XXX: testing...
        i+=1
        #if i == 5:
        #    break;


    #print(md)

with open('master_pad.md', 'w') as o:
    o.write(md)
