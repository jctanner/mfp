#!/usr/bin/python

import pdb
import rpmfluff
import magic
import tarfile
import os
import sys
import fetchsources
import tempfile
import glob
import shutil

#packagename = "test"

class RpmPackage(object): 
    def __init__(self):
        self.packageobj = rpmfluff.SimpleRpmBuild(self.name, 
                                                self.version, 
                                                self.release)
        if hasattr(self, 'buildrequires'):
            for br in self.buildrequires:
                self.packageobj.add_build_requires(br)

        #description, group, license, packager, summary, url
        try:
            self.packageobj.basePackage.description = self.description
            self.packageobj.basePackage.group = self.group
            self.packageobj.license = self.license
            self.packageobj.packager = self.packager
            self.packageobj.basePackage.summary = self.summary
            self.packageobj.url = self.url
        except:
            pass

        #import epdb; epdb.st()
        self.builddir = tempfile.mkdtemp()
        print "> buildir: %s" % self.builddir
        os.chdir(self.builddir)
        #os.chdir('/tmp')

    def setup(self,args):
        print "class setup"

    def build(self, args):
        print "building ..."

        #pdb.set_trace()

        if args.verbose:
            print "> verbose mode on"

        if args.speconly:
            print "> speconly mode on"

        print ""
        print "> package name:" , str(self.name)
        print "> package version:" , str(self.version)
        print "> package release:" , str(self.release)

        self.setup()
        #pdb.set_trace()
        if args.speconly:
            self.packageobj.gather_spec_file('')
            self._copySpecToRpmbuild()
        else:
            self.packageobj.make()

    def _copySpecToRpmbuild(self):
        specdir = os.path.join(os.environ['HOME'], 'rpmbuild', 'SPECS')
        assert os.path.isdir(specdir), "please create %s" % specdir    
        for filename in glob.glob(os.path.join(self.builddir, '*.spec')):
            shutil.copy(filename, specdir)
            #import epdb; epdb.st()
            print "> ", os.path.join(specdir, os.path.basename(filename))

    def Create(self, filename, contents, dir):
        fakefile = rpmfluff.SourceFile(filename, contents)
        self.packageobj.add_installed_file(installPath = str(dir) + "/" + str(filename), 
                sourceFile = fakefile, 
                mode=None, 
                createParentDirs=True, 
                subpackageSuffix=None, 
                isConfig=False, 
                isDoc=False, 
                isGhost=False)
        #pass

    def addSource(self, filename, dir):
        pass
        f = open(filename, 'r')
        data = f.read()
        f.close()
        self.Create(filename, data, dir)

    def addArchive(self, filename, dir=None):

        if filename.startswith('http://') or filename.startswith('https://'):
            filename = fetchsources.fetchHttpFile(filename, self.builddir)
        filename = os.path.join(self.builddir, filename)
        print "> %s" % filename

        # copy file to ~/rpmbuild/SOURCES
        dstdir = os.path.join(os.environ['HOME'], 'rpmbuild', 'SOURCES')
        dstfile = os.path.join(dstdir, os.path.basename(filename))
        assert os.path.isdir(dstdir), "please create %s" % dstdir
        shutil.copyfile(filename, dstfile) 
        filename = os.path.basename(dstfile)
        #import epdb; epdb.st()

        # add to spec
        fakefile = rpmfluff.ExternalSourceFile(filename, filename)
        self.packageobj.add_source(fakefile)
        self.packageobj.section_build += "tar xvf %s\n" % filename

    def Configure(self, options=None):

            self.packageobj.section_prep += "%setup -q"

            if options == None:
                self.packageobj.section_build += "%configure \n"
            else:
                self.packageobj.section_build += "./configure %s \n"%(options)

    def Make(self, options=None):
		if options == None:
			self.packageobj.section_build += "make \n"
			print "> make"
		else:
			self.packageobj.section_build += "make %s \n"%(options)
			print "> make %s" % options

    def MakeInstall(self, options=None):
		if options == None:
			self.packageobj.section_install+= "make install DESTDIR=%{buildroot} \n"
			print "> make install DESTDIR=%{buildroot}"
		else:
			self.packageobj.section_install += "make install %s \n"%(options)
			print "> make install %s" % options

		#pdb.set_trace()
		sub = self.packageobj.get_subpackage(None)
		sub.section_files += '/*\n'
		'''
		sub.section_files += '%{_sysconfdir}/*\n'
		sub.section_files += '%{_prefix}/*\n'
		sub.section_files += '%{_exec_prefix}/*\n'
		sub.section_files += '%{_bindir}/*\n'
		sub.section_files += '%{_libdir}/*\n'
		sub.section_files += '%{_libexecdir}/*\n'
		sub.section_files += '%{_sbindir}/*\n'
		'''

    def Run(self, command):
        print "> %s" % command
        self.packageobj.section_build += "%s\n" % command
