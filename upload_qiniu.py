 #-*- coding: utf-8 -*-
 # 7dtime.com 时间管理 外包开发 
 # 7天时间,时间管理,时间清单APP,任务管理,gtd软件
 # 7天时间看一生,了解自己周期数据有效的改善提升自己.时间管理和清单管理可以科学性的完成梦想达到目标.你的时间花费在哪儿,你就会成为怎样的人
 # 5526555@qq.com
 # 4000076003 电话
import os,re
import sys

# from reload import reload
# reload(sys)
# sys.setdefaultencoding('utf-8')
from qiniu import Auth, put_file,PersistentFop, build_op, op_save, urlsafe_base64_encode

import qiniu.config
# from clipboard import get_paste_img_file
from ctypes import *
import time,os.path

class PinYin(object):  
    def __init__(self, dict_file='word.data'):  
        self.word_dict = {}  
        self.dict_file = dict_file  
  
  
    def load_word(self):  
        if not os.path.exists(self.dict_file):  
            raise IOError("NotFoundFile")  
  
        with open(self.dict_file) as f_obj:  
            for f_line in f_obj.readlines():  
                try:  
                    line = f_line.split(' ')
                    self.word_dict[line[0]] = line[1]  
                except:  
                    line = f_line.split(' ')  
                    self.word_dict[line[0]] = line[1]  
  
  
    def hanzi2pinyin(self, string="", firstLetter=False):  
        result = []  
        for char in string:  
            key = '%X' % ord(char)
            if not self.word_dict.get(key):
                result.append(char)
            else:
                if firstLetter:
                    result.append(self.word_dict.get(key, char).split()[0][:-1].lower()[0])
                else:
                    result.append(self.word_dict.get(key, char).split()[0][:-1].lower())
                  
        return ''.join(result)
  

    def hanzi2pinyin_split(self, string="", split=""):  
        result = self.hanzi2pinyin(string=string)  
        if split == "":  
            return result  
        else:  
            return split.join(result)

pinyin3 = PinYin()
pinyin3.load_word()

access_key = "xxx" # 填入你的AK
secret_key = "xxx" # 填入你的SK
bucket_name = "d7game" # 填入你的七牛空间名称
url = "http://cdn.7dtime.com" # 填入你的域名地址

q = Auth(access_key, secret_key)
mime_type = "image/jpeg"
params = {'x:a': 'a'}

file_max_len = 15
video_template = '{%% raw %%}' + "\n" + \
'<video id="my-video" class="video-js" controls preload="auto" width="100%%"' + \
' poster="%s" data-setup=\'{"aspectRatio":"16:9"}\'>' + "\n" + \
' <source src="%s" type="video/mp4" >' + "\n" + \
' <p class="vjs-no-js">' + "\n" +  \
' To view this video please enable JavaScript, and consider upgrading to a web browser that' + \
' <a href="http://videojs.com/html5-video-support/" target="_blank">supports HTML5 video</a>'+ \
'</p>'+ "\n" + \
'</video>' + "\n" + \
'{%% endraw %%}'

def is_video(filename):
    return filename.endswith(".mp4") or filename.endswith(".MP4")

def upload_qiniu(path):
    dirname, filename = os.path.split(path)
    filename = pinyin3.hanzi2pinyin(string=filename, firstLetter=True)

    filename = re.sub(r'[^.a-zA-Z0-9_]+', '', filename)
    filename = filename[-15:]
    daytime = time.strftime('%Y-%m-%d') 
    key = 'time_tlog/%s_%s' % (daytime,filename)
    # key = key.encode('utf8')
    token = q.upload_token(bucket_name, key)
    # print (daytime)
    progress_handler = lambda progress, total: progress
    markdown_url = ''
    if is_video(filename):
        mime_type="video/mp4"
        video_url = "%s/%s" % (url, key)
        poster_url = os.path.splitext(key)[0] + '.jpg'
        poster_url = url + '/' + poster_url
        
        markdown_url = video_template % (poster_url, video_url)
    else:
        mime_type="image/jpeg"
        markdown_url = "![](%s/%s?imageView/2/w/620/h/667)" % (url, key)

    f = open('markdown.txt', 'w')
    f.write(markdown_url)
    f.flush()
    f.close()

    ret, info = put_file(token, key, path, params, mime_type, progress_handler=progress_handler)
    return ret != None and ret['key'] == key

def get_video_frame(path):
    key = path

    fops = 'vframe/jpg/offset/10/w/480/h/360'
    #pipeline = 'abc'
    saveas_key = urlsafe_base64_encode(bucket_name + ':' + os.path.splitext(path)[0] + '.jpg')
    fops = fops + '|saveas/' + saveas_key
    print(saveas_key)
    policy = {
        'scope': key,
        'deadline': 0,
        'persistentOps':fops
        #'persistentPipeline': pipeline
    }

    pfop = PersistentFop(q, bucket_name)
    ops = []
    ops.append(fops)
    ret, info = pfop.execute(key, ops, 1)
    print(ret)
    print(info)


#get_video_frame('time_tlog/2017-11-26_70414_haima.mp4')

if __name__ == '__main__':
    path = sys.argv[1]
    # newfile = img_file = get_paste_img_file() 
    # print (newfile)
    
    ret = upload_qiniu(path)
    # print (ret)
    # print (path)
    dirname, filename = os.path.split(path)
    filename = pinyin3.hanzi2pinyin(string=filename, firstLetter=True)
    filename = re.sub(r'[^.a-zA-Z0-9_]+', '', filename)
    filename = filename[-15:]
    daytime = time.strftime('%Y-%m-%d') 
    seo = 'time_tlog' 
    name = '%s/%s_%s' % (seo,daytime,filename)   #  以前是markdown
    if ret:
        #markdown_url = ''
        if is_video(filename):
            #video_url = "%s/%s" % (url, name)
            get_video_frame(name)
            #poster_url = os.path.splitext(name)[0] + '.jpg'
            #poster_url = url + '/' + poster_url
            
            #markdown_url = video_template % (poster_url, video_url)
        else:
            pass
            # name = os.path.split(path)[1]
            #markdown_url = "![](%s/%s?imageView/2/w/620/h/667)" % (url, name)

        #f = open('markdown.txt', 'w')
        #f.write(markdown_url)
        #f.flush()
        #f.close()
        # make it to clipboard
        #ahk = cdll.AutoHotkey # load AutoHotkey
        #ahk.ahktextdll("") # start script in persistent mode (wait for action)
        #while not ahk.ahkReady(): # Wait for AutoHotkey.dll to start
        #    time.sleep(0.01)
        #ahk.ahkExec(u"clipboard = %s" % markdown_url)
    else:
        print ("upload_failed")