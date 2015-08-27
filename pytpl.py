#!/usr/bin/env python
"""
Creaet Python template file.close

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

if __name__ == '__main__':
    """Main function"""

    if len(sys.argv) == 2:
        filename = sys.argv[1]
        if True == os.path.isfile(filename):
            print filename
        else:
            print filename + ' is not a valid file.'
    else:
        print 'Usage: ' + sys.argv[0] + ' FileName'    

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
        