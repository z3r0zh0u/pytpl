#!/usr/bin/env python
"""
Creaet Python template file

Usage:
    pytpl.py FileName
"""

import os
import sys

template = '''#!/usr/bin/env python
"""
Add your comments here.
"""

import os
import sys
import argparse

if __name__ == '__main__':
    """main function"""

    parser = argparse.ArgumentParser(description='add description here')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', '--dir', action='store_true', help='directory')
    group.add_argument('-f', '--file', action='store_true', help='file')
    parser.add_argument('target', action='store')

    args = parser.parse_args()

    if args.dir:
        if True == os.path.isdir(args.target):
            print args.target
        else:
            print '[!] Invalid Directory: ' + args.target

    if args.file:
        if True == os.path.isfile(args.target):
            print args.target
        else:
            print '[!] Invalid File: '+ args.target 
'''

if __name__ == '__main__':
    """Main function"""

    if len(sys.argv) == 2:
        filename = sys.argv[1]
        if '.py' != os.path.splitext(filename)[-1]:
                filename += '.py'
        if False == os.path.exists(filename):
            open(filename, 'wb').write(template)
            print 'Template file ' + filename + ' created successfully.'
        else:
            print filename + ' already exists.'
    else:
        print 'Usage: ' + sys.argv[0] + ' FileName'
        