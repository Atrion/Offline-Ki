# -*- coding: utf-8 -*-
import os, time
from dataserver_file import Flags, PrpFile, OggFile, AgeFile, FniFile


# a list of files belong together somehow
class Manifest:
    def __init__(self, baseFolder, cacheBaseFolder, manifestFilename, ageName, required):
        self.baseFolder = baseFolder
        self.cacheBaseFolder = cacheBaseFolder
        self.manifestFilename = manifestFilename
        self.files = [] # the order is important, at least for some manifests
        self.ageName = ageName
        self.required = required
    
    # Add a file to the manfiest
    def addFile(self, file):
        self.files.append(file)
        file.copyTo(self.baseFolder, self.cacheBaseFolder)
        file.manifests.append(self)
    
    # Write the checked part of the manifest to the given (already opened) file
    def writeChecked(self, file):
        assert self.ageName is not None
        checkedFiles = filter(lambda f: f.flags & Flags.Checked, self.files)
        if not checkedFiles: return # do not add anything if there are no checked files
        if self.required:
            file.write('\nAgeRequired: dat/%s.age\n' % self.ageName)
        else:
            file.write('\nAge: dat/%s.age\n' % self.ageName)
        for f in checkedFiles:
            assert f.flags == Flags.Checked # there must be nothing else set
            self.files.remove(f) # this file is done
            file.write('%s,%d  %s\n' % (f.md5, f.fileSize, f.name))

    # Write the manifest to its file
    def write(self):
        file = open(os.path.join(self.baseFolder, self.manifestFilename), 'w')
        file.write('[version]\nformat=5\n') # write header
        # get the sections
        base = []
        pages = []
        other = []
        for f in self.files:
            # checl some stuff
            assert not (f.flags & Flags.Checked)
            if isinstance(f, OggFile): assert f.flags & Flags.Sound
            else: assert not (f.flags & Flags.Sound)
            # get name and date
            name = f.name
            if isinstance(f, PrpFile): # PrpFile already verified that this starts with dat/
                name = name[len("dat/"):]
            date = time.strftime('%m/%d/%y %H:%M:%S', f.fileDate)
            # get the line to add
            if f.flags & Flags.Compressed:
                line = "%s,%d,%s,%s,%d,%d" % (name, f.fileSize, date, f.md5, f.flags & Flags.Uru, f.compressedSize)
            else:
                line = "%s,%d,%s,%s,%d" % (name, f.fileSize, date, f.md5, f.flags & Flags.Uru)
            # add it to the proper section
            if isinstance(f, PrpFile):
                pages.append(line)
            elif isinstance(f, AgeFile) or isinstance(f, FniFile):
                base.append(line)
            else:
                other.append(line)
        # write sections to file
        file.write('\n[base]\n')
        file.write('\n'.join(base)+'\n')
        file.write('\n[pages]\n')
        file.write('\n'.join(pages)+'\n')
        file.write('\n[other]\n')
        file.write('\n'.join(other)+'\n')
        file.close()