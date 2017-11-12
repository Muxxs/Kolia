#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def pass_word(word):
    The_word="要、打、闭、了、呢、哇、额、嗯、呀、吧、罢、呗、啵、啦、来、唻、了、嘞、哩、咧、咯、啰、喽、吗、嘛、嚜、么、哪、呢、呐、呵、哈、不、兮、般、则、连、罗、给、噻、哉"
    for  i in The_word.split("、"):
        if i==word:
            return 1
import urllib
import json
def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html
def turing(text):
    key = 'e8a9decd87a9422aa356554a8454a2c5'
    api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='
    while True:
        info = text
        request = api + info
        response = getHtml(request)
        dic_json = json.loads(response)
        return dic_json['text']
def cut_word(text):
    import jieba.posseg as pseg
    word=pseg.cut(text)
    global ver
    ver=[]
    words=[]
    for i in word:
        print i.word,i.flag
        if i.flag=="v":
            ver.append(i.word)
        words.append(str(i.flag).encode("utf-8")+","+str(i.word).encode("utf-8"))
    model=0
    ver_real=[]
    print ver
    if ver.__len__()==1:
        get_ver=0
        v_n=""
        for i in words:
            flag=str(i).encode("utf-8").split(",")[0]
            word_get=str(i).split(",")[1]
            if flag=="v":
                get_ver=1
            if flag=="n":
                if get_ver==1:
                    v_n=word_get
        if ver[0]==u"想":
            print v_n
        else:
            return ver[0]+v_n
    else:
        for i in ver:
            print i
            if i==u"想":
                model=1
                Start=0
                target=""
                for x in words:
                    word = str(x).split(",")[1]
                    flag = str(x).split(",")[0]
                    if Start==0:
                        if word==u"想":
                            Start=1
                    else:
                        if pass_word(word)<>1:
                            target=target+word
                return "target:"+target+"."
            else:
                model=0
                ver_get=0
                last_ver=""
                for x in words:
                    word = str(x).split(",")[1]
                    flag = str(x).split(",")[0]
                    if ver_get==1:
                        if flag=="n":
                            return last_ver+word
                        else:
                            last_ver=""
                            ver_get=""
                    else:
                        if flag=="v":
                            last_ver=word
                            ver_get=1
        return turing(text)
