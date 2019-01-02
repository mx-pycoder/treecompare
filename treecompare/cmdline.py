#!/usr/bin/env python3

''' application.py - commandline interface for treecompare

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

import argparse as _argparse
import os.path as _path

from . import _treecompare

def _parser():
    ''' argument parser '''
    parser = _argparse.ArgumentParser(
        prog='treecompare',
        formatter_class = _argparse.RawDescriptionHelpFormatter,
        description = 'treecompare - a simple tool to compare two directories',
        epilog = 'Example usage: \n' +\
                 ' treecompare --unique dir1 dir2\n' +\
                 ' treecompare --purge dir1 dir2\n'
        )

    parser.add_argument('dir1', metavar='DIR1', help='first directory')
    parser.add_argument('dir2', metavar='DIR2', help='second directory')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--unique', action='store_true', help='list files that only exist in DIR1')
    group.add_argument('--duplicate', action='store_true', 
            help='list files in DIR1 that have a duplicate in DIR2 at same path')
    group.add_argument('--purge', action='store_true',
            help='remove files from DIR1 that have duplicate in DIR2 at same path')
    return parser


def main():
    ''' entry point '''

    parser = _parser()
    args = parser.parse_args()

    dir1 = getattr(args, 'dir1')
    dir2 = getattr(args, 'dir2')

    if getattr(args, 'unique') is True:
        try:
            w = _treecompare.namecomp(dir1, dir2, fullpath=True)
            for (f1, f2) in w:
                if f1 is not None and f2 is None:
                    # path only exists in f1, print result
                    print(f1)
                elif f1 is not None and f2 is not None:
                    # path exists in both trees, compare contents
                    if not _treecompare.duplicate(f1, f2):
                        print(f1)

        except ValueError:
            print("DIR1 and DIR2 cannot be the same!\n")
        except FileNotFoundError:
            print("one of the specified dirs does not exist!\n")
        except NotADirectoryError:
            print("one of the specified dirs is not a directory!\n")
        return

    elif getattr(args, 'duplicate') is True:
        try:
            w = _treecompare.treedups(dir1, dir2)
            for f in w:
                print(f)
        except ValueError:
            print("DIR1 and DIR2 cannot be the same!\n")
        except FileNotFoundError:
            print("one of the specified dirs does not exist!\n")
        except NotADirectoryError:
            print("one of the specified dirs is not a directory!\n")
        return

    elif getattr(args, 'purge') is True:
        try:
            _treecompare.treepurge(dir1, dir2)
        except ValueError:
            print("DIR1 and DIR2 cannot be the same!\n")
        except FileNotFoundError:
            print("one of the specified dirs does not exist!\n")
        except NotADirectoryError:
            print("one of the specified dirs is not a directory!\n")
        return

    else:
        print('specify either --unique, --duplicate or --purge\n')
        parser.print_help()


if __name__ == "__main__":
    main()


