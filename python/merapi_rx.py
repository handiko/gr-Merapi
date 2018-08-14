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
from gnuradio.filter import pfb
import Merapi
import math

class merapi_rx(gr.hier_block2):
    """
    docstring for block merapi_rx
    """
    def __init__(self, baud,bpf_trans,filter_len,fsk_hi_tone,fsk_lo_tone,gain,gmu,hi,input_rate,low,mu):
        gr.hier_block2.__init__(self,
            "merapi_rx",
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
            gr.io_signaturev(3, 3, [gr.sizeof_gr_complex*1, gr.sizeof_float*1, gr.sizeof_short*1]),
        )
        self.message_port_register_hier_out("frame_out")
        self.message_port_register_hier_out("afsk")
        self.message_port_register_hier_out("hi_symb")
        self.message_port_register_hier_out("lo_symb")
        self.message_port_register_hier_out("softbits")

        ##################################################
        # Parameters
        ##################################################
        self.baud = baud
        self.bpf_trans = bpf_trans
        self.filter_len = filter_len
        self.fsk_hi_tone = fsk_hi_tone
        self.fsk_lo_tone = fsk_lo_tone
        self.gain = gain
        self.gmu = gmu
        self.hi = hi
        self.input_rate = input_rate
        self.low = low
        self.mu = mu

        ##################################################
        # Variables
        ##################################################
        self.ch_rate = ch_rate = 48e3
        self.sps = sps = int(ch_rate / baud)

        ##################################################
        # Blocks
        ##################################################
        self.root_raised_cosine_filter_1 = filter.fir_filter_ccf(1, firdes.root_raised_cosine(
        	1, sps*1.0, 1.0, 0.7, 4*sps))
        self.root_raised_cosine_filter_0 = filter.fir_filter_ccf(1, firdes.root_raised_cosine(
        	1, sps*1.0, 1.0, 0.7, 4*sps))
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=2,
                decimation=sps,
                taps=None,
                fractional_bw=None,
        )
        self.pfb_arb_resampler_xxx_0 = pfb.arb_resampler_ccf(
        	  ch_rate / input_rate,
                  taps=None,
        	  flt_size=32)
        self.pfb_arb_resampler_xxx_0.declare_sample_delay(0)
        	
        self.Merapi_frame_detect_0 = Merapi.frame_detect()
        self.fft_filter_xxx_0 = filter.fft_filter_fff(1, (firdes.band_pass(0.1,ch_rate,fsk_lo_tone-(bpf_trans/2),fsk_hi_tone+(bpf_trans/2),1e3,firdes.WIN_BLACKMAN)), 1)
        self.fft_filter_xxx_0.declare_sample_delay(0)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(2*(1+0.0), 0.25*gmu*gmu, mu, gmu, 0.005)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_threshold_ff_0 = blocks.threshold_ff(low, hi, 0)
        self.blocks_tagged_stream_to_pdu_1 = blocks.tagged_stream_to_pdu(blocks.float_t, 'packet_len')
        self.blocks_tagged_stream_to_pdu_0_0_0 = blocks.tagged_stream_to_pdu(blocks.float_t, 'packet_len')
        self.blocks_tagged_stream_to_pdu_0_0 = blocks.tagged_stream_to_pdu(blocks.float_t, 'packet_len')
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.float_t, 'packet_len')
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_stream_to_tagged_stream_1 = blocks.stream_to_tagged_stream(gr.sizeof_float, 1, 512, "packet_len")
        self.blocks_stream_to_tagged_stream_0_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_float, 1, 512, "packet_len")
        self.blocks_stream_to_tagged_stream_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_float, 1, 512, "packet_len")
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_float, 1, 512, "packet_len")
        self.blocks_rotator_cc_1 = blocks.rotator_cc((-1.0*fsk_hi_tone/ch_rate)*2*math.pi)
        self.blocks_rotator_cc_0_0 = blocks.rotator_cc((-1.0*fsk_lo_tone/ch_rate)*2*math.pi)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((gain, ))
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(filter_len, 1.0/filter_len, 4000)
        self.blocks_keep_m_in_n_0 = blocks.keep_m_in_n(gr.sizeof_short, 2, sps, 0)
        self.blocks_float_to_short_0 = blocks.float_to_short(1, 1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, 0)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_1 = blocks.complex_to_mag(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_burst_tagger_1 = blocks.burst_tagger(gr.sizeof_float)
        self.blocks_burst_tagger_1.set_true_tag('burst_start',True)
        self.blocks_burst_tagger_1.set_false_tag('burst_stop',False)
        	
        self.blocks_burst_tagger_0 = blocks.burst_tagger(gr.sizeof_float)
        self.blocks_burst_tagger_0.set_true_tag('burst_start',True)
        self.blocks_burst_tagger_0.set_false_tag('burst_stop',False)
        	
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(ch_rate/(2*math.pi*(10e3)/8.0))
        self.analog_agc_xx_0 = analog.agc_ff(1e-4, 1.0, 1.0)
        self.analog_agc_xx_0.set_max_gain(65536)
        self.analog_agc2_xx_1 = analog.agc2_ff(0.5, 0.00001, 1.0, 1.0)
        self.analog_agc2_xx_1.set_max_gain(65536)
        self.analog_agc2_xx_0 = analog.agc2_ff(0.5, 0.00001, 1.0, 1.0)
        self.analog_agc2_xx_0.set_max_gain(65536)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self, 'softbits'))    
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0_0, 'pdus'), (self, 'hi_symb'))    
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0_0_0, 'pdus'), (self, 'lo_symb'))    
        self.msg_connect((self.blocks_tagged_stream_to_pdu_1, 'pdus'), (self, 'afsk'))    
        self.msg_connect((self.Merapi_frame_detect_0, 'frame out'), (self, 'frame_out'))    
        self.connect((self.analog_agc2_xx_0, 0), (self.blocks_stream_to_tagged_stream_0_0, 0))    
        self.connect((self.analog_agc2_xx_0, 0), (self.blocks_sub_xx_0, 0))    
        self.connect((self.analog_agc2_xx_1, 0), (self.blocks_stream_to_tagged_stream_0_0_0, 0))    
        self.connect((self.analog_agc2_xx_1, 0), (self.blocks_sub_xx_0, 1))    
        self.connect((self.analog_agc_xx_0, 0), (self.blocks_burst_tagger_1, 0))    
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.fft_filter_xxx_0, 0))    
        self.connect((self.blocks_burst_tagger_0, 0), (self.blocks_stream_to_tagged_stream_1, 0))    
        self.connect((self.blocks_burst_tagger_0, 0), (self, 1))    
        self.connect((self.blocks_burst_tagger_1, 0), (self.blocks_stream_to_tagged_stream_0, 0))    
        self.connect((self.blocks_complex_to_mag_0, 0), (self.analog_agc2_xx_0, 0))    
        self.connect((self.blocks_complex_to_mag_1, 0), (self.analog_agc2_xx_1, 0))    
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.blocks_delay_0, 0), (self.blocks_null_sink_0, 0))    
        self.connect((self.blocks_delay_0, 0), (self, 0))    
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_rotator_cc_0_0, 0))    
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_rotator_cc_1, 0))    
        self.connect((self.blocks_float_to_short_0, 0), (self.blocks_burst_tagger_0, 1))    
        self.connect((self.blocks_float_to_short_0, 0), (self.blocks_keep_m_in_n_0, 0))    
        self.connect((self.blocks_float_to_short_0, 0), (self, 2))    
        self.connect((self.blocks_keep_m_in_n_0, 0), (self.blocks_burst_tagger_1, 1))    
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_threshold_ff_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_moving_average_xx_0, 0))    
        self.connect((self.blocks_rotator_cc_0_0, 0), (self.root_raised_cosine_filter_0, 0))    
        self.connect((self.blocks_rotator_cc_1, 0), (self.root_raised_cosine_filter_1, 0))    
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_tagged_stream_to_pdu_0, 0))    
        self.connect((self.blocks_stream_to_tagged_stream_0_0, 0), (self.blocks_tagged_stream_to_pdu_0_0, 0))    
        self.connect((self.blocks_stream_to_tagged_stream_0_0_0, 0), (self.blocks_tagged_stream_to_pdu_0_0_0, 0))    
        self.connect((self.blocks_stream_to_tagged_stream_1, 0), (self.blocks_tagged_stream_to_pdu_1, 0))    
        self.connect((self.blocks_sub_xx_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_float_to_short_0, 0))    
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.Merapi_frame_detect_0, 0))    
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))    
        self.connect((self.fft_filter_xxx_0, 0), (self.blocks_burst_tagger_0, 0))    
        self.connect((self.fft_filter_xxx_0, 0), (self.blocks_float_to_complex_0, 0))    
        self.connect((self, 0), (self.blocks_delay_0, 0))    
        self.connect((self, 0), (self.pfb_arb_resampler_xxx_0, 0))    
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.analog_quadrature_demod_cf_0, 0))    
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.analog_agc_xx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))    
        self.connect((self.root_raised_cosine_filter_0, 0), (self.blocks_complex_to_mag_0, 0))    
        self.connect((self.root_raised_cosine_filter_1, 0), (self.blocks_complex_to_mag_1, 0))    

    def get_baud(self):
        return self.baud

    def set_baud(self, baud):
        self.baud = baud
        self.set_sps(int(self.ch_rate / self.baud))

    def get_bpf_trans(self):
        return self.bpf_trans

    def set_bpf_trans(self, bpf_trans):
        self.bpf_trans = bpf_trans
        self.fft_filter_xxx_0.set_taps((firdes.band_pass(0.1,self.ch_rate,self.fsk_lo_tone-(self.bpf_trans/2),self.fsk_hi_tone+(self.bpf_trans/2),1e3,firdes.WIN_BLACKMAN)))

    def get_filter_len(self):
        return self.filter_len

    def set_filter_len(self, filter_len):
        self.filter_len = filter_len
        self.blocks_moving_average_xx_0.set_length_and_scale(self.filter_len, 1.0/self.filter_len)

    def get_fsk_hi_tone(self):
        return self.fsk_hi_tone

    def set_fsk_hi_tone(self, fsk_hi_tone):
        self.fsk_hi_tone = fsk_hi_tone
        self.fft_filter_xxx_0.set_taps((firdes.band_pass(0.1,self.ch_rate,self.fsk_lo_tone-(self.bpf_trans/2),self.fsk_hi_tone+(self.bpf_trans/2),1e3,firdes.WIN_BLACKMAN)))
        self.blocks_rotator_cc_1.set_phase_inc((-1.0*self.fsk_hi_tone/self.ch_rate)*2*math.pi)

    def get_fsk_lo_tone(self):
        return self.fsk_lo_tone

    def set_fsk_lo_tone(self, fsk_lo_tone):
        self.fsk_lo_tone = fsk_lo_tone
        self.fft_filter_xxx_0.set_taps((firdes.band_pass(0.1,self.ch_rate,self.fsk_lo_tone-(self.bpf_trans/2),self.fsk_hi_tone+(self.bpf_trans/2),1e3,firdes.WIN_BLACKMAN)))
        self.blocks_rotator_cc_0_0.set_phase_inc((-1.0*self.fsk_lo_tone/self.ch_rate)*2*math.pi)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.blocks_multiply_const_vxx_1.set_k((self.gain, ))

    def get_gmu(self):
        return self.gmu

    def set_gmu(self, gmu):
        self.gmu = gmu
        self.digital_clock_recovery_mm_xx_0.set_gain_omega(0.25*self.gmu*self.gmu)
        self.digital_clock_recovery_mm_xx_0.set_gain_mu(self.gmu)

    def get_hi(self):
        return self.hi

    def set_hi(self, hi):
        self.hi = hi
        self.blocks_threshold_ff_0.set_hi(self.hi)

    def get_input_rate(self):
        return self.input_rate

    def set_input_rate(self, input_rate):
        self.input_rate = input_rate
        self.pfb_arb_resampler_xxx_0.set_rate(self.ch_rate / self.input_rate)

    def get_low(self):
        return self.low

    def set_low(self, low):
        self.low = low
        self.blocks_threshold_ff_0.set_lo(self.low)

    def get_mu(self):
        return self.mu

    def set_mu(self, mu):
        self.mu = mu
        self.digital_clock_recovery_mm_xx_0.set_mu(self.mu)

    def get_ch_rate(self):
        return self.ch_rate

    def set_ch_rate(self, ch_rate):
        self.ch_rate = ch_rate
        self.set_sps(int(self.ch_rate / self.baud))
        self.pfb_arb_resampler_xxx_0.set_rate(self.ch_rate / self.input_rate)
        self.fft_filter_xxx_0.set_taps((firdes.band_pass(0.1,self.ch_rate,self.fsk_lo_tone-(self.bpf_trans/2),self.fsk_hi_tone+(self.bpf_trans/2),1e3,firdes.WIN_BLACKMAN)))
        self.blocks_rotator_cc_1.set_phase_inc((-1.0*self.fsk_hi_tone/self.ch_rate)*2*math.pi)
        self.blocks_rotator_cc_0_0.set_phase_inc((-1.0*self.fsk_lo_tone/self.ch_rate)*2*math.pi)
        self.analog_quadrature_demod_cf_0.set_gain(self.ch_rate/(2*math.pi*(10e3)/8.0))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.root_raised_cosine_filter_1.set_taps(firdes.root_raised_cosine(1, self.sps*1.0, 1.0, 0.7, 4*self.sps))
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.sps*1.0, 1.0, 0.7, 4*self.sps))
        self.blocks_keep_m_in_n_0.set_n(self.sps)
