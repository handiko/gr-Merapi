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

from gnuradio import gr
from gnuradio import blocks
from gnuradio.filter import firdes

class carrier_detect(gr.hier_block2):
    """
    docstring for block carrier_detect
    """
    def __init__(self, filter_len,gain,hi,low):
        gr.hier_block2.__init__(self,
            "carrier_detect",
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
            gr.io_signature(1, 1, gr.sizeof_short*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.filter_len = filter_len
        self.gain = gain
        self.hi = hi
        self.low = low

        ##################################################
        # Blocks
        ##################################################
        self.blocks_threshold_ff_0 = blocks.threshold_ff(low, hi, 0)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((gain, ))
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(filter_len, 1.0/filter_len, 4000)
        self.blocks_float_to_short_0 = blocks.float_to_short(1, 1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.blocks_float_to_short_0, 0), (self, 0))    
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_threshold_ff_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_moving_average_xx_0, 0))    
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_float_to_short_0, 0))    
        self.connect((self, 0), (self.blocks_complex_to_mag_squared_0, 0))    

    def get_filter_len(self):
        return self.filter_len

    def set_filter_len(self, filter_len):
        self.filter_len = filter_len
        self.blocks_moving_average_xx_0.set_length_and_scale(self.filter_len, 1.0/self.filter_len)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.blocks_multiply_const_vxx_1.set_k((self.gain, ))

    def get_hi(self):
        return self.hi

    def set_hi(self, hi):
        self.hi = hi
        self.blocks_threshold_ff_0.set_hi(self.hi)

    def get_low(self):
        return self.low

    def set_low(self, low):
        self.low = low
        self.blocks_threshold_ff_0.set_lo(self.low)
