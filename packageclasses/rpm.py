#!/usr/bin/python

import pdb
import rpmfluff
import magic
import tarfile
import os

#packagename = "test"

class RpmPackage(object): 
    def __init__(self):
        #self.name = "test"
        #foo = rpmfluff.SimpleRpmBuild(packagename, "0.1", "1")
        self.packageobj = rpmfluff.SimpleRpmBuild(self.name, 
                                                self.version, 
                                                self.release)

    def setup(self,args):
        print "class setup"

    def build(self, args):
        print "building ..."

        #pdb.set_trace()

        if args.verbose:
            print "    verbose mode on"

        if args.speconly:
            print "    speconly mode on"

        print ""
        print "    package name:" , str(self.name)
        print "    package version:" , str(self.version)
        print "    package release:" , str(self.release)

        self.setup()
        #pdb.set_trace()
        if args.speconly:
            self.packageobj.gather_spec_file('')
        else:
            self.packageobj.make()

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
        #pass
        #self.packageobj.add_compressed_file(filename, dir)
        '''
        self.packageobj.add_generated_tarball(filename,
                                                '',
                                                'contents',
                                                installPath=dir)
        '''
        filetype = ""
        ms = magic.open(magic.MAGIC_NONE)
        ms.load()
        f = file(filename, 'r')
        buffer = f.read(4096)
        f.close()
        type = ms.buffer(buffer)
        ms.close
        print "     %s" % type
        #pdb.set_trace()

        if "gzip compressed data, from Unix" in type:
            print "     this is a gzip file"
            filetype = "tar"
        else:
            print "     cant not handle %s types yet" % type
            sys.exit("error") 

        #pdb.set_trace()

        # if no directory is given, assume this is a source tarball
        #   else, extract all files and add individually

        if dir == None:
            fakefile = rpmfluff.ExternalSourceFile(filename, filename)
            self.packageobj.add_source(fakefile)
        else:
            if filetype == "tar":
                extractdir = "mfp.tmp"
                t = tarfile.open(filename)    
                #print t.list(verbose=False)
                tfiles = t.list(verbose=False)
                #print tfiles
                t.extractall(extractdir)
                #pdb.set_trace()

                for tf in os.listdir(extractdir):
                    f = open(extractdir + "/" + tf, 'r')
                    data = f.read()
                    f.close()
                    self.Create(tf, data, dir)
