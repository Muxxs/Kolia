#coding=utf-8
def get_config():
    try:
        fp=open("config.txt","rb")
        read=fp.read()
        fp.close()
        read=read.split("|")
        port=read[0]
        word_get=read[1]
        place_get=read[3]
        words_wake=read[2]
    except:
        port="8082"
        words_wake="贾维斯"
        place_get="北京"
        word_get=""
    return port,word_get,words_wake,place_get
def get_wordtext():
    return get_config()[1]
def get_porttext():
    return get_config()[0]
def rewrite_config(port,word_get):
    fp=open("config.txt","w+")
    return fp.write(port+"|"+word_get)
def get_places():
    return get_config()[3]
def get_wake():
    return get_config()[2]