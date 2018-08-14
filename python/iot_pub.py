#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2018 PT. Datto Asia Teknologi
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr
import httplib
import urllib
import time
import pmt

class iot_pub(gr.sync_block):
    """
    docstring for block iot_pub
    """
    def __init__(self, address,api_key,content_type,accept_type,field1,field2,field3,field4,field5,field6,field7,field8):
        gr.sync_block.__init__(self,
            name="iot_pub",
            in_sig=None,
            out_sig=None)
        self.message_port_register_in(pmt.intern('parse_in'))
        self.set_msg_handler(pmt.intern('parse_in'), self.handle_msg)
        self.address=address
        self.api_key=api_key
        self.content_type=content_type
        self.accept_type=accept_type
        self.field1=field1
        self.field2=field2
        self.field3=field3
        self.field4=field4
        self.field5=field5
        self.field6=field6
        self.field7=field7
        self.field8=field8

        self.sanity_check=0

    def handle_msg(self, msg_pmt):
        pkt = pmt.pmt_to_python.pmt_to_python(msg_pmt)

        pkt_d = "".join([chr(item) for item in pkt[1][:3]])

        headers = {"Content-typeZZe":self.content_type,"Accept":self.accept_type}

        try:
            conn = httplib.HTTPConnection(self.address)

            if pkt_d=="HOR":
                pkt_hor = "".join([chr(item) for item in pkt[1][:]])

                params = urllib.urlencode({'field1':float(pkt_hor[6:len(pkt_hor)-4]), 'key':self.api_key})
                conn.request("POST","/update",params,headers)
                response = conn.getresponse()
                print "upload HOR status", response.status
        
            elif pkt_d=="VER":
                pkt_ver = "".join([chr(item) for item in pkt[1][:]])

                params = urllib.urlencode({'field2':float(pkt_ver[7:len(pkt_ver)-4]), 'key':self.api_key})
                conn.request("POST","/update",params,headers)
                response = conn.getresponse()
                print "upload VER status", response.status
        
            elif pkt_d=="TEM":
                pkt_tem = "".join([chr(item) for item in pkt[1][:]])
                
                self.sanity_check=float(pkt_tem[7:len(pkt_tem)-6])
                if self.sanity_check>=0 and self.sanity_check<=100:
                    params = urllib.urlencode({'field3':float(pkt_tem[7:len(pkt_tem)-6]), 'key':self.api_key}) 
                    conn.request("POST","/update",params,headers)
                    response = conn.getresponse()
                    print "upload TEMP status", response.status
                else:
                    print "TEMP data is error, not uploaded"
        
            elif pkt_d=="Gas":
                pkt_gas = "".join([chr(item) for item in pkt[1][:]])

                self.sanity_check=float(pkt_gas[12:len(pkt_gas)-4])
                if self.sanity_check>=0 and self.sanity_check<=100:
                    params = urllib.urlencode({'field4':float(pkt_gas[12:len(pkt_gas)-4]), 'key':self.api_key})
                    conn.request("POST","/update",params,headers)
                    response = conn.getresponse()
                    print "upload GAS status", response.status
                else:
                    print "GAS data is error, not uploaded"
        
            elif pkt_d=="HUM":
                pkt_hum = "".join([chr(item) for item in pkt[1][:]])

                self.sanity_check=float(pkt_hum[6:len(pkt_hum)-2])
                if self.sanity_check>=0 and self.sanity_check<=100:
                    params = urllib.urlencode({'field5':float(pkt_hum[6:len(pkt_hum)-2]), 'key':self.api_key})
                    conn.request("POST","/update",params,headers)
                    response = conn.getresponse()
                    print "upload HUM status", response.status
                else:
                    print "HUM data is error, not uploaded"
        
            elif pkt_d=="RAI":
                pkt_rai = "".join([chr(item) for item in pkt[1][:]])

                params = urllib.urlencode({'field6':float(pkt_rai[7:len(pkt_rai)-3]), 'key':self.api_key})
                conn.request("POST","/update",params,headers)
                response = conn.getresponse()
                print "upload RAIN status", response.status
                
            conn.close()

        except:
            print "Connection Failed"

    def work(self, input_items, output_items):
        in0 = input_items[0]
        # <+signal processing here+>
        return len(input_items[0])
