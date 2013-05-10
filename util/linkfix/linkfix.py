#!/usr/bin/python
# -*- coding: utf-8 -*-
#==============================================================================#
#                                                                              #
#    Offline KI                                                                #
#                                                                              #
#    Copyright (C) 2008-2011  Diafero                                          #
#                                                                              #
#    This program is free software: you can redistribute it and/or modify      #
#    it under the terms of the GNU General Public License as published by      #
#    the Free Software Foundation, either version 3 of the License, or         #
#    (at your option) any later version, with or (at your option) without      #
#    the Uru exception (see below).                                            #
#                                                                              #
#    This program is distributed in the hope that it will be useful,           #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#    GNU General Public License for more details.                              #
#                                                                              #
#    Please see the file COPYING for the full GPLv3 license, or see            #
#    <http://www.gnu.org/licenses/>                                            #
#                                                                              #
#==============================================================================#
import sys, os
from linkfix_config import java, drizzle, lists, wdir
from createpak import getfile, create_pak, call
allowed = []
fixes = {}
msgs = []

linkingFiles = ['offlineki.pak', 'offlineki2.pak', 'tpots-addons.pak', 'tpots-fixes.pak', 'python.pak'] # pak files allowed to use linking commands
overwritingFiles = ['tpots-addons.pak', 'tpots-fixes.pak'] # pak files allowed to overwrite files
overwrittenFiles = ['python.pak', 'journal.pak'] # pak files allowed to be (partially) overwritten

### useful functions
def remove(name):
    if not os.path.exists(name): return
    if os.path.isfile(name):
        os.remove(name)
    else:
        for file in os.listdir(name):
            remove(os.path.join(name, file))
        os.rmdir(name)

def mayOverwrite(pakfile1, pakfile2):
    global overwritingFiles, overwrittenFiles
    pakfile1 = os.path.basename(pakfile1)
    pakfile2 = os.path.basename(pakfile2)
    if (pakfile1 in overwritingFiles) and (pakfile2 in overwrittenFiles):
        return True
    if (pakfile2 in overwritingFiles) and (pakfile1 in overwrittenFiles):
        return True
    return False

def decompile(pakfile, wdir):
    global drizzle
    call([java, '-DDrizzle.IsLauncher=false', '-Djava.awt.headless=true', '-splash:', '-jar', drizzle, '-decompilepak', pakfile, wdir, 'pots'])
    time.sleep(0.2)

### file processing function (returns True if the file should be recompiled and repacked, throws an exception if a link was left unfixed)
def checkForLink(pyfile, fixIt):
    content = getfile(os.path.join(wdir, pyfile))
    
    # before looking for the linking code, blend out allowed code
    contentFiltered = content
    for allowedStr in allowed:
        contentFiltered = contentFiltered.replace(allowedStr, '')

    # check
    if contentFiltered.find('ptNetLinkingMgr') >= 0:
        # let's see if we have a fix
        if fixIt:
            for fix in fixes:
                content = content.replace(fix, fixes[fix])
        # check if we could fix it or not
        if content.find('ptNetLinkingMgr') >= 0:
            # no or not enough fixes, warn
            raise Exception("Unfixable linking code in "+pyfile)
        else:
            msgs.append('Successfully removed ptNetLinkingMgr usage in '+pyfile)
            # we fixed it! Save the file
            f = open(os.path.join(wdir, pyfile), 'w')
            f.write(content)
            f.close()
            return True
    return False


### pak file processing. Returns a list of contained filenames, throws an exception if a file links
def checkPak(pakfile, fixIt = False, silent = True):
    files = []
    try:
        # get file content
        os.mkdir(wdir)
        decompile(pakfile, wdir)
        
        # check sourcecode
        repack = False
        for pyfile in os.listdir(wdir):
            files.append(pyfile)
            if not silent:
                print "    Processing",pyfile
            if not os.path.basename(pakfile) in linkingFiles: # exclude some files from this check
                repack = checkForLink(pyfile, fixIt) or repack

        if repack:
            if not fixIt: raise Exception("Something went seriously wrong, how can repack be requested if fixes are disabled?")
            create_pak(wdir, pakfile)
            msgs.append("Re-packed "+pakfile+" after linking was fixed")
    finally:
        # cleanup
        remove(wdir)
    return files
    

### initialization
# load list of allowed usages and of fixes
for file in os.listdir(lists):
    if file.startswith('white'):
        allowed.append(getfile(os.path.join(lists, file)))
    elif file.startswith('fix') and not file.startswith('fixed'):
        fix = getfile(os.path.join(lists, file))
        fixed = getfile(os.path.join(lists, file.replace('fix', 'fixed')))
        fixes[fix] = fixed


if __name__ == '__main__':
    ### main program
    # process arguments
    if len(sys.argv) == 1:
        print "Usage: linkfix.py pakfiles"
        exit(0)

    try:
        # check files
        filenames = {}
        for pakfile in sys.argv[1:]:
            # process this file
            print "Processing",pakfile
            files = checkPak(pakfile, fixIt = True, silent = False)
            # check for duplicate files
            for file in files:
                if file in filenames and not mayOverwrite(filenames[file], pakfile):
                    raise Exception(file+" can be found in both "+filenames[file]+" and "+pakfile)
                filenames[file] = pakfile
            print
    except Exception, err:
        print
        # error handling
        msgs.append("ERROR: "+str(err))
        # cleanup after exception
        remove(wdir)

    # print messages
    if len(msgs):
        print "There were %d messages:" % len(msgs)
        for text in msgs:
            print text
    else:
        print "Everything is all right!"
