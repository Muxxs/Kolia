#coding=utf-8
'''
Requirements:
+ pyaudio - `pip install pyaudio`
+ py-webrtcvad - `pip install webrtcvad`
'''
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
CHUNK_DURATION_MS = 30       # supports 10, 20 and 30 (ms)
PADDING_DURATION_MS = 1500   # 1 sec jugement
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


def say(words):
    from aip import AipSpeech
    """ 你的 APPID AK SK """
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
        with open('auido.wav', 'wb') as f:
            f.write(result)
    playwma("audio.wav")
def handle_int(sig, chunk):
    global leave, got_a_sentence
    leave = True
    got_a_sentence = True
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def wav_to_text(wav_file):
    import os
    # 设置应用信息
    baidu_server = "https://openapi.baidu.com/oauth/2.0/token?"
    grant_type = "client_credentials"
    client_id = " fszBbd9xWKUqM9aZ6p5atNec"  # 填写API Key
    client_secret = "3b86c60023658c183e20621810427aa7"  # 填写Secret Key

    # 合成请求token的URL
    url = baidu_server + "grant_type=" + grant_type + "&client_id=" + client_id + "&client_secret=" + client_secret

    # 获取token
    res = urllib2.urlopen(url).read()
    data = json.loads(res)
    token = data["access_token"]
    print token

    # 设置音频属性，根据百度的要求，采样率必须为8000，压缩格式支持pcm（不压缩）、wav、opus、speex、amr
    VOICE_RATE = 16000
    WAVE_FILE = wav_file  # 音频文件的路径
    USER_ID = "hail_hydra"  # 用于标识的ID，可以随意设置
    WAVE_TYPE = "wav"

    # 打开音频文件，并进行编码
    f = open(WAVE_FILE, "r")
    speech = base64.b64encode(f.read())
    size = os.path.getsize(WAVE_FILE)
    update = json.dumps(
        {"format": WAVE_TYPE, "rate": VOICE_RATE, 'channel': 1, 'cuid': USER_ID, 'token': token, 'speech': speech,
         'len': size})
    headers = {'Content-Type': 'application/json'}
    url = "http://vop.baidu.com/server_api"
    req = urllib2.Request(url, update, headers)

    r = urllib2.urlopen(req)

    t = r.read()
    result = json.loads(t)
    print result
    if result['err_msg'] == 'success.':
        word = result['result'][0].encode('utf-8')
        if word != '':
            if word[len(word) - 3:len(word)] == '，':
                print word[0:len(word) - 3]
            else:
                print word
        else:
            print "音频文件不存在或格式错误"
    else:
        print "错误"

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
    say("你好")
    wav_to_text("recording.wav")
    print res
    return "break"


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
    res=read()
    if res=="break":
        leave=True
stream.close()
