#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Merapi Decode - PT. Datto Asia Teknologi
# Author: Handiko Gesang - Unit Rumah Produksi - PT. Datto Asia Teknologi
# Generated: Mon Jan  7 20:51:38 2019
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import Merapi
import osmosdr
import sip
import sys
import time


class merapi_decode(gr.top_block, Qt.QWidget):

    def __init__(self, path="gqrx_20180404_011711_144119900_300000_fc.raw", source=1):
        gr.top_block.__init__(self, "Merapi Decode - PT. Datto Asia Teknologi")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Merapi Decode - PT. Datto Asia Teknologi")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "merapi_decode")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.path = path
        self.source = source

        ##################################################
        # Variables
        ##################################################
        self.rate_bank = rate_bank = [2.4e6,300e3]
        self.device = device = ['rtl=0','file='+str(path),'rate=300e3','repeat=true','throttle=true']
        self.samp_rate = samp_rate = rate_bank[source]
        self.rfgain = rfgain = 30
        self.freq = freq = 433.25
        self.device_bank = device_bank = ['rtl=0',str(device[1]) + ',' + str(device[2]) + ',' + str(device[3]) + ',' + str(device[4])]

        ##################################################
        # Blocks
        ##################################################
        self.tab = Qt.QTabWidget()
        self.tab_widget_0 = Qt.QWidget()
        self.tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_0)
        self.tab_grid_layout_0 = Qt.QGridLayout()
        self.tab_layout_0.addLayout(self.tab_grid_layout_0)
        self.tab.addTab(self.tab_widget_0, 'RF Input')
        self.tab_widget_1 = Qt.QWidget()
        self.tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_1)
        self.tab_grid_layout_1 = Qt.QGridLayout()
        self.tab_layout_1.addLayout(self.tab_grid_layout_1)
        self.tab.addTab(self.tab_widget_1, 'Demodulation')
        self.top_grid_layout.addWidget(self.tab, 0,0,1,2)
        self._rfgain_range = Range(0.0, 49.0, 1.0, 30, 200)
        self._rfgain_win = RangeWidget(self._rfgain_range, self.set_rfgain, 'RF Gain (dB)', "counter_slider", float)
        self.tab_grid_layout_0.addWidget(self._rfgain_win, 2,1,1,1)
        self._freq_tool_bar = Qt.QToolBar(self)
        self._freq_tool_bar.addWidget(Qt.QLabel('Freq (MHz)'+": "))
        self._freq_line_edit = Qt.QLineEdit(str(self.freq))
        self._freq_tool_bar.addWidget(self._freq_line_edit)
        self._freq_line_edit.returnPressed.connect(
        	lambda: self.set_freq(eng_notation.str_to_num(str(self._freq_line_edit.text().toAscii()))))
        self.tab_grid_layout_0.addWidget(self._freq_tool_bar, 2,0,1,1)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=int(300e3),
                decimation=int(samp_rate),
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	4096, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	freq*1e6, #fc
        	300e3, #bw
        	'RF Spectrogram', #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)
        
        if not False:
          self.qtgui_waterfall_sink_x_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not True)
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [6, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])
        
        self.qtgui_waterfall_sink_x_0.set_intensity_range(-120, -20)
        
        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab_grid_layout_0.addWidget(self._qtgui_waterfall_sink_x_0_win, 1,0,1,2)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
        	1024, #size
        	2400, #samp_rate
        	'Softbits', #name
        	0 #number of inputs
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.1)
        self.qtgui_time_sink_x_0_0.set_y_axis(-3, 3)
        
        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")
        
        self.qtgui_time_sink_x_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, 'burst_start')
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        
        if not False:
          self.qtgui_time_sink_x_0_0.disable_legend()
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [2, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.tab_grid_layout_1.addWidget(self._qtgui_time_sink_x_0_0_win, 1,0,1,1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	8192*8, #size
        	48e3, #samp_rate
        	'AFSK Waveform', #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.2)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")
        
        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_POS, 0.0, 0.15, 0, 'burst_start')
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        
        if not False:
          self.qtgui_time_sink_x_0.disable_legend()
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["red", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab_grid_layout_1.addWidget(self._qtgui_time_sink_x_0_win, 0,0,1,1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	4096, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	freq*1e6, #fc
        	300e3, #bw
        	'RF Spectrum', #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-100, 0)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(0.2)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        
        if not False:
          self.qtgui_freq_sink_x_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab_grid_layout_0.addWidget(self._qtgui_freq_sink_x_0_win, 0,0,1,2)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + device_bank[source] )
        self.osmosdr_source_0.set_sample_rate(rate_bank[source])
        self.osmosdr_source_0.set_center_freq(freq*1e6, 0)
        self.osmosdr_source_0.set_freq_corr(55, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(rfgain, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.blocks_socket_pdu_0 = blocks.socket_pdu("TCP_SERVER", 'localhost', '52001', 10000, False)
        self.Merapi_parse_frame_0 = Merapi.parse_frame('merapi_log.csv')
        self.Merapi_merapi_rx_0 = Merapi.merapi_rx(1200, 1e3, 400, 2200.0, 1200.0, 10e3, 0.5, 0.7, 300e3, 0.5, 0.5)
        self.Merapi_iot_pub_0 = Merapi.iot_pub("api.thingspeak.com", '', "application/x-www-form-urlencoded", "*/*", "", "", "", "", "", "", "", "")

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.Merapi_merapi_rx_0, 'frame_out'), (self.Merapi_parse_frame_0, 'frame_in'))    
        self.msg_connect((self.Merapi_merapi_rx_0, 'softbits'), (self.qtgui_time_sink_x_0_0, 'in'))    
        self.msg_connect((self.Merapi_parse_frame_0, 'parse_out'), (self.Merapi_iot_pub_0, 'parse_in'))    
        self.msg_connect((self.Merapi_parse_frame_0, 'info_out'), (self.blocks_socket_pdu_0, 'pdus'))    
        self.connect((self.Merapi_merapi_rx_0, 0), (self.qtgui_freq_sink_x_0, 0))    
        self.connect((self.Merapi_merapi_rx_0, 1), (self.qtgui_time_sink_x_0, 0))    
        self.connect((self.Merapi_merapi_rx_0, 0), (self.qtgui_waterfall_sink_x_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.Merapi_merapi_rx_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "merapi_decode")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = path
        self.set_device(['rtl=0','file='+str(self.path),'rate=300e3','repeat=true','throttle=true'])

    def get_source(self):
        return self.source

    def set_source(self, source):
        self.source = source
        self.set_samp_rate(self.rate_bank[self.source])
        self.osmosdr_source_0.set_sample_rate(self.rate_bank[self.source])

    def get_rate_bank(self):
        return self.rate_bank

    def set_rate_bank(self, rate_bank):
        self.rate_bank = rate_bank
        self.set_samp_rate(self.rate_bank[self.source])
        self.osmosdr_source_0.set_sample_rate(self.rate_bank[self.source])

    def get_device(self):
        return self.device

    def set_device(self, device):
        self.device = device
        self.set_device_bank(['rtl=0',str(self.device[1]) + ',' + str(self.device[2]) + ',' + str(self.device[3]) + ',' + str(self.device[4])])

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_rfgain(self):
        return self.rfgain

    def set_rfgain(self, rfgain):
        self.rfgain = rfgain
        self.osmosdr_source_0.set_gain(self.rfgain, 0)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        Qt.QMetaObject.invokeMethod(self._freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.freq)))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.freq*1e6, 300e3)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq*1e6, 300e3)
        self.osmosdr_source_0.set_center_freq(self.freq*1e6, 0)

    def get_device_bank(self):
        return self.device_bank

    def set_device_bank(self, device_bank):
        self.device_bank = device_bank


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    return parser


def main(top_block_cls=merapi_decode, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
