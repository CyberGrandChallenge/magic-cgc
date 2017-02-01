#!/usr/bin/python

import os
import sys
import unittest
import time
import tempfile
import subprocess
import shutil

class test_magic(unittest.TestCase):
    def build_cb(self):
        c = os.getcwd()
        for cb in self.cbs:
            subprocess.check_output(['cp', '-r', '/usr/share/cgc-sample-challenges/examples/%s' % cb, self.tmp_dir])
            os.chdir("%s/%s" % (self.tmp_dir, cb))
            subprocess.check_output(['make', 'build', 'generate-polls'])
            subprocess.check_output(['make', 'install', 'CB_INSTALL_DIR=%s/%s' % (self.cbdir, cb)])
        os.chdir(c)

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.cbdir = '%s/challenges' % self.tmp_dir

        self.cbs = ['LUNGE_00005', 'CADET_00003']

        self.files = {'/bin/cat': 'ELF','/etc/passwd': 'ASCII'}

        for i in [self.cbdir]:
            if not os.path.isdir(i):
                os.mkdir(i)

        self.build_cb()


    def tearDown(self):
        shutil.rmtree(self.tmp_dir) 

    def test_cb(self):
        for cb in self.cbs:
            thefile = '%s/%s/bin/%s' % (self.cbdir, cb, cb)

            #just find and check first CB if this is a multi-CB CS
            if not os.path.isfile(thefile):
               thefile = thefile + "_1"

            self.assertTrue(os.path.isfile(thefile))

            result = subprocess.check_output(['file',thefile])
            self.assertTrue(result.endswith( "CGC 32-bit LSB executable, (CGC/Linux)\n"))
            self.assertFalse(": data" in result)

    def test_non_cb(self):
        for bin,text in self.files.items():
            result = subprocess.check_output(['file',bin])
            self.assertTrue(text in result)
            self.assertFalse(": data" in result)
            self.assertFalse("CGC 32-bit LSB executable" in result)


if __name__ == '__main__':
    unittest.main()
