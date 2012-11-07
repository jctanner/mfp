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
