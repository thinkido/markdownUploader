# 简介
  markdown 图片和视频文件上传插件1秒完成上传. windows系统下python开发的插件,可以快速上传图片,视频后自动生成markdown格式字符.
  实现Windows上通过ctrl+alt+c -> alt+v往Markdown文档中插入图片

## 使用方法
选中图片文件，按ctrl+alt+c，此时会跳出cmd窗口，当该窗口自动关闭之后，按alt+v就会在Markdown文档中插入图片

## ~~旧方法~~
将图片上传到七牛云存储并直接返回markdown可用的图片链接
功能虽然很简单，但确实刚需啊！！！以前写个markdown想要贴个图简直让人崩溃啊！！

 - 你可能先要截个图
 - 然后打开浏览器
 - 打开你的图床网站
 - 点击上传图片
 - 等待上传完成
 - 复制外链
 - 返回markdown
当然这是只是一个url，你还得写成markdown的格式，才算完成

## 工具
Python
要安装qiniu模块（必要）和ConfigParser模块
AutoHotkey+AutoHotkey.dll
AutoHotkey.dll是用来实现其他脚本语言对AutoHotkey的调用,请下载对应于你的AutoHotKey版本的dll文件，然后将它放到windows/System32文件夹中

##运行要求：
python环境，并且有pywin32，没有的话这里下
AutoHotKey,这个真是个神器，自己下吧
windows系统
七牛云存储账户

## 配置方法 七牛云账号
注册七牛云账号，获得自己的AK、SK、空间名称以及域名地址
新建配置文件config.ini,将它与upload_qiniu.py放在同一目录下
[qiniu]
ak     = # 填入你的AK
sk     = # 填入你的SK
url    = # 填入你的域名地址
bucket = # 填入你的空间名称
styleName = # 填入图片样式
将markdown_picture.ahk文件中python后面的地址替换成upload_qiniu.py文件的绝对地址
双击markdown_picture.ahk文件，执行该脚本
使用


## 有待完善
    QQ截图后,直接从内存上传图片base64字符,减少保存图片到系统上传文件的操作过程.

## bug
   1.上传文件会出现ctrl+v复制出来的字符不是最新图片字符. 原因上传视频是通过把字符缓存到同目录下的markdown.txt文件新出现的问题.

## 原项目地址
   https://github.com/xzonepiece/markdown-img-upload-windows
