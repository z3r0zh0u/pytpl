#!/usr/bin/env python
"""
Port Scan Through mxtoolbox.com
"""

import os
import re
import sys
import time
import json
import urllib2
import argparse


def mxtb_scan(address):
    """Port scan for a single IP address or host name"""

    print '[*] Scan: ' + address

    url = 'http://mxtoolbox.com/Public/Lookup.aspx/DoLookup2'

    headers = { 'Origin': 'http://mxtoolbox.com',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
                'Referer': 'http://mxtoolbox.com/SuperTool.aspx',
                'Content-Type': 'application/json; charset=UTF-8',
                'Accept-Encoding': 'deflate',
                'Accept-Language': 'en-US,en;q=0.8'}

    data = '{"inputText":"scan:' + address + '", "resultIndex":1}'

    try:
        request = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(request)
        content = response.read()
        data1 = json.loads(content)
        data2 = json.loads(data1[u'd'])
        html_data = data2['HTML_Value']
        m = re.search('<table.*?</table>', html_data, re.S)
        if m is not None:
            table_data = m.group(0)
            return table_data
    except Exception as e:
        print '[!] Network Error: ' + str(e)

    return None


def process_file(filename):
    """Port scan for a list of IP addresses or host names in a file"""

    if False == os.path.isfile(filename):
        print '[!] Invalid File: ' + filename
        return

    result_file = 'scan_result_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.html'
    for address in open(filename, 'rb'):
        address = address.strip()
        result = mxtb_scan(address)
        open(result_file, 'ab').write('<h4>' + address + '</h4>\r\n')
        if result is not None:
            open(result_file, 'ab').write(result)
        else:
            open(result_file, 'ab').write('Scan Fail\r\n')
        
        time.sleep(1)

    print '[*] Result Saved: ' + result_file


if __name__ == '__main__':
    """main function"""

    parser = argparse.ArgumentParser(description='Port Scan Through mxtoolbox.com')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', '--address', action='store_true', help='single IP address or host name')
    group.add_argument('-f', '--file', action='store_true', help='IP addresses or host names from a file')
    parser.add_argument('target', action='store')

    args = parser.parse_args()

    if args.address:
        mxtb_scan(args.target)

    if args.file:
        if True == os.path.isfile(args.target):
            process_file(args.target)
        else:
            print '[!] Invalid File: '+ args.target 
