#coding=utf-8
import exercise
from pub import get_config


def play_mp3(filename):
    import pygame
    file = filename
    pygame.mixer.init()
    print("播放音乐")
    track = pygame.mixer.music.load(file)
    pygame.mixer.music.play()
def say(word):
    import os
    return os.system("say "+word)
def translate(res):
    from bosonnlp import BosonNLP
    nlp = BosonNLP("nPom9h4a.18434.tEA4SsUlkG8g")
    return nlp.sentiment(res)[0]
def wake(words):
    key_words= get_config.get_wake()
    if words.find(key_words)<>-1:
        return 1
def text(content):
    Main_word="贾维斯"
    if content[:3]== Main_word or content.find(Main_word) <> -1:
        global model
        model=1
        exercise.cut_word(content)
    else:
        feel=translate(content)[0]
        global The_feel
        if int(feel) >=0.5 :
            The_feel=True
        else:
            The_feel=False
        say_word=exercise.cut_word(content)
        return say_word
