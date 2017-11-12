#coding=utf-8
import webrtcvad
import collections
import sys
import signal
import pyaudio
import base64
import urllib2
import urllib
import json
import wave
from array import array
from struct import pack
import wave
import time

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK_DURATION_MS = 30  # supports 10, 20 and 30 (ms)
PADDING_DURATION_MS = 1500  # 1 sec jugement
CHUNK_SIZE = int(RATE * CHUNK_DURATION_MS / 1000)  # chunk to read
CHUNK_BYTES = CHUNK_SIZE * 2  # 16bit = 2 bytes, PCM
NUM_PADDING_CHUNKS = int(PADDING_DURATION_MS / CHUNK_DURATION_MS)
# NUM_WINDOW_CHUNKS = int(240 / CHUNK_DURATION_MS)
NUM_WINDOW_CHUNKS = int(400 / CHUNK_DURATION_MS)  # 400 ms/ 30ms  ge
NUM_WINDOW_CHUNKS_END = NUM_WINDOW_CHUNKS * 2
START_OFFSET = int(NUM_WINDOW_CHUNKS * CHUNK_DURATION_MS * 0.5 * RATE)
vad = webrtcvad.Vad(1)
pa = pyaudio.PyAudio()
stream = pa.open(format=FORMAT,
                     channels=CHANNELS,
                     rate=RATE,
                     input=True,
                     start=False,
                     # input_device_index=2,
                     frames_per_buffer=CHUNK_SIZE)
got_a_sentence = False
leave = False
def playwma(filename):
    import pyaudio
    import wave

    # define stream chunk
    chunk = 1024

    # open a wav format music
    f = wave.open(filename)
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # open stream
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)
    # read data
    data = f.readframes(chunk)

    # paly stream
    while data != '':
        stream.write(data)
        data = f.readframes(chunk)

        # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()

def playmp3(filename):
    import pygame,time
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(loops=0, start=0.0)


def say(words):
    from aip import AipSpeech
    APP_ID = '8952809'
    API_KEY = ' fszBbd9xWKUqM9aZ6p5atNec'
    SECRET_KEY = '3b86c60023658c183e20621810427aa7'
    aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = aipSpeech.synthesis(words, 'zh', 1, {
        'vol': 5,
    })
    print result
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('auio.wma', 'wb') as f:
            f.write(result)
    playmp3("auio.mp3")

def say_word(text):
    import os
    return os.system("say "+text)

def handle_int(sig, chunk):
    global leave, got_a_sentence
    leave = True
    got_a_sentence = True
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def wav_to_text(wav_file):
    from aip import AipSpeech
    APP_ID = '8952809'
    API_KEY = 'fszBbd9xWKUqM9aZ6p5atNec'
    SECRET_KEY = '3b86c60023658c183e20621810427aa7'
    aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    res = aipSpeech.asr(get_file_content(wav_file), 'pcm', 16000, {
        'lan': 'zh',
    })
    return res



def record_to_file(path, data, sample_width):
    "Records from the microphone and outputs the resulting data to 'path'"
    # sample_width, data = record()
    data = pack('<' + ('h' * len(data)), *data)
    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()


def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 32767  # 16384
    times = float(MAXIMUM) / max(abs(i) for i in snd_data)
    r = array('h')
    for i in snd_data:
        r.append(int(i * times))
    return r
signal.signal(signal.SIGINT, handle_int)



def read():
    print "read"
    res=wav_to_text("recording.wav")
    for (i,l) in res.items():
        text=str(l).decode('unicode_escape')
        if text.find("[")==-1 and text.find("]")==-1:
            pass
        else:
            text=text.split("'")[1]
            print text
            return text




