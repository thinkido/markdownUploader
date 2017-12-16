;将图片上传至七牛云，并获得图片地址 快捷键 ctrl+alt + C
^!c::
send, ^c
clipwait
;Run %comspec%  /c "Python %cd%upload_qiniu.py %Clipboard%" /p
fname=%Clipboard%
Run %comspec%  /c "Python F:\tools\text\upload_qiniu.py %fname%" /p
Sleep,1000
FileRead,content,F:\tools\text\markdown.txt
clipboard=%content%
return