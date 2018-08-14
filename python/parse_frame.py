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
import pmt
import math
import array
import time
import datetime
import csv, sys, os, io

class parse_frame(gr.sync_block):
    """
    docstring for block parse_frame
    """
    def __init__(self, filename):
        gr.sync_block.__init__(self,
            name="parse_frame",
            in_sig=None,
            out_sig=None)
        self.message_port_register_in(pmt.intern('frame_in'))
        self.message_port_register_out(pmt.intern('info_out'))
        self.message_port_register_out(pmt.intern('parse_out'))
        self.set_msg_handler(pmt.intern('frame_in'), self.handle_msg)
        self.filename=filename

    def handle_msg(self, msg_pmt):
        pkt = pmt.pmt_to_python.pmt_to_python(msg_pmt)
        
        #print pkt
        
        buff_var=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0]]
        
        var=[0,0,0,0,0,0]
        
        
        buff_var[0][:]=pkt[1][6:10]
        buff_var[1][:]=pkt[1][10:14]
        buff_var[2][:]=pkt[1][14:18]
        buff_var[3][:]=pkt[1][18:22]
        buff_var[4][:]=pkt[1][22:26]
        buff_var[5][:]=pkt[1][26:28]
        
        for i in range(0,5):
            for j in range(0,4):
                var[i]+=((buff_var[i][3-j])-48)*(pow(16,j))
            #print var[i]
                
        for k in range(0,2):
            var[5]+=((buff_var[5][1-k])-48)*(pow(16,k))
        #print var[5]
        
        hor = var[0]*0.05			#hor=round(var[0]/2.0)/10.0
        vert = var[1]*0.05			#vert=round(var[1]/2.0)/10.0
        temp = var[2]*0.1			#temp=round((var[2]/10.0)*10)/10.0
        gas = var[3]*0.05			#gas=round(var[3]/2.0)/10.0
        hum = -0.05*var[4] + 440	#hum=round(1000*(34816 - var[4])/28016.0)/5.0
        rain = var[5]*1.5			#rain=round(var[5]*15.0)/10.0
        
        """
        print hor
        print vert
        print temp
        print gas
        print hum
        print rain
        """
        localtime = time.asctime( time.localtime(time.time()))
        time_text="["+localtime+"]"
        info = time_text+"   HOR = "+str(hor)+" v/v "+"VERT = "+str(vert)+" v/v "+"TEMP = "+str(temp)+" deg.C "+"Gas Cons. = "+str(gas)+" % "+"HUM = "+str(hum)+" % "+"RAIN = "+str(rain)+" mm \n"
        #print info

        csvfile=open(self.filename,'a')
        csv_text = [[time_text,"HOR = ",str(hor),"VERT = ",str(vert),"TEMP = ",str(temp),"GAS = ",str(gas),"HUM = ",str(hum),"RAIN = ",str(rain)]]
        with csvfile:
            writer = csv.writer(csvfile)
            for row in csv_text:
                writer.writerow(row) 

        info = bytearray(info)
        self.message_port_pub(pmt.intern('info_out'), pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(info), info)))

        info = bytearray(localtime)
        self.message_port_pub(pmt.intern('parse_out'), pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(info), info)))

        info = bytearray("HOR = "+str(hor)+" v/v")
        self.message_port_pub(pmt.intern('parse_out'), pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(info), info)))

        info = bytearray("VERT = "+str(vert)+" v/v")
        self.message_port_pub(pmt.intern('parse_out'), pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(info), info)))

        info = bytearray("TEMP = "+str(temp)+" deg.C")
        self.message_port_pub(pmt.intern('parse_out'), pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(info), info)))

        info = bytearray("Gas Cons. = "+str(gas)+" %")
        self.message_port_pub(pmt.intern('parse_out'), pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(info), info)))

        info = bytearray("HUM = "+str(hum)+" %")
        self.message_port_pub(pmt.intern('parse_out'), pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(info), info)))

        info = bytearray("RAIN = "+str(rain)+" mm")
        self.message_port_pub(pmt.intern('parse_out'), pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(info), info)))


    def work(self, input_items, output_items):
        in0 = input_items[0]
        # <+signal processing here+>
        return len(input_items[0])