def recording():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK_DURATION_MS = 30  # supports 10, 20 and 30 (ms)
    PADDING_DURATION_MS = 1500  # 1 sec jugement
    CHUNK_SIZE = int(RATE * CHUNK_DURATION_MS / 1000)  # chunk to read
    CHUNK_BYTES = CHUNK_SIZE * 2  # 16bit = 2 bytes, PCM
    NUM_PADDING_CHUNKS = int(PADDING_DURATION_MS / CHUNK_DURATION_MS)
    # NUM_WINDOW_CHUNKS = int(240 / CHUNK_DURATION_MS)
    NUM_WINDOW_CHUNKS = int(400 / CHUNK_DURATION_MS)  # 400 ms/ 30ms  ge
    NUM_WINDOW_CHUNKS_END = NUM_WINDOW_CHUNKS * 2
    START_OFFSET = int(NUM_WINDOW_CHUNKS * CHUNK_DURATION_MS * 0.5 * RATE)
    vad = webrtcvad.Vad(1)

    pa = pyaudio.PyAudio()
    stream = pa.open(format=FORMAT,
                     channels=CHANNELS,
                     rate=RATE,
                     input=True,
                     start=False,
                     # input_device_index=2,
                     frames_per_buffer=CHUNK_SIZE)
    got_a_sentence = False
    leave = False
    while not leave:
        ring_buffer = collections.deque(maxlen=NUM_PADDING_CHUNKS)
        triggered = False
        voiced_frames = []
        ring_buffer_flags = [0] * NUM_WINDOW_CHUNKS
        ring_buffer_index = 0

        ring_buffer_flags_end = [0] * NUM_WINDOW_CHUNKS_END
        ring_buffer_index_end = 0
        buffer_in = ''
        # WangS
        raw_data = array('h')
        index = 0
        start_point = 0
        StartTime = time.time()
        print("* recording: ")
        stream.start_stream()

        while not got_a_sentence and not leave:
            chunk = stream.read(CHUNK_SIZE)
            # add WangS
            raw_data.extend(array('h', chunk))
            index += CHUNK_SIZE
            TimeUse = time.time() - StartTime

            active = vad.is_speech(chunk, RATE)

            sys.stdout.write('1' if active else '_')
            ring_buffer_flags[ring_buffer_index] = 1 if active else 0
            ring_buffer_index += 1
            ring_buffer_index %= NUM_WINDOW_CHUNKS

            ring_buffer_flags_end[ring_buffer_index_end] = 1 if active else 0
            ring_buffer_index_end += 1
            ring_buffer_index_end %= NUM_WINDOW_CHUNKS_END

            # start point detection
            if not triggered:
                ring_buffer.append(chunk)
                num_voiced = sum(ring_buffer_flags)
                if num_voiced > 0.8 * NUM_WINDOW_CHUNKS:
                    sys.stdout.write(' Open ')
                    triggered = True
                    start_point = index - CHUNK_SIZE * 20  # start point
                    # voiced_frames.extend(ring_buffer)
                    ring_buffer.clear()
            # end point detection
            else:
                # voiced_frames.append(chunk)
                ring_buffer.append(chunk)
                num_unvoiced = NUM_WINDOW_CHUNKS_END - sum(ring_buffer_flags_end)
                if num_unvoiced > 0.90 * NUM_WINDOW_CHUNKS_END or TimeUse > 10:
                    sys.stdout.write(' Close ')
                    triggered = False
                    got_a_sentence = True

            sys.stdout.flush()

        sys.stdout.write('\n')
        # data = b''.join(voiced_frames)

        stream.stop_stream()
        print("* done recording")
        got_a_sentence = False

        # write to file
        raw_data.reverse()
        for index in range(start_point):
            raw_data.pop()
        raw_data.reverse()
        raw_data = normalize(raw_data)
        record_to_file("recording.wav", raw_data, 2)
        leave=True
    stream.close()
    return 1
left=False
while not left:
    record=recording()
    res=read()
    if res == "break":
        left=True
    else:
        print res
        from plu import sendMessage
        if res==None:
            pass
        else:
            print say_word(sendMessage.sendMessage(res,"1"))
