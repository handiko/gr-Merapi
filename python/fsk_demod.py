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

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
import math

class fsk_demod(gr.hier_block2):
    """
    docstring for block fsk_demod
    """
    def __init__(self, baud,fsk_hi_tone,fsk_lo_tone,gmu,in_sps):
        gr.hier_block2.__init__(self,
            "fsk_demod",
            gr.io_signature(1, 1, gr.sizeof_float*1),
            gr.io_signaturev(4, 4, [gr.sizeof_float*1, gr.sizeof_float*1, gr.sizeof_float*1, gr.sizeof_float*1]),
        )

        ##################################################
        # Parameters
        ##################################################
        self.baud = baud
        self.fsk_hi_tone = fsk_hi_tone
        self.fsk_lo_tone = fsk_lo_tone
        self.gmu = gmu
        self.in_sps = in_sps

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = baud*in_sps
        self.out_sps = out_sps = 2

        ##################################################
        # Blocks
        ##################################################
        self.root_raised_cosine_filter_1 = filter.fir_filter_ccf(1, firdes.root_raised_cosine(
        	1, in_sps*1.0, 1.0, 0.7, 4*in_sps))
        self.root_raised_cosine_filter_0 = filter.fir_filter_ccf(1, firdes.root_raised_cosine(
        	1, in_sps*1.0, 1.0, 0.7, 4*in_sps))
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=out_sps,
                decimation=in_sps,
                taps=None,
                fractional_bw=None,
        )
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(out_sps*(1+0.0), 0.25*pow(gmu,2.0), 0.5, gmu, 0.005)
        self.blocks_sub_xx_2 = blocks.sub_ff(1)
        self.blocks_rotator_cc_1 = blocks.rotator_cc((-1.0*fsk_hi_tone/samp_rate)*2*math.pi)
        self.blocks_rotator_cc_0 = blocks.rotator_cc((-1.0*fsk_lo_tone/samp_rate)*2*math.pi)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_mag_1 = blocks.complex_to_mag(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.analog_agc2_xx_1 = analog.agc2_ff(0.5, 0.00001, 1.0, 1.0)
        self.analog_agc2_xx_1.set_max_gain(65536)
        self.analog_agc2_xx_0 = analog.agc2_ff(0.5, 0.00001, 1.0, 1.0)
        self.analog_agc2_xx_0.set_max_gain(65536)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc2_xx_0, 0), (self.blocks_sub_xx_2, 0))    
        self.connect((self.analog_agc2_xx_0, 0), (self, 2))    
        self.connect((self.analog_agc2_xx_1, 0), (self.blocks_sub_xx_2, 1))    
        self.connect((self.analog_agc2_xx_1, 0), (self, 3))    
        self.connect((self.blocks_complex_to_mag_0, 0), (self.analog_agc2_xx_0, 0))    
        self.connect((self.blocks_complex_to_mag_1, 0), (self.analog_agc2_xx_1, 0))    
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_rotator_cc_0, 0))    
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_rotator_cc_1, 0))    
        self.connect((self.blocks_rotator_cc_0, 0), (self.root_raised_cosine_filter_0, 0))    
        self.connect((self.blocks_rotator_cc_1, 0), (self.root_raised_cosine_filter_1, 0))    
        self.connect((self.blocks_sub_xx_2, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self, 0))    
        self.connect((self, 0), (self.blocks_float_to_complex_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self, 1))    
        self.connect((self.root_raised_cosine_filter_0, 0), (self.blocks_complex_to_mag_0, 0))    
        self.connect((self.root_raised_cosine_filter_1, 0), (self.blocks_complex_to_mag_1, 0))    

    def get_baud(self):
        return self.baud

    def set_baud(self, baud):
        self.baud = baud
        self.set_samp_rate(self.baud*self.in_sps)

    def get_fsk_hi_tone(self):
        return self.fsk_hi_tone

    def set_fsk_hi_tone(self, fsk_hi_tone):
        self.fsk_hi_tone = fsk_hi_tone
        self.blocks_rotator_cc_1.set_phase_inc((-1.0*self.fsk_hi_tone/self.samp_rate)*2*math.pi)

    def get_fsk_lo_tone(self):
        return self.fsk_lo_tone

    def set_fsk_lo_tone(self, fsk_lo_tone):
        self.fsk_lo_tone = fsk_lo_tone
        self.blocks_rotator_cc_0.set_phase_inc((-1.0*self.fsk_lo_tone/self.samp_rate)*2*math.pi)

    def get_gmu(self):
        return self.gmu

    def set_gmu(self, gmu):
        self.gmu = gmu
        self.digital_clock_recovery_mm_xx_0.set_gain_omega(0.25*pow(self.gmu,2.0))
        self.digital_clock_recovery_mm_xx_0.set_gain_mu(self.gmu)

    def get_in_sps(self):
        return self.in_sps

    def set_in_sps(self, in_sps):
        self.in_sps = in_sps
        self.set_samp_rate(self.baud*self.in_sps)
        self.root_raised_cosine_filter_1.set_taps(firdes.root_raised_cosine(1, self.in_sps*1.0, 1.0, 0.7, 4*self.in_sps))
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.in_sps*1.0, 1.0, 0.7, 4*self.in_sps))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_rotator_cc_1.set_phase_inc((-1.0*self.fsk_hi_tone/self.samp_rate)*2*math.pi)
        self.blocks_rotator_cc_0.set_phase_inc((-1.0*self.fsk_lo_tone/self.samp_rate)*2*math.pi)

    def get_out_sps(self):
        return self.out_sps

    def set_out_sps(self, out_sps):
        self.out_sps = out_sps
        self.digital_clock_recovery_mm_xx_0.set_omega(self.out_sps*(1+0.0))
