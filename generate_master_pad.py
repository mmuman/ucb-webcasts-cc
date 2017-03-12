#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright 2017, François Revol <revol@free.fr>
#

import collections
import sys
import urllib.request
import urllib3.filepost
import http.client
import json
import youtube_dl

from html import escape

#HttpHandler = urllib.request.HTTPHandler (debuglevel=1)
#HttpsHandler = urllib.request.HTTPSHandler (debuglevel=1)
#opener = urllib.request.build_opener (HttpsHandler)
#urllib.request.install_opener (opener)

pad_base = 'https://etherpad.wikimedia.org/p' # etherpad base URL

# markdown import doesn't really work in etherpad... let's use HTML
md = ''
html = ''
i = 0

semesters = collections.OrderedDict()
semester = None

do_import_pads = False


with open('ucb_webcasts.json', 'r') as f:
    data = json.load(f)

    for course in data:

        sem = course['semester'].replace(' ', '_')
        if sem not in semesters:
            semesters[sem] = ''
            #md = semesters[sem]
            html = semesters[sem]
            semester = sem

        # most etherpads don't import H1/H2/... correctly
        #md += "# %s\n" % course['title']
        md += "**%s**\n\n" % course['title']
        md += "Department: %s\n\n" % course['dept']
        md += "Semester: %s\n\n" % course['semester']
        md += "Lecturer: %s\n\n" % course['lecturer']
        md += course['descr']
        md += '\n\n'

        html += "<p><strong>%s</strong></p>\n" % escape(course['title'])
        html += "<p>Department: %s</p>\n" % escape(course['dept'])
        html += "<p>Semester: %s</p>\n" % escape(course['semester'])
        html += "<p>Lecturer: %s</p>\n" % escape(course['lecturer'])
        html += '<p><em>' + escape(course['descr']) + '</em></p>'
        #html += '<br />\n'


        #print(course)
        if not 'playlist' in course:
            md += '*(no playlist)*\n\n'
            html += "<p><em>(no playlist)</em></p>\n"
        else:
            url = 'https://www.youtube.com/view_play_list?p=' + course['youTube']
            md += 'Playlist: https://www.youtube.com/view_play_list?p=' + course['youTube'] + '\n\n'
            html += '<p>Playlist: <a href="%s">%s</a></p>\n' % (escape(url), url)
            for item in course['playlist']:
                url = 'https://www.youtube.com/watch?v=%s' % item['url']
                padurl = '%s/UCB_Webcasts_CC_%s' % (pad_base, item['url'])
                #md += "## %s\n" % item['title']
                md += "**_%s_**\n\n" % item['title']
                md += 'URL: %s\n\n' % url
                md += 'Pad: %s/UCB_Webcasts_CC_%s\n\n' % (pad_base, item['url'])
                md += 'Done: 0%\n\n'
                md += 'Takers: \n\n'
                md += '\n'

                html += "<p><strong><em>%s</em></strong></p>\n" % escape(item['title'])
                html += '<p>URL: <a href="%s">%s</a></p>\n' % (escape(url), url)
                html += '<p>Pad: <a href="%s">%s</a></p>\n' % (escape(padurl), padurl)
                html += '<p>Status: unknown</p>\n'
                html += '<p>Done: 0%</p>\n'
                html += '<p>Takers: </p>\n'
                html += '<br/>\n'

        md += '\n\n'
        md += '\n\n'
        html += '<br/>\n'
        html += '<br/>\n'

        # XXX: testing...
        i+=1
        #if i == 5:
        #    break;
        #semesters[semester] = md
        semesters[semester] = html

    #print(md)

master = '<p><strong>Semester pads:</strong></p>\n'
for s in semesters:
    padurl = '%s/UCB_Webcasts_CC_%s' % (pad_base, s)
    html = '<!doctype html>\n<html lang="en">\n<head>\n<title>UCB_Webcasts_CC_%s</title>\n</head>\n<body>\n' % s
    html += semesters[s]
    html += '</body>\n</html>\n'
    #with open('pad_'+s+'.md', 'w') as o:
    with open('pad_'+s+'.html', 'w') as o:
        o.write(html)
    master += '<p>Pad: <a href="%s">%s</a></p>\n' % (escape(padurl), padurl)
    if (do_import_pads):
        data = { 'file': ('pad_'+s+'.html', html, 'text/html') }
        #data = urllib.urlencode(data)
        data, content_type = urllib3.filepost.encode_multipart_formdata(data)
        #print(data)
        #print(content_type)
        print('Importing pad to %s' % padurl)
        req = urllib.request.Request(url=padurl + '/import', data=data, headers={'Content-Type': content_type})
        #print(req.get_method())
        #print(vars(req))
        try:
            with urllib.request.urlopen(req) as f:
                print('Importing pad: %s' % f.getcode())
                #print(f.info())
                #print(f.read())
                #print(vars(f))
        except Exception as err:
            print(err)

with open('master_pad.html', 'w') as o:
    o.write(master)
