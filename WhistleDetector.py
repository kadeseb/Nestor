#!/usr/bin/python3
#! -*- coding: utf8 -*-
import pyaudio
import wave
import numpy
import time
import struct

'''
Detecte un sifflement
'''

class WhistleDetector:
    LOST_BITS = 7
    CHUNK = 512  # FFT block size
    RATE = 22100
    CHANNELS = 1
    FORMAT = pyaudio.paInt16
    TRIGGER_DELAY = 0.250

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.bitmask = ((-1) >> self.LOST_BITS) << self.LOST_BITS
        self.currentWhistling = False

    def __del__(self):
        if (self.stream != None)
        self.stream.stop_stream()
        self.stream.close()

        if (self.p != None):
            self.p.terminate()

    def _openStream(self):
        self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)

    def _computeSpector(self):
        data = self.stream.read(self.CHUNK)
        data = struct.unpack('<%dh'%(self.CHUNK), data)
        data = [x & self.bitmask for x in data]

        return numpy.fft.rfft(data)/2

    def waitForWhistle(self):
        self._openStream()
        self.currentWhistling = False
        whistleStartTime = None

        while(True):
            spector = self._computeSpector()
            isWhistle, p0, p1 = self.is_whistle(spector)

            if (isWhistle):
                if (whistleStartTime == None):
                    whistleStartTime = time.time()

                if ((time.time() - whistleStartTime) >= self.TRIGGER_DELAY):
                    return
            else:
                whistleStartTime = None

    # given a frequency in Hz, compute which cell of the fft result
    # will contain it
    @staticmethod
    def freq_bin(freq):
        chunk_duration = float(WhistleDetector.CHUNK) / WhistleDetector.RATE
        cycles_per_chunk = freq * chunk_duration
        return int(cycles_per_chunk)

    # given an array with "islands" of consecutive nonzero values
    # separated by spans of consecutive zeroes, compute the fraction
    # of the mass contained in the island at <pos>
    @staticmethod
    def piece_fraction(spector, pos):
        window_start = pos
        window_end = pos
        while window_start > 0 and spector[window_start] > 0.00001:
            window_start -= 1
        while window_end < len(spector)-1 and spector[window_end] > 0.000001:
            window_end += 1
        if sum(spector) < 0.000001:
            return 0
        return sum(spector[window_start:window_end]) / sum(spector)

    # filter (make zero) everything lower than 1/16 the maximal value
    @staticmethod
    def filter_weaks(spector):
        percent = max(spector) / 16
        vals = [x if x > percent else 0 for x in spector]
        return vals

    @staticmethod
    def avg(values):
        return sum(values) / float(len(values))

    def is_whistle(self, spector):
        avg_min = self.freq_bin(200)
        avg_max = self.freq_bin(10000)
        whistle_min = self.freq_bin(1000)
        whistle_max = self.freq_bin(3000)

        avg_area = list(map(lambda x:x**2,abs(spector[avg_min:avg_max])))
        whistle_area = list(map(lambda x:x**2,abs(spector[whistle_min:whistle_max])))
        filt_avg_area = self.filter_weaks(avg_area)
        peak = numpy.argmax(filt_avg_area)
        paramA = self.avg(whistle_area) > 2*self.avg(avg_area)
        paramB = self.piece_fraction(filt_avg_area, peak) > 0.9
        return (paramA and paramB, self.piece_fraction(filt_avg_area, peak), self.avg(whistle_area) / self.avg(avg_area))

'''
if (__name__ == "__main__"):
    # how many of the least-significant bits of each sample to remove.
    # used to simulate low-resolution samples
    LOST_BITS = 7
    CHUNK = 512  # FFT block size
    RATE = 22100

    CHANNELS = 1
    FORMAT = pyaudio.paInt16

    SCREEN_SIZE = (512, 512)

    screen = pygame.display.set_mode(SCREEN_SIZE)

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    # a mask of all-ones except for LOST_BITS least significant bits
    bitmask = ((-1) >> LOST_BITS) << LOST_BITS

    try:
        run = True
        pause_frames = 0
        while True:
            pause_frames = max(0, pause_frames - 1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            if not run:
                break

            data = stream.read(CHUNK)
            data = struct.unpack('<%dh'%(CHUNK), data)
            data = [x & bitmask for x in data]

            spector = numpy.fft.rfft(data)/2
            whistle_detected,p1,p2 = is_whistle(spector)

            if whistle_detected:
                print("YES %.2f %.2f"%(p1,p2))
            else:
                print("NO %.2f %.2f"%(p1,p2))
            if pause_frames > 0:
                continue
            if whistle_detected:
                pause_frames = 40
                color = (255,255,0)
            else:
                color = (255,0,0)
            screen.fill((0,0,0))
            for i in range(0,len(spector),4):
                pygame.draw.line(screen, color, (i,SCREEN_SIZE[1]), (i, SCREEN_SIZE[1]-int(abs(spector[i])/65536. * SCREEN_SIZE[1])))
            for i in range(0, 15000, 1000):
                x = freq_bin(i)
                pygame.draw.line(screen, (0,0,255), (x,SCREEN_SIZE[1]), (x, 0))
            pygame.display.flip()
    finally:
        pygame.quit()
        stream.stop_stream()
        stream.close()
        p.terminate()
'''
