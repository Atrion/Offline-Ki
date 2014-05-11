# -*- coding: utf-8 -*-
import os, sys, time, subprocess, shutil, re
import PyHSPlasma, linkfix
kChunksize = 1024*1024 # chunksize of 1MiB (for MD5sum generation)
kCompressionExtension = '.gz' # extension addes by gzip

# PyHSPlasma init
PyHSPlasma.plDebug.Init(PyHSPlasma.plDebug.kDLError)
plResMgr = PyHSPlasma.plResManager()

def plGetVersionName(v):
    if v == PyHSPlasma.pvPrime: return "Prime/UU"
    elif v == PyHSPlasma.pvPots: return "PotS/CC"
    elif v == PyHSPlasma.pvMoul: return "MOUL/MQO"
    elif v == PyHSPlasma.pvEoa: return "Myst V/Crowthislte"
    elif v == PyHSPlasma.pvHex: return "Hex Isle"
    elif v == PyHSPlasma.pvUniversal: return "Universal"
    elif v < PyHSPlasma.pvPrime: return "Choru"
    elif v > PyHSPlasma.pvPots and v < PyHSPlasma.pvMoul: return "MOUL Beta"
    else: return "Unknown"

# factory
def loadFile(file, cacheData, flag):
    type = file[file.rfind('.')+1:] # get file extension
    if type == 'prp':
        return PrpFile(file, cacheData, flag)
    elif type == 'age':
        return AgeFile(file, cacheData, flag)
    elif type == 'ogg':
        return OggFile(file, cacheData, flag)
    elif type == 'fni':
        return FniFile(file, cacheData, flag)
    elif type == 'pak':
        return PakFile(file, cacheData, flag)
    else:
        return File(file, cacheData, flag)


# container for the flags
class Flags:
    LeftRightWav = 1 << 0
    NoWav = 1 << 1
    SingleWav = 1 << 2
    Compressed = 1 << 3
    Sound = LeftRightWav|NoWav|SingleWav # all sound-related bits
    Uru = Sound|Compressed # bits known by Uru
    # some more flags for internal tracking
    Uncompressed = 1 << 4
    Checked = 1 << 5


# A file with no special properties whatsoever
class File:
    def __init__(self, file, cacheData, flag):
        if flag not in (Flags.Compressed, Flags.Uncompressed, Flags.Checked):
            raise Exception("Invalid flag {0} for file {1}".format(flag, file))
        self.flags = flag
        self.manifests = []
        # get file info
        os.chmod(file, 0644)
        self.name = file
        self.absName = os.path.abspath(file)
        self.fileSize = os.path.getsize(file) # get file size
        self.fileDate = time.gmtime(os.stat(file).st_mtime) # get last change date
        # check if we can trust the cache
        self.validCache = (self.fileSize == cacheData.get('size') and self.fileDate == cacheData.get('date'))
        if not self.validCache: # we can not
            cacheData.clear() # don't use anything (the caller will see it as empty as well!)
        # we also need the checksum
        self.md5 = cacheData.get('md5')
        if self.md5 is None: # checksum not cached
            self.displayStartWorking("Calculating checksum")
            self.md5 = self.md5sum()
            self.displayDoneWorking()
    
    # returns the data ot be cached for this file
    def getCacheData(self):
        return { 'size': self.fileSize, 'date': self.fileDate, 'md5': self.md5 }
    
    # copy the file to the dataserver!
    def copyTo(self, baseFolder, cacheBaseFolder):
        # copy the file to where we need it
        targetFile = os.path.join(baseFolder, self.name)
        cacheTargetFile = os.path.join(cacheBaseFolder, self.name)
        targetDir = os.path.dirname(targetFile)
        if not os.path.isdir(targetDir): os.makedirs(targetDir) # make sure the directory exists
        if self.flags & Flags.Compressed and not os.path.isfile(targetFile + kCompressionExtension): # the file might be in a different manifest already
            # we need the gz file in the target
            if self.validCache and os.path.isfile(cacheTargetFile + kCompressionExtension): # use cached file
                os.link(cacheTargetFile + kCompressionExtension, targetFile + kCompressionExtension)
            else: # compress source file
                self.displayStartWorking("Compressing file")
                shutil.copy2(self.absName, targetFile)
                subprocess.check_call(['gzip', targetFile])
                self.displayDoneWorking()
            # we need the compressed filesize
            self.compressedSize = os.path.getsize(targetFile+kCompressionExtension)
        elif self.flags & Flags.Uncompressed and not os.path.isfile(targetFile):
            # we need the original file in the target
            if self.validCache and os.path.isfile(cacheTargetFile): # use cached file
                os.link(cacheTargetFile, targetFile)
            else: # copy source file
                self.displayStartWorking("Copying file")
                shutil.copy2(self.absName, targetFile)
                self.displayDoneWorking()

    def md5sum(self):
        import hashlib
        file = open(self.absName, 'rb')
        sum = hashlib.md5()
        # hash the whole file
        while True:
            chunk = file.read(kChunksize)
            if not chunk: break # file done
            sum.update(chunk)
        file.close()
        return sum.hexdigest()
    
    # small helpers
    def displayStartWorking(self, str):
        print "    "+self.name+": "+str+"...\r",
        sys.stdout.flush()
    def displayDoneWorking(self):
        print " "*99+"\r",
        sys.stdout.flush()


