#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Felipe Espic

DESCRIPTION:
This script extracts low-dimensional acoustic parameters from a wave file.
Then, it resynthesises the signal from these features.
Features:
- m_mag_mel_log: Mel-scaled Log-Mag (dim=nbins_mel,   usually 60).
- m_real_mel:    Mel-scaled real    (dim=nbins_phase, usually 45).
- m_imag_mel:    Mel-scaled imag    (dim=nbins_phase, usually 45).
- v_lf0:         Log-F0 (dim=1).

INSTRUCTIONS:
This demo should work out of the box. Just run it by typing: python <script name>
If wanted, you can modify the input options and/or perform some modification to the
extracted features before re-synthesis. See the main function below for details.
"""
import sys, os
this_dir = os.getcwd()
sys.path.append(os.path.realpath(this_dir + '/../src'))
import numpy as np
import libutils as lu
import libaudio as la
from libplot import lp
import magphase as mp

def plots(m_mag_mel_log, m_real_mel, m_imag_mel, v_lf0):
    lp.plotm(m_mag_mel_log)
    lp.title(' Mel-scaled Log-Magnitude Spectrum')
    lp.xlabel('Time (frames)')

    lp.ylabel('Mel-scaled frequency bins')

    lp.plotm(m_real_mel)
    lp.title('"R" Feature Phase Spectrum')
    lp.xlabel('Time (frames)')
    lp.ylabel('Mel-scaled frequency bins')

    lp.plotm(m_imag_mel)
    lp.title('"I" Feature Phase Spectrum')
    lp.xlabel('Time (frames)')
    lp.ylabel('Mel-scaled frequency bins')

    lp.figure()
    lp.plot(np.exp(v_lf0)) # unlog for better visualisation
    lp.title('F0')
    lp.xlabel('Time (frames)')
    lp.ylabel('F0')
    lp.grid()
    return


if __name__ == '__main__':  

    # INPUT:==============================================================================
    wav_file_orig = 'data_48k/wavs_nat/hvd_593.wav' # Original natural wave file. You can choose anyone provided in the /wavs_nat directory.
    out_dir       = 'data_48k/wavs_syn_ph_comp_dev_2' # Where the synthesised waveform will be stored.
    nbins_phase   = 45 # 45 #20 #45
    alpha_phase   = None # 0.99 # 0.6 # 0.77

    # PROCESS:============================================================================
    lu.mkdir(out_dir)

    # ANALYSIS:
    print("Analysing.....................................................")
    #m_mag_mel_log, m_real_mel, m_imag_mel, v_lf0, v_shift, fs, fft_len = mp.analysis_compressed_type1(wav_file_orig)

    # FALTA SMOOTH AVERAGE EN FILTER BANK!!!!!!!!!!!
    #m_mag_mel_log, m_real_mel, m_imag_mel, v_lf0, v_shift, fs, fft_len = mp.analysis_compressed_type1_with_phase_comp(wav_file_orig,
    #                                                                                                    nbins_mel=60, nbins_phase=nbins_phase)


    m_mag_mel_log, m_real_mel, m_imag_mel, v_lf0, v_shift, fs, fft_len = mp.analysis_compressed_type1_with_phase_comp_mcep(wav_file_orig,
                                                                                                        nbins_mel=60, nbins_phase=nbins_phase, alpha_phase=alpha_phase)

    # SYNTHESIS:
    print("Synthesising.................................................")
    #v_syn_sig = mp.synthesis_from_compressed_type1(m_mag_mel_log, m_real_mel, m_imag_mel, v_lf0, fs, fft_len)
    #v_syn_sig = mp.synthesis_from_compressed_type1_with_phase_comp(m_mag_mel_log, m_real_mel, m_imag_mel, v_lf0, fs)
    v_syn_sig = mp.synthesis_from_compressed_type1_with_phase_comp_mcep(m_mag_mel_log, m_real_mel, m_imag_mel, v_lf0, fs, alpha_phase=alpha_phase)


    # SAVE WAV FILE:=======================================================================
    print("Saving wav file..............................................")
    wav_file_syn = out_dir + '/' + lu.get_filename(wav_file_orig) + '_copy_syn_low_dim_ph_comp_prue_5_alpha_ph_None.wav'
    la.write_audio_file(wav_file_syn, v_syn_sig, fs)


    if False:
        pl(la.build_mel_curve(0.2, 2049))

    print('Done!')


