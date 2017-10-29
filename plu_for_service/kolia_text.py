#coding=utf-8
import threading, time, random
def play_mp3(filename):
    import time
    import pygame
    file = filename
    pygame.mixer.init()
    print("播放音乐")
    track = pygame.mixer.music.load(file)
    pygame.mixer.music.play()
def say(word):

    play_mp3("say.mp3")
def try_understand(s):
    from bosonnlp import BosonNLP
    # 注意：在测试时请更换为您的API token。
    nlp = BosonNLP('nPom9h4a.18434.tEA4SsUlkG8g')
    import os
    feel=nlp.sentiment(s)
    result = nlp.depparser(s)

    print(' '.join(result[0]['word']))
    print(' '.join(result[0]['tag']))
    print(result[0]['head'])
    print(' '.join(result[0]['role']))
    text=""
    threading.Thread(target=say, args=(text), name='thread-' + str(i)).start()
def translate(res):
    from bosonnlp import BosonNLP
    nlp = BosonNLP("nPom9h4a.18434.tEA4SsUlkG8g")
    print nlp.sentiment(res)[0]