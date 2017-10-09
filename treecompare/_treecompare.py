#!/usr/bin/env python3

''' treecompare.py - compare two directory trees 

Copyright (c) 2017 Marnix Kaart

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import os as _os

# blocksize when reading files
BLOCKSIZE = 8388608


def _walkdir(dirname):
    ''' yields relative paths (under dirname) for each file under given dir '''

    dirname = _os.path.abspath(_os.path.expanduser(dirname))

    if not _os.path.exists(dirname):
        raise FileNotFoundError('directory does not exist')
    if not _os.path.isdir(dirname):
        raise NotADirectoryError('this is not a directory')

    w = _os.walk(dirname)

    for (top, dirs, files) in w:
        # strip the original dirname from result
        if not top.startswith(dirname):
            raise RuntimeError('programming mistake!')
        top = top[len(dirname)+1:]
        for f in files:
            yield _os.path.join(top, f)


def namecomp(dir1, dir2, fullpath=True):
    ''' yield tuples of (subpath1, subpath2) for each file that occurs in both
    directories. If subpath only occurs in a given dir, the other item is None
    '''

    dir1 = _os.path.abspath(_os.path.expanduser(dir1))
    dir2 = _os.path.abspath(_os.path.expanduser(dir2))

    if dir1 == dir2:
        raise ValueError('both dirs are actually the same dir')

    # build a set of all names in the first directory
    nameset1={f for f in _walkdir(dir1)}

    for f in _walkdir(dir2):
        if f in nameset1:
            nameset1.remove(f)
            if fullpath is True:
                yield(_os.path.join(dir1, f), _os.path.join(dir2, f))
            else:
                yield(f, f)
        else:
            if fullpath is True:
                yield (None, _os.path.join(dir2, f))
            else:
                yield (None, f)

    for f in nameset1:
        if fullpath is True:
            yield (_os.path.join(dir1, f), None)
        else:
            yield (f, None)


def duplicate(file1, file2):
    ''' returns True if two files have equal contents '''

    file1 = _os.path.abspath(_os.path.expanduser(file1))
    file2 = _os.path.abspath(_os.path.expanduser(file2))

    f1size = _os.stat(file1).st_size
    f2size = _os.stat(file2).st_size

    if file1 == file2:
        raise ValueError('file1 and file2 cannot be the same file')

    # if size differs, so does contents
    if f1size != f2size:
        return False

    # empty files are not considered duplicates
    if f1size == 0:
        return False

    with open(file1, 'rb') as f1:
        with open(file2, 'rb') as f2:
            # read first block of both files
            f1blk = f1.read(BLOCKSIZE)
            f2blk = f2.read(BLOCKSIZE)
            while len(f1blk) != 0:
                if f1blk != f2blk:
                    # if blocks differ, files differ
                    return False
                # keep reading new blocks until eof
                f1blk = f1.read(BLOCKSIZE)
                f2blk = f2.read(BLOCKSIZE)

    # all blocks are equal: duplicate
    return True


def treedups(dir1, dir2):
    ''' yield path of files in dir1 that have duplicate in dir2 at same sub-path '''

    for n1, n2 in namecomp(dir1, dir2, fullpath=True):
        if n1 is None or n2 is None:
            # file has no counterpart in the other dir
            continue
        if duplicate(n1, n2):
            yield n1


def treepurge(dir1, dir2):
    ''' remove files from dir1 that have duplicate at same location in dir2 '''

    dir1 = _os.path.abspath(_os.path.expanduser(dir1))
    dir2 = _os.path.abspath(_os.path.expanduser(dir2))

    for path in treedups(dir1, dir2):
        # prevent foobar by checking if path is realy under dir1
        if not path.startswith(dir1):
            raise RuntimeError('programming error!')
        _os.unlink(path)

