mfp
===

multi-format packager


input: python/conary like recipe

output:  .spec + srcrpm + rpm  / deb / ?

Usage:
---

# output just an rpm spec file
mfp testpackage.recipe --verbose --speconly

# create spec, sourcerpm and rpms
mfp testpackage.recipe --verbose


Example Recipe:
---

```python
class TestPackage(RpmPackage):

    name = "mypackage"
    version = "1"
    release = "1"
    description = "test package"
    license = "GPL"
    vendor = "jtanner"
    packager = "jtanner"
    url = "localhost"


    def setup(r):
        r.Create('newfile', contents="hello world\n", dir='/etc')
        r.addSource('testfile.txt', dir='/etc/')
        r.addArchive('tarball.tar.gz', '/opt/data')
```

Example Joe Recipe:
---

```python
class TestPackage(RpmPackage):

    name = "joe"
    version = "3.7"
    release = "1"
    description = "joe's editor"
    license = "GPL"
    vendor = "joe"
    packager = "tanner.jc@gmail.com"
    url = "http://joe-editor.sourceforge.net/"

    def setup(r):
        r.addArchive('joe-3.7.tar.gz')
        r.Configure()
        r.Make()
        r.MakeInstall()
```

Example Conary Package Manager:
---
```python
class TestPackage(RpmPackage):

    name = "conary"
    version = "2.4.13"
    release = "1"
    description = "conary package manager"
    license = "Apache 2.0"
    vendor = "rpath"
    summary = "conary package manager"
    group = "System Environment/Base"
    packager = "tanner.jc@gmail.com"
    url = "https://bitbucket.org/rpathsync/conary"

    buildrequires = ['python-devel', 'openssl-devel', 'elfutils-libelf-devel', 'sqlite-devel']

    def setup(r):
        r.addArchive("https://bitbucket.org/rpathsync/conary/get/conary-2.4.13.tar.gz")

        # cd rpathsync-conary-9e82ab6709a2
        r.Run("cd rpathsync-conary-*")

        # make minimal libelf=-lelf
        r.Make(options="minimal libelf=-lelf")

        # make install NO_KID=1
        r.MakeInstall(options="NO_KID=1")
```
