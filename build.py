#!/usr/bin/env python2.7

import subprocess

import os
import zipfile
import virtualenv
import pip

workingPath = os.path.dirname(os.path.abspath(__file__))

def buildZip(sources, dstRelative):
    dstSub1 = os.path.join(workingPath,'dist')
    dst = os.path.join(workingPath,'dist',dstRelative)
    if not os.path.isdir(dstSub1):
        os.mkdir(dstSub1)
    zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
    for relativeSrc in sources:
        src=os.path.join(workingPath,relativeSrc)
        
        abs_src = os.path.abspath(src)
        for dirname, subdirs, files in os.walk(src):
            for filename in files:
                absname = os.path.abspath(os.path.join(dirname, filename))
                arcname = absname[len(abs_src) + 1:]
                print 'zipping %s as %s' % (os.path.join(dirname, filename),
                                            arcname)
                zf.write(absname, arcname)
    zf.close()
    
venvPath=os.path.join(workingPath,'venv')
virtualenv.create_environment(venvPath)
execfile(os.path.join(venvPath, "bin", "activate_this.py"))

pip.main(["install","--ignore-installed","--prefix", venvPath, "requests"])
pip.main(["install","--ignore-installed", "--prefix", venvPath, "dashbot"])
       
buildZip(
    [
        "src",
        "venv/lib/python2.7/site-packages",
        "venv/lib/python2.7/dist-packages"
     ],
     "build"
)
