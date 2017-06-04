# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 23:03:36 2017

@author: SiqiCai
"""
import numpy as np
import matplotlib.pyplot as plt
#from scipy import fftpack
import matplotlib.ticker as ticker

def txtRead():
    txtFile = open('C117-C305_Sitzbeschl_10Heide-km_Polaritaet-korrigiert_RD-KIS_Eggers_ASCII.txt.vda')#(path) path = 'C:\Users\SiqiCai\myPython\01-FFT_RoughRoadSignal\C117-C305_Sitzbeschl_10Heide-km_Polaritaet-korrigiert_RD-KIS_Eggers_ASCII.txt.vda'
    txtLines = txtFile.readlines()
    txtList = [[] for i in range(17)]
    txtFile.close()
    for txtLine in txtLines:
        txtDatas = txtLine.replace(',','.').split('\t')
        txtDatas = [float(txtDatas) for txtDatas in txtDatas]
        i = 0
        for txtData in txtDatas:
            txtList[i].append(txtData)
            i = i + 1
            
    return txtList
    
def fftTrans(samplingRate, dataList):
    fft_size = len(dataList)
    #timeList = np.arange(0, fft_size*1.0/samplingRate, 1.0/samplingRate)
    dataFFT = np.fft.rfft(dataList)/fft_size
    dataFreq = np.linspace(0, samplingRate/2, fft_size/2 + 1)
    abs_dataFFT = np.abs(dataFFT)
    
    return dataFreq, abs_dataFFT

def writeTxt(dataX, dataY, path):
    ''' 1st method:
    datas = [dataX, dataY]
    data_csv = []
    for i in map(list, zip(*datas)):
        data_csv.append(i)
    np.savetxt(path, data_csv, fmt='%s',delimiter=',')
    
    #2 nd method:
    np.savetxt(path, np.c_[dataX, dataY], fmt='%s, %s')
    
    '''
    #3 rd way
    np.savetxt(path, list(zip(dataX, dataY)), fmt='%s, %s')
    
    return ''

def main():
    txtList = txtRead()
    samplingRate = 1000
    # fft for every channel
    for i in range(13, 16):
        dataFreq, abs_dataFFT = fftTrans(samplingRate, txtList[i])
        
        #wirte data into txt
        txtPath = 'Channel' + str(i).zfill(2) + '-afterFFT.csv'
        figName = 'Channel' + str(i).zfill(2) + '.png'
        writeTxt(dataFreq, abs_dataFFT, txtPath)
        
        #data plot and save as pics
        fft_size = len(txtList[i])
        timeList = np.arange(0, fft_size*1.0/samplingRate, 1.0/samplingRate)
        #plt.figure(figsize=(8,4))
        
        ax = plt.subplot(311)
        plt.plot(timeList, txtList[i])
        plt.xlabel('time (s)')
        ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(20))
        ax.set_xlim(0,1200)
        ax.set_ylim(-5,5)
        plt.ylabel('g (m/$s^2$)')
        plt.title('Raw Data')
        
        ax = plt.subplot(312)
        plt.plot(dataFreq, abs_dataFFT)
        plt.xlabel('Frequency (Hz)')
        ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(20))
        ax.set_xlim(0,500)
        ax.set_ylim(0,0.02)
        plt.ylabel('Amplitude')
        plt.title('FFT Trans')
        
        ax = plt.subplot(313)
        plt.plot(dataFreq, abs_dataFFT)
        plt.xlabel('Frequency (Hz)')
        ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
        ax.set_xlim(0,40)
        ax.set_ylim(0,0.02)
        plt.ylabel('Amplitude')
        plt.title('FFT Trans Details @ 0 ~ 40')
        plt.tight_layout()
        #plt.savefig('x.svg')
        plt.savefig(figName,dpi=600)
        plt.close('all')
        
main()
