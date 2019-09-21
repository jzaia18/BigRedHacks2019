#!/usr/bin/python
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2014, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of GPLv3 or later.

from __future__ import print_function

import os, sys
from bluetooth.ble import GATTRequester


class Reader(object):
    def __init__(self, address):
        self.requester = GATTRequester(address, False)
        self.connect()
        self.request_data()

    def connect(self):
        print("Connecting...", end=' ')
        sys.stdout.flush()

        self.requester.connect(True)
        print("OK!")

    def request_data(self):
        #for each in self.requester.discover_characteristics():
        #    print(each)
        #    print(self.requester.read_by_handle(each['handle']))
        print("Begin reading data: ")
        while(True):
            data = self.requester.read_by_uuid(
            #"0x2902")
                "0000aaaa-0000-1000-8000-00805f9b34fb")
            #"0000181c-0000-1000-8000-00805f9b34fbC")
            #"00002a00-0000-1000-8000-00805f9b34fb")
            #print(data)
            data = ",".join([str(ord(datum)) for datum in data[0]])


            path = "../server/info_pipe"
            try:
                os.mkfifo(path)
            except:
                #print("pipe already exists")
                pass
            fifo = open(path, 'w')
            fifo.write(str(data) + "\n")
            fifo.close()
        '''
        try:
            print("Device name: " + data.decode("utf-8"))
        except AttributeError:
            print("Device name: " + data)
        '''

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} <addr>".format(sys.argv[0]))
        sys.exit(1)

    Reader(sys.argv[1])
    print("Done.")
