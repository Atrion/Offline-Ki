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
import os, glob, subprocess
from createpak_config import python22_bin, python22_modules, pypack, paths

def getfile(name):
    f = open(name, 'r')
    c = f.read().replace("\r", "")
    f.close()
    return c

def clean_folder(folder):
    for file in glob.iglob(os.path.join(folder, "*.pyc")):
        os.remove(file)

def compile_folder(folder):
    global python22
    # check if the python installation was properly patched
    filename = os.path.join(python22_modules, "py_compile.py")
    pc_compile = getfile(filename)
    if pc_compile.find("\n        return False\n") < 0:
        raise Exception("You have to patch %s to return False in case of a compilation error" % filename)
    # let's go!
    #print "Compiling everything in",folder
    subprocess.check_output([python22_bin, os.path.join(python22_modules, "compileall.py"), '-lf', '.'], cwd=folder)

def pak_folder(folder, pakfile):
    global pypack
    #print "Packing everything in",folder,"to",pakfile
    command = [pypack, '-c']
    files = glob.glob(os.path.join(folder, "*.pyc"))
    if not len(files): raise Exception("No pyc files found in %s" % folder)
    command.extend(files)
    command.append(pakfile)
    subprocess.check_output(command)

def create_pak(folder, pakfile):
    clean_folder(folder) # make sure we don't pack old leftovers
    compile_folder(folder)
    pak_folder(folder, pakfile)
    clean_folder(folder)

def auto_create_pak(folder, name, start = False):
    if name not in paths:
        raise Exception(name+" is not a well-known path")
    (path, startApp) = paths[name]
    pakfile = os.path.split(folder)[-1:][0] # split the path into an array, get the slice with the last elemnt, get that element
    pakfile = os.path.join(path, pakfile)+".pak"
    create_pak(folder, pakfile)
    print "Created pak file",pakfile
    if start: subprocess.check_call(startApp)

if __name__ == '__main__':
    import sys
    if sys.argv[1] == 'auto':
        start = (len(sys.argv) >= 4 and sys.argv[3] == 'start')
        auto_create_pak(os.getcwd(), sys.argv[2], start)
    elif sys.argv[1] == 'rec':
        for file in os.listdir(os.getcwd()):
            if os.path.isfile(file): continue
            if len(glob.glob(os.path.join(file, "*.py"))): # there is at least one *.py file in there
                auto_create_pak(file, sys.argv[2])
    else:
        create_pak(os.getcwd(), sys.argv[1])
        print "Created pak file",sys.argv[1]
