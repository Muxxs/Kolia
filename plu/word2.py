#coding=utf-8
def wordstotwo(words):
    return ' '.join([bin(ord(c)).replace('0b', '') for c in words])
def twotowords(two):
    return ''.join([chr(i) for i in [int(b, 2) for b in two.split(' ')]])