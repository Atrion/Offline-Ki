#!/usr/bin/python -u
# -*- coding: utf-8 -*-
import os, shutil, glob, cPickle as pickle, re
import linkfix
from dataserver_file import Flags, File, loadFile, PrpFile, OggFile, PakFile, AgeFile
from dataserver_manifest import Manifest

# settings
import create_dataserver_config as config

#===================================================================================================================================
# create a manifest for the given base folder
def createManifest(folder, file, ageName = None, required = False):
	return Manifest(os.path.join(config.kTmpPath, folder), os.path.join(config.kResultPath, folder), file, ageName, required)


# prints a headline
def printCaption(text):
	print '='*len(text)
	print text
	print '='*len(text)


# load a list from a file
def loadList(file, lowerCase = False):
	list = []
	for line in file:
		if not line: continue
		if line.startswith('#'): continue
		if lowerCase: line = line.lower()
		list.append(line.strip())
	return list

#===================================================================================================================================
class Dataserver:
	installManifest = None # the manifest requested by UruSetup directly after startup
	clientManifest = None # the manifest containing all the global client files (downloaded after hitting "Play")
	ageManifests = {} # maps lower-case age names to age manifests
	allFiles = {} # maps lower-case filenames to their file objects
	oldCache = None # the old cache file (information about the state of the files)
	
	kCacheFile = 'create-dataserver-cache'
	kCacheFileVersion = 3
	
	# loads the cache from the given file
	def loadCache(self):
		self.oldCache = {}
		try:
			cache = pickle.load(open(os.path.join(config.kResultPath, self.kCacheFile), 'r'))
			if type(cache) == type({}) and cache.get('version') == self.kCacheFileVersion: # correct cache version
				self.oldCache = cache
		except IOError:
			pass
		# anything went wrong: no cache


	# saves the cache to the given file
	def saveCache(self):
		cache = {'version': self.kCacheFileVersion}
		# add all the file's cache info
		for file in self.allFiles.values():
			assert file.name != 'version' # that would be rather fatal, obviously
			cache[file.name] = file.getCacheData()
		# store it
		pickle.dump(cache, open(os.path.join(config.kTmpPath, self.kCacheFile), 'w'))


	# Adds the files to the given manifest.
	# manifest may be None, then files will be added to the age the age they belong to
	# uruStarterOptions may contain "checked" for prp files to be only checked, not copied to the dataserver, and "required" for that check to
	#   only succeed if the file actually exists (por default, such a file is optional)
	# if patternsMustMatch is True, an exception will be thrown when a pattern/filename does not match any file
	def addToManifest(self, files, manifest, uruStarterOptions = [], patternsMustMatch = True):
		duplicateFiles = []
		prpFilesOnlyChecked = "checked" in uruStarterOptions
		agesRequired = "required" in uruStarterOptions
		# add all the files
		for pattern in files:
			globbed = filter(os.path.isfile, glob.glob(pattern)) # get all files matching the pattern
			if patternsMustMatch and not globbed:
				raise Exception("No file matches pattern "+pattern)
			for filename in sorted(globbed, key=str.lower):
				# let's get the file info
				file = self.allFiles.get(filename.lower())
				if file is not None:
					# A known file. Make sure we mean the same one!
					if file.absName != os.path.abspath(filename):
						duplicateFiles.append("File {0} is already on the dataserver, conflicting with {1}".format(file.absName, os.path.abspath(filename)))
				else: # we have not yet seen this file
					# get some base info
					print "Processing %s..." % filename
					cache = self.oldCache.get(filename, {}) # get cache info for this file
					basename = os.path.basename(filename)
					type = basename[basename.rfind('.')+1:] # get file extension
					# load the file with the correct main manifest flag (uncompressed, compressed, checked)
					if prpFilesOnlyChecked and type == 'prp':
						file = File(filename, cache, Flags.Checked) # treat these checked prp files as fils we don't know anything about - we don't even want to check their consistency
					elif type in config.kUncompressed:
						file = loadFile(filename, cache, Flags.Uncompressed) # get correct file depending on the type
					elif type in config.kCompressed:
						file = loadFile(filename, cache, Flags.Compressed) # get correct file depending on the type
					else: # unknown
						raise Exception('Unknown file type: {0}'.format(filename))
					self.allFiles[filename.lower()] = file
				# add the file to the correct manifest
				if manifest is None: # no manifest given, we have to find out ourselves
					# sound files are special: we do not yet know the age!
					if type == 'ogg':
						continue # we will copy them later
					elif type in ('prp', 'age', 'fni', 'csv'):
						age = basename[:basename.rfind('.')] # the part before the last .
						age = age[age.rfind('/')+1:] # the part after the last /
						if type == 'prp':
							pos = age.find('_District_')
							if pos < 0: raise Exception("prp file without _District_: {0}".format(file))
							age = age[:pos] # the part before the _District_
					elif type == 'p2f':
						age = 'GUI' # not that nice, but got a better idea?
					else:
						raise Exception("Can not automatically find out the age for {0}".format(file))
					# get that age's manifest
					ageManifest = self.ageManifests.get(age.lower())
					if ageManifest is None:
						ageManifest = self.ageManifests[age.lower()] = createManifest('game_data', 'dat/'+age+'.mfs', age, agesRequired)
					else:
						assert ageManifest.ageName == age # this check is case-sensitive
						ageManifest.required = ageManifest.required or agesRequired # require an age if at least one file is required
					ageManifest.addFile(file)
				else:
					manifest.addFile(file)
		if duplicateFiles:
			raise Exception('\n'.join(duplicateFiles))


	# add all files from the given package
	def addPackage(self, package):
		# switch into this package's source directory
		oldCwd = os.getcwd()
		os.chdir(os.path.join(config.kSourcePath, package))
		# load age set properties
		if os.path.exists('options'):
			options = loadList(open('options'), lowerCase = True)
		else:
			options = ()
		# Add global files to client (including subfolders of img, for Relto pages and age information)
		self.addToManifest(('Python/*', 'SDL/*', 'ageresources/*', 'readme/*', 'avi/*', 'img/*', 'img/*/*'), self.clientManifest, patternsMustMatch = False)
		# Add age files to data part
		self.addToManifest(('dat/*', 'sfx/*'), manifest = None, uruStarterOptions = options, patternsMustMatch = False)
		# restore working directory
		os.chdir(oldCwd)


	# add the sound files to the manifest files of the ages they are used in
	def addSoundFilesToManifests(self):
		missingFiles = set()
		# for all prp files, add the sound files used there to their manifest
		for f in self.allFiles.values():
			if not isinstance(f, PrpFile): continue # we care only about prp files
			for s in f.soundFiles:
				soundFile = self.allFiles.get('sfx/'+s.lower())
				if soundFile is None:
					if s not in config.kSoundMissing:
						missingFiles.add(s)
				else:
					# add the flags of this occurence
					soundFile.flags |= f.soundFiles[s]
					# and add the sound file to the manifest of the prp file
					assert len(f.manifests) == 1
					f.manifests[0].addFile(soundFile)
		# check if files are missing
		if missingFiles:
			raise Exception("Missing sound files: " + str(sorted(missingFiles, key=str.lower)))


	# check for orphaned sound files
	def checkForOrphanedSoundFiles(self):
		orphanedFiles = set()
		# check that all sound files are in some manifest, and make sure every sound file which is decompressed is in some auto-loaded age
		GUIManifest = self.ageManifests['gui']
		assert GUIManifest.ageName in config.kAutoloadAges # an assumption used below
		for f in self.allFiles.values():
			if not isinstance(f, OggFile): continue # only care about sound files
			if f.manifests:
				if f.flags & (Flags.LeftRightWav | Flags.SingleWav): # checks if either bit is set
					# the file is in some manifest. Look for an auto-loaded age
					fileIsLoaded = False
					# check if this file is loaded by an auto-loaded age. If not, make sure it is to work around a decompression issue.
					for m in f.manifests:
						if m.ageName in config.kAutoloadAges:
							fileIsLoaded = True
							break
					# if it is not auto-loaded, add it to the GUI
					if not fileIsLoaded:
						GUIManifest.addFile(f)
			else:
				# this sound file is orphaned
				assert f.name.startswith('sfx/')
				name = f.name[len('sfx/'):]
				if name not in config.kSoundOrphaned:
					orphanedFiles.add(name)
				#assert not (f.flags & Flags.Sound) # no sound-related flag can be set
				f.flags |= Flags.NoWav
				GUIManifest.addFile(f) # add it to the GUI
		# check if files are orphaned
		if orphanedFiles:
			print "WARNING: Orphaned sound files: " + str(sorted(orphanedFiles, key=str.lower))


	# Check if we found all Python files, and none twice
	def checkPythonFiles(self):
		# first pass: check which python files exist where
		pythonFiles = {} # maps a lower-case file name to the pak file providing it
		pythonModuleNames = set() # a set of all python files seen, in their proper case
		for f in self.allFiles.values():
			if not isinstance(f, PakFile): continue # only care about python files
			for p in f.files:
				otherPak = pythonFiles.get(p.lower())
				if otherPak is None:
					pythonFiles[p.lower()] = f
					pythonModuleNames.add(p)
				elif not linkfix.mayOverwrite(f.name, otherPak.name): # check if this is okay
					raise Exception("{0} is both in {1} and {2}".format(p, f.name, otherPak.name))
		del pythonFiles
		# pass two: check if all python files used by the prp files are present
		for f in self.allFiles.values():
			if not isinstance(f, PrpFile): continue # we only care about prp files
			for p in f.pythonFiles:
				if p not in pythonModuleNames and p not in config.kPythonMissing:
					raise Exception("Python file {0} used by {1} does not exist.".format(p, f.name))


	# make sure all prefixes are registered
	def checkSequencePrefixes(self):
		# first load the list
		file = open(config.kSequencePrefixes)
		registeredPrefixes = {}
		for line in file:
			# get prefix and name
			m = re.search('^\|\|?(-?[0-9]+)\|\|([a-zA-Z0-9][a-zA-Z0-9_-]+)\|\|.*\|\|.*', line)
			if m is None: continue # not a line we are interested in
			prefix = int(m.groups()[0])
			name = m.groups()[1]
			# filter out some lines dealing with conflicts we know of - the resulting hashmap will not contain any prefix twice, so that is verified to be right on the dataserver
			# plus, the dataserver ensures that no two ages have the same filename by its duplicate check
			if name in ('Tochoortahv', 'Guerr'): continue
			# finally add the age
			registeredPrefixes[prefix] = name
		# now check all .age files
		for f in self.allFiles.values():
			if not isinstance(f, AgeFile): continue # ognore everything but age files
			registeredName = registeredPrefixes.get(f.sequencePrefix)
			if registeredName is None: raise Exception("Age %s with prefix %d not registered" % (f.name, f.sequencePrefix))
			if "dat/{0}.age".format(registeredName) != f.name:
				raise Exception("Age %s registered for prefix %d, but we have that prefix in %s" % (registeredName, f.sequencePrefix, f.name))



	# manifest write functions (expects the working directory to be the original base folder)
	def writeManifests(self):
		# first write the checked whitelist
		file = open(config.kChecksumFile, 'w')
		for age in self.ageManifests.values():
			age.writeChecked(file)
		file.close()
		# now the normal whitelist
		shutil.copyfile(config.kWhitelistTemplate, config.kWhitelistFile)
		file = open(config.kWhitelistFile, 'a')
		file.write('\n')
		for f in self.allFiles.values():
			if not f.flags & Flags.Checked: # checked file are already on the other whitelist
				file.write(f.name+'\n')
				if f.name.endswith(".age"):
					file.write(f.name[:-len(".age")]+'.sum\n')
		file.write(config.kChecksumFile+'\n') # this file is not yet on the dataserver, so add it manually
		file.write(config.kWhitelistFile+'\n') # same for this one
		file.close()
		# add these whitelists to the dataserver
		self.addToManifest([config.kWhitelistFile, config.kChecksumFile], self.clientManifest)
		# and write the manifests
		self.installManifest.write()
		self.clientManifest.write()
		for age in self.ageManifests.values():
			age.write()
		# Write list of ages to be updated on startup
		file = open(os.path.join(config.kTmpPath, 'game_data/dat/agelist.txt'), 'w')
		for age in config.kAutoloadAges:
			manifest = self.ageManifests.get(age.lower())
			if manifest is None or manifest.ageName != age: # also compare the case
				raise Exception('Age %s should be automatically loaded, but it does not exist' % age)
			file.write(age+'\n')
		file.close()

