# Treecompare

This is a simple tool to compare two directory trees. The comparison is based
on the subpath that each file holds within the two trees. This is best
illustrated with the following example of two different directories (under
/home/testuser/temp):

```
dir1/one                         dir2/one
dir1/two                         dir2/four
dir1/subdir1/three               dir2/subdir1/three
dir1/subdir2/four                dir2/subdir2/five
                                 dir2/subdir3/six
```

In this example, the files named 'one' and 'six' have the exact same contents,
all other files are different.

Treecompare can be used to list all unique file paths in one of the two
directories:

```
$ treecompare --unique dir1 dir2
/home/testuser/temp/dir1/two
/home/testuser/temp/dir1/subdir2/four
```

Or the other way around:

```
$ treecompare --unique dir2 dir1
/home/testuser/temp/dir2/four
/home/testuser/temp/dir2/subdir3/six
/home/testuser/temp/dir2/subdir2/five
```

Another use case is to list all duplicates that exist at the same location
within both directory trees:


```
$ treecompare --duplicate dir1 dir2
/home/testuser/temp/dir1/one
```

We always compare the directory that is specified first against the directory
that is specified second, so if we want to list all duplicates in the second
dir, just reverse the arguments:

```
$ treecompare --duplicate dir1 dir2
/home/testuser/temp/dir1/one
```

Note that the file dir2/subdir3/six has the same contents as dir1/one and
dir2/one, but since it is at a different subpath, it is not considered
duplicate by treecompare.

Hopefully, from these examples it should be clear that this is intended for a
very specific use-case. I use it to compare multiple backups of the same device
in order to determine what files have been changed or removed between backups.
If you are looking for a tool to find *all* duplicates in one or more
directories, you should use a tool such as fslint or fdupes.

## warning

I take no responsibilty if you decide to use this software and if anything goes
wrong (see LICENCE). But if you do decide to try it and find any problems or
issues, it is appreciated if you report them.

Also note that this has been written and tested on a Linux machine, it may or
may not work on Windows. It should work, but I have not tested it.

## Usage

Treecompare can be used as a standalone tool or as a python module.

### commandline tool usage

See:

```
$ treecompare -h
usage: treecompare [-h] [--unique | --duplicate | --purge] DIR1 DIR2

treecompare - a simple tool to compare two directories

positional arguments:
  DIR1         first directory
  DIR2         second directory

optional arguments:
  -h, --help   show this help message and exit
  --unique     list files that only exist in DIR1
  --duplicate  list files in DIR1 that have a duplicate in DIR2 at same path
  --purge      remove files from DIR1 that have duplicate in DIR2 at same path

Example usage:
 treecompare --unique dir1 dir2
 treecompare --purge dir1 dir2
```

### module usage

You can also use treecompare in your other projects. If you want to compare two
directory trees by name, use the following:

```
>>> import treecompare
>>> w = treecompare.namecomp('~/temp/dir1','~/temp/dir2/', fullpath=False)
>>> for r in w: print(r)
...
(None, 'four')
('one', 'one')
(None, 'subdir3/six')
(None, 'subdir2/five')
('subdir1/three', 'subdir1/three')
('two', None)
('subdir2/four', None)
```

Here we see that 'one' and 'subdir1/three' exist in both directories, all other
files are unique to either dir1 or dir2 (i.e. one of the entries is None).

In above example, only the filename is checked. If you want to compare by
contents as well we can use the following:

```
>>> w = treecompare.treedups('~/temp/dir1/','~/temp/dir2')
>>> next(w)
'/home/testuser/temp/dir1/one'
>>> next(w)
Traceback (most recent call last):
  File "<input>", line 1, in <module>
StopIteration
```

We see here that the files 'dir1/one' and 'dir2/one' are both in the same
subpath *and* have the same contents. If you want to compare dir2 against dir1,
you can just reverse the arguments to this function.

The files that exist at the same location are compared on a block-by-block
basis. As soon as a different block is encountered, comparison is aborted and
the files will be marked as being different. This makes comparison rather fast
when the files are different and only a full compare is done when files are
actually equal. If you are only interested in this comparison of two files, you
can call the 'duplicate' function:

```
>>> treecompare.duplicate('~/temp/dir1/one','~/temp/dir2/one')
True
>>> treecompare.duplicate('~/temp/dir1/one','~/temp/dir2/subdir3/six')
True
>>> treecompare.duplicate('~/temp/dir1/subdir1/three','~/temp/dir2/subdir1/three')
False
```

Note that this function does not consider file-path so you can just compare any
two files this way. Internally, an md5 hash is used to determine if the files
are equal.

## installation

I did not yet submit this to PyPI, so currently the only way to install is to
clone the repository and install manually or via the provided Makefile:

```
$ sudo make install
```

## licence

MIT License

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

