#!/usr/bin/python
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2014, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of GPLv3 or later.

from __future__ import print_function

import os, sys
from random import randint
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
        path = "../server/info_pipe"
        if os.path.exists(path):
            os.unlink(path)
            #os.remove(path)
            print("Removed old pipe")

        print("Begin reading data: ")
        while(True):
            data = self.requester.read_by_uuid(
            #"0x2902")
                "0000aaaa-0000-1000-8000-00805f9b34fb")
            #"0000181c-0000-1000-8000-00805f9b34fbC")
            #"00002a00-0000-1000-8000-00805f9b34fb")
            #print(data)
            data = [ord(datum) for datum in data[0]]
            try:
                os.mkfifo(path)
            except:
                #print("pipe already exists")
                pass
            fifo = open(path, 'w')

            #copy & add randomness to data to show how aggregation
            data1 = ",".join([str(randint(i-3, i+3)) for i in data[:]])
            data2 = ",".join([str(randint(i-3, i+3)) for i in data[:]])
            data3 = ",".join([str(randint(i-3, i+3)) for i in data[:]])
            fifo.write(data1+"\n"+data2+"\n"+data3)
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
