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

class frame_detect(gr.sync_block):
    """
    docstring for block frame_detect
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="frame_detect",
            in_sig=[numpy.uint8],
            out_sig=None)
            
        self.message_port_register_out(pmt.intern('frame out'))
        
        self.bits_buff=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.preamble=[1,1,1,1,1,1,1,1,1,1,0,0,0,1,0,0,1,0,0,1]
        self.count_bits=0
        self.count_char=0
        self.preamble_found=0
        self.char=0
        self.bytes=[]
        self.data_is_valid=0

    def work(self, input_items, output_items):
        in0 = input_items[0]
        
        for i in in0:
            for j in range(0,19):
                self.bits_buff[j]=self.bits_buff[j+1]
            self.bits_buff[19]=i
            self.count_bits+=1
            
            if self.bits_buff==self.preamble:
                #print "Preamble Found !"
                self.preamble_found=1
                self.count_bits=10
                
            if self.preamble_found == 1 and self.count_bits==10:
                self.char+=self.bits_buff[11]
                self.char+=self.bits_buff[12]*2
                self.char+=self.bits_buff[13]*4
                self.char+=self.bits_buff[14]*8
                self.char+=self.bits_buff[15]*16
                self.char+=self.bits_buff[16]*32
                self.char+=self.bits_buff[17]*64
                self.char+=self.bits_buff[18]*128
                
                if self.char==35 or self.char==36 or (self.char>=48 and self.char<=57) or (self.char>=65 and self.char<=90):
                    self.data_is_valid=1
                
                self.count_bits=0
                self.count_char+=1
                #print chr(self.char)
                self.bytes.append(self.char)
                self.char=0
                if self.count_char==29:
                    self.preamble_found=0
                    self.count_bits=0
                    self.count_char=0
                    self.bytes.append(10)
                    if self.data_is_valid==1:
                        self.message_port_pub(pmt.intern('frame out'), pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(self.bytes), self.bytes)))
                    else:
                        print "Invalid Data Received \n"
                    self.bytes=[]
                    self.data_is_valid=0
            
            #print self.char
        
        return len(input_items[0])

