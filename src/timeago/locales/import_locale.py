# coding=utf-8
import codecs
import glob
import json

from git import Repo
import os

import shutil
import re

from subprocess import call

# Note that you have to specify path to script

dest = './jsrepo'

# Clean dest
shutil.rmtree(dest)

if not os.access(dest, os.F_OK):
    os.mkdir(dest)

Repo.clone_from('https://github.com/hustcc/timeago.js.git', dest)

for filename in glob.glob(os.path.join(dest, 'locales/*.js')):
    with open(filename) as f:
        content = f.readlines()
        # We're doing just the basic syntax and we're not trying to understand locale.js which is the index file
        if len(content) > 18 or 'locales.js' in filename:
            print('Seems that %s is a bit too complex for this parser' % filename)
            continue
        print('Generating %s\'s JSON Object...' % filename)
        call(["node", "convert_local_to_json.js", filename])

override = True

for filename in glob.glob('./tmp/*.json'):
    wrong = False
    pure_filename = filename.split('/')[-1:][0][:-5]
    if not override:
        for already_existing in glob.glob('./*.py'):
            if already_existing[2:-3] == pure_filename:
                wrong = True
                break
        if wrong:
            continue
    with open(filename) as g:
        json_value = json.loads(g.read())

        generated_placeholder = []

        for x in json_value['statements']:
            generated_placeholder.append(x[0])
            generated_placeholder.append(x[1])

        txt = \
"""#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017-8-30

@author: generated by @lolobosse script
'''
LOCALE = [
    ["%s", "%s"],
    ["%s", "%s"],
    ["%s", "%s"],
    ["%s", "%s"],
    ["%s", "%s"],
    ["%s", "%s"],
    ["%s", "%s"],
    ["%s", "%s"],
    ["%s", "%s"],
    ["%s", "%s"],
    ["%s", "%s"],
    ["%s", "%s"],
    ["%s", "%s"],
    ["%s", "%s"]
]
        """ % tuple(generated_placeholder)
        with codecs.open(pure_filename+'.py', 'w+', "utf-8") as h:
            h.write(txt)
            h.close()


# Clean
shutil.rmtree('./tmp')
shutil.rmtree(dest)