# An age file: also has a sequence prefix
class AgeFile(File):
    def __init__(self, file, cacheData, flag):
        File.__init__(self, file, cacheData, flag)
        assert flag != Flags.Checked # just checking them is invalid
        # get the age's sequence prefix
        self.sequencePrefix = cacheData.get('sequence-prefix')
        if self.sequencePrefix is None: # sequence prefix not cached
            self.displayStartWorking("Reading AGE file")
            self.sequencePrefix = self.getSequencePrefix()
            self.displayDoneWorking()
    
    def getCacheData(self):
        cache = File.getCacheData(self)
        cache['sequence-prefix'] = self.sequencePrefix
        return cache

    def getSequencePrefix(self):
        sequencePrefix = None
        # read the file and get sequence prefix
        stream = PyHSPlasma.plEncryptedStream()
        stream.open(self.name, PyHSPlasma.fmRead, PyHSPlasma.plEncryptedStream.kEncXtea)
        while not stream.eof():
            line = stream.readLine()
            if line.startswith("SequencePrefix="):
                if sequencePrefix is not None: raise Exception("Two sequence prefixes in age file %s" % file)
                sequencePrefix = int(line[len("SequencePrefix="):]) # the number after the =
        stream.close()
        # now check if this prefix exists
        if sequencePrefix is None: raise Exception("No sequence prefix in age file %s" % file)
        return sequencePrefix


# A prp file: load age- and pagename, sound information and python information, and perform some checks by the way
class PrpFile(File):
    def __init__(self, file, cacheData, flag):
        File.__init__(self, file, cacheData, flag)
        # check if we can get everything from the cache
        self.soundFiles = cacheData.get("sound")
        self.pythonFiles = cacheData.get("python")
        # if not, get it ourselves
        if self.soundFiles is None or self.pythonFiles is None:
            self.displayStartWorking("Reading PRP file")
            self.loadPrpInfo() # side-effect: throws exception if there is invalid stuff in there
            self.displayDoneWorking()
    
    def getCacheData(self):
        cache = File.getCacheData(self)
        cache['sound'] = self.soundFiles
        cache['python'] = self.pythonFiles
        return cache
    
    def loadPrpInfo(self):
        page = plResMgr.ReadPage(self.name)
        self.soundFiles = {} # a map of sound filenames to the flags used by the age
        self.pythonFiles = [] # a list of python files used by the age
        if page.location.version != PyHSPlasma.pvPots:
            raise Exception("{0} is not a URU:CC/POTS file, it's for {1}".format(self.name, plGetVersionName(page.location.version)))
        isFanAge = (page.location.prefix >= 100 and page.location.prefix != 1168) or page.location.prefix == 61 # 61 is vothol, 1168 is NeighborhoodMOUL
        # verify the filename
        if self.name != "dat/{0}_District_{1}.prp".format(page.age, page.page):
            raise Exception("{0} contains age {1}, page {2}".format(self.name, page.age, page.page))
        # check for sound files: Code here is based on sounddecompres script script from libHSPlasma
        for key in plResMgr.getKeys(page.location, PyHSPlasma.plFactory.kSoundBuffer):
            soundBuffer = key.object
            flags = self.soundFiles.get(soundBuffer.fileName, 0) # default to 0
            # get the new flags
            if (soundBuffer.flags & soundBuffer.kStreamCompressed): flags |= Flags.NoWav
            else: # uncompressed
                if (soundBuffer.flags & soundBuffer.kOnlyRightChannel) or (soundBuffer.flags & soundBuffer.kOnlyLeftChannel):
                    flags |= Flags.LeftRightWav
                elif flags == 0:
                    flags |= Flags.SingleWav
            # store the flags
            self.soundFiles[soundBuffer.fileName] = flags
        if isFanAge: # perform some checks for fan-ages only
            # linking responder check
            for key in plResMgr.getKeys(page.location, PyHSPlasma.plFactory.kResponderModifier):
                obj = key.object
                if obj is None: continue # object is in the keyring, but it does not actually exist
                for state in obj.states:
                    for command in state.commands:
                        if isinstance(command.msg, PyHSPlasma.plLinkToAgeMsg):
                            als = command.msg.ageLink
                            # kBasicLink = 0, kOriginalBook = 1, kOwnedBook = 3
                            linkIsGood = (als.linkingRules == 0)
                            if not linkIsGood: 
                                raise Exception("%s contains an invalid link to %s in object %s" % (file, als.ageInfo.ageFilename, key))
            # Python file check
            for key in plResMgr.getKeys(page.location, PyHSPlasma.plFactory.kPythonFileMod):
                obj = key.object
                # some basic checks
                if obj.filename.find('.') >= 0:
                    raise Exception("Invalid python file name %s on page %s" % (obj.filename, file))
                if not len(obj.filename):
                    raise Exception("Invalid empty python file name on page %s" % file)
                if key.name == "VeryVerySpecialPythonFileMod": # many of these are missing, so ignore them all
                    if page.page != "BuiltIn":
                        raise Exception("Found %s on page %s" % (key.name, file))
                    if obj.filename != page.age:
                        raise Exception("Found %s for %s in %s" % (key.name, obj.filename, file))
                    continue
                # add file to list
                name = obj.filename+".py" # remember to attach the file ending
                if not name in self.pythonFiles: # do not add files twice, that'd just blow up the cache
                    self.pythonFiles.append(name)
        # done
        plResMgr.UnloadPage(page.location)


