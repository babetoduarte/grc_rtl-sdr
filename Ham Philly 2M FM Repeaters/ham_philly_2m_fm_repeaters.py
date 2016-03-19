#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: HAM 2m FM Receiver
# Author: Jorge A. Duarte G.
# Description: An FM receiver for the 2m Ham radio Repeaters in Philadelphia, PA
# Generated: Fri Mar 11 12:25:11 2016
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

def struct(data): return type('Struct', (object,), data)()
from gnuradio import analog
from gnuradio import audio
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx


class ham_philly_2m_fm_repeaters(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="HAM 2m FM Receiver")

        ##################################################
        # Variables
        ##################################################
        self.repeaters = repeaters = struct({"a": 145270000, "b": 145410000, "c": 146685000, "d": 147030000, "e": 441700000, })
        self.repeater_chooser = repeater_chooser = repeaters.e
        self.variable_static_text_0 = variable_static_text_0 = repeater_chooser
        self.samp_rate = samp_rate = 2.4e6
        self.frequency = frequency = 441.700e6

        ##################################################
        # Blocks
        ##################################################
        self._repeater_chooser_chooser = forms.drop_down(
        	parent=self.GetWin(),
        	value=self.repeater_chooser,
        	callback=self.set_repeater_chooser,
        	label='repeater_chooser',
        	choices=[repeaters.a, repeaters.b, repeaters.c, repeaters.d, repeaters.e],
        	labels=["W3PVI", "KD3WT", "WM3PEN", "W3QV", "W3WAN"],
        )
        self.Add(self._repeater_chooser_chooser)
        self.wxgui_fftsink2_0_1 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=repeater_chooser,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="RF Spectrum",
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0_1.win)
        self._variable_static_text_0_static_text = forms.static_text(
        	parent=self.GetWin(),
        	value=self.variable_static_text_0,
        	callback=self.set_variable_static_text_0,
        	label='variable_static_text_0',
        	converter=forms.float_converter(),
        )
        self.Add(self._variable_static_text_0_static_text)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "rtl=0" )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(repeater_chooser, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(True, 0)
        self.rtlsdr_source_0.set_gain(10, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna("", 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=500,
                decimation=2400,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=48,
                decimation=50,
                taps=None,
                fractional_bw=None,
        )
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, 500000, 100000, 8000, firdes.WIN_HAMMING, 6.76))
        self.audio_sink_0 = audio.sink(48000, "", True)
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=50,
        	quad_rate=500000,
        	tau=75e-6,
        	max_dev=10e3,
          )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_nbfm_rx_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_nbfm_rx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.rational_resampler_xxx_1, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.rational_resampler_xxx_1, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.wxgui_fftsink2_0_1, 0))    

    def get_repeaters(self):
        return self.repeaters

    def set_repeaters(self, repeaters):
        self.repeaters = repeaters
        self.set_repeater_chooser(self.repeaters.e)

    def get_repeater_chooser(self):
        return self.repeater_chooser

    def set_repeater_chooser(self, repeater_chooser):
        self.repeater_chooser = repeater_chooser
        self._repeater_chooser_chooser.set_value(self.repeater_chooser)
        self.set_variable_static_text_0(self.repeater_chooser)
        self.rtlsdr_source_0.set_center_freq(self.repeater_chooser, 0)
        self.wxgui_fftsink2_0_1.set_baseband_freq(self.repeater_chooser)

    def get_variable_static_text_0(self):
        return self.variable_static_text_0

    def set_variable_static_text_0(self, variable_static_text_0):
        self.variable_static_text_0 = variable_static_text_0
        self._variable_static_text_0_static_text.set_value(self.variable_static_text_0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_0_1.set_sample_rate(self.samp_rate)

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency


def main(top_block_cls=ham_philly_2m_fm_repeaters, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
