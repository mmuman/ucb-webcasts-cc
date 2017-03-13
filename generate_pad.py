#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright 2017, François Revol <revol@free.fr>
#

import collections
import sys
#import urllib.request
import urllib.request
import urllib3.filepost
import json
import youtube_dl

from html import escape

#HttpHandler = urllib.request.HTTPHandler (debuglevel=1)
#HttpsHandler = urllib.request.HTTPSHandler (debuglevel=1)
#opener = urllib.request.build_opener (HttpsHandler)
#urllib.request.install_opener (opener)

pad_base = 'https://etherpad.wikimedia.org/p' # etherpad base URL

i = 0

semesters = collections.OrderedDict()
semester = None

do_write_cc = False
do_import_pads = False
do_import_all = False
do_import_semester = None
do_import = []
# TODO:
# start again at
# Computer Science 61C
# OrrIbXqfu4U

if ('-a' in sys.argv):
    do_import_all = True
elif ('-s' in sys.argv):
    do_import_semester = sys.argv[sys.argv.index('-s') + 1]
else:
    do_import = sys.argv[1:]

#print(do_import_all)
#print(do_import_semester)
#print(do_import)

ydl_opts = {
    'outtmpl': '%(id)s%(ext)s',
    #'verbose': True,
    #'dump_single_json': True,
    #'listsubtitles': True
    'skip_download': True,
    'writesubtitles': True,
    'writeautomaticsub': True
}

ydl = youtube_dl.YoutubeDL(ydl_opts)

with open('ucb_webcasts.json', 'r') as f:
    data = json.load(f)

    for course in data:

        sem = course['semester'].replace(' ', '_')
        if (not 'playlist' in course):
            continue
        if (do_import_semester and (do_import_semester != sem)):
            continue
        for v in course['playlist']:
            padurl = '%s/UCB_Webcasts_CC_%s' % (pad_base, v['url'])
            if (not do_import_all and not do_import_semester and not v['url'] in do_import and not padurl in do_import):
                continue

            print('Generating pad for video "%s"...' % v['url'])

            url = 'https://www.youtube.com/watch?v=' + v['url']

            # find close-caption
            # prefer real one over automatically-generated one
            result = ydl.extract_info(url, download=False, process=True)
            #print(json.dumps(result, indent=4))
            suburl = None
            source = None
            if ('en' in result['automatic_captions']):
                #print('AUTO:'+str(result['automatic_captions']['en']))
                for fmt in result['automatic_captions']['en']:
                    if (fmt['ext'] == 'vtt'):
                        suburl = fmt['url']
                        source = 'Auto-CC'
            if ('en' in result['subtitles']):
                #print('SUB:'+str(result['subtitles']['en']))
                for fmt in result['automatic_captions']['en']:
                    if (fmt['ext'] == 'vtt'):
                        suburl = fmt['url']
                        source = 'CC'

            if (not suburl):
                print('>> No CC found for %s ; skipping...' % v['url'])
                continue
            print('>> Found %s for %s' % (source, v['url']))


            try:
                t = '# Source: %s Status: unknown\n' % source
                cc = ''
                with urllib.request.urlopen(suburl) as f:
                    cc = f.read().decode('utf-8')
                t += cc

                if (do_write_cc):
                    with open('UCB_Webcasts_CC_%s.vtt' % v['url'], 'w') as o:
                        o.write(cc)
                if (do_import_pads):
                    data = { 'file': ('pad_'+v['url']+'.txt', t, 'text/plain') }
                    data, content_type = urllib3.filepost.encode_multipart_formdata(data)
                    print('Importing pad to %s' % padurl)
                    req = urllib.request.Request(url=padurl + '/import', data=data, headers={'Content-Type': content_type})
                    with urllib.request.urlopen(req) as f:
                        print('Importing pad to %s : %s' % (padurl, f.getcode()))
            except Exception as err:
                print('>>> ERROR:' + str(err))