# A sound file: this makes them quicker to distinguish
class OggFile(File):
    def __init__(self, file, cacheData, flag):
        File.__init__(self, file, cacheData, flag)
        assert flag == Flags.Uncompressed # compressing these with gzip or just checking them is invalid


# An age configuration file
class FniFile(File):
    def __init__(self, file, cacheData, flag):
        File.__init__(self, file, cacheData, flag)
        if not 'fni' in cacheData:
            self.displayStartWorking("Reading FNI file")
            self.checkFniFile() # throws an exception if the file is invalid
            self.displayDoneWorking()
    
    def getCacheData(self):
        cache = File.getCacheData(self)
        cache['fni'] = True
        return cache
    
    def checkFniFile(self):
        # remember what we found and what not
        foundFogColor = False
        foundFogGradient = False
        foundClearColor = False
        # now go and look for it
        stream = PyHSPlasma.plEncryptedStream()
        stream.open(self.name, PyHSPlasma.fmRead, PyHSPlasma.plEncryptedStream.kEncXtea)
        while not stream.eof():
            line = stream.readLine()
            line = re.sub(r'\s+', ' ', line.strip()).lower() # normalize whitespaces and capitalization
            if line == "graphics.renderer.fog.setdeflinear 0 0 0": # fog entirely disabled, that's okay too
                foundFogGradient = True
                foundFogColor = True
            elif line.startswith("graphics.renderer.fog.setdeflinear ") or line.startswith("graphics.renderer.fog.setdefexp2 ") or line.startswith("graphics.renderer.fog.setdefexp "):
                if foundFogGradient: raise Exception("%s has several gradient specifications" % self.name) # if someone sets the gradient to "0 0 0" and later to something else, we might miss that no color is set^
                foundFogGradient = True
            elif line.startswith("graphics.renderer.fog.setdefcolor"):
                foundFogColor = True
            elif line.startswith("graphics.renderer.setclearcolor"):
                foundClearColor = True
        stream.close()
        # check if we found it all
        if not (foundClearColor and foundFogColor and foundFogGradient):
            raise Exception("%s does not contain all the necessary fog settings" % self.name)


# A python pack file
class PakFile(File):
    def __init__(self, file, cacheData, flag):
        File.__init__(self, file, cacheData, flag)
        self.files = cacheData.get('files')
        if self.files is None:
            self.displayStartWorking("Reading PAK file")
            self.files = linkfix.checkPak(self.name) # side-effect: throws exception if there is a link in there
            self.displayDoneWorking()
    
    def getCacheData(self):
        cache = File.getCacheData(self)
        cache['files'] = self.files
        return cache