#===================================================================================================================================
	def create(self):
		# cd to source directory
		os.chdir(config.kSourcePath)
		# load old cache
		self.loadCache()
		# Prepare the temporary location for new result
		if os.path.exists(config.kTmpPath): shutil.rmtree(config.kTmpPath)
		os.mkdir(config.kTmpPath)
		# Prepare the global manifests
		self.installManifest = createManifest('install/Expanded', 'ClientSetupNew.mfs')
		self.clientManifest = createManifest('game_clients/drcExplorer', 'client.mfs')

		# first, we have to generate the installer part
		printCaption("Processing installer")
		self.addToManifest(config.kInstallerFiles, self.installManifest)
		print

		# now get the main client files and the in-game configuration
		printCaption("Processing main client")
		self.addToManifest(config.kClientFiles, self.clientManifest)
		print

		# process packages
		for pattern in config.kPackageFolders:
			globbed = glob.glob(pattern)
			if not globbed: raise Exception("No folder matches pattern "+pattern)
			for folder in sorted(globbed, key=str.lower): # sort ages by name
				printCaption("Processing %s" % folder)
				self.addPackage(folder)
				print


		# Finalization
		printCaption("Finalizing dataserver")
		self.saveCache() # Now that we processed all files, save the cache (before an exception makes us loose all data)
		# Collect the info we gathered
		print "Checking some consistencies..."
		self.checkPythonFiles()
		self.checkSequencePrefixes()
		print "Dealing with sound files..."
		self.addSoundFilesToManifests()
		self.checkForOrphanedSoundFiles()
		# write the age manifests
		print "Writing Manifests..."
		self.writeManifests()
		# kTmpPath now holds the dataserver, let's remove the old cruft and move ours there
		print "Moving files to destination..."
		if os.path.exists(config.kResultPath): shutil.rmtree(config.kResultPath)
		os.rename(config.kTmpPath, config.kResultPath)

#===================================================================================================================================
if __name__ == "__main__":
	Dataserver().create()
