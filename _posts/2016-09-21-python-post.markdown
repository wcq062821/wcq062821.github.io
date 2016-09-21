---
layout:     post
title:      "POST提交表单塞爆钓鱼网站"
subtitle:   "只适用于弱智的钓鱼网站"
date:       2016-09-21
author:     "Wcq"
header-img: "img/in-post/post-python-post.jpg"
tags:
    - 
    - 
---


> 据说每一个猿的指尖都隐藏着改变世界的力量  LOL


### 环境
* Python 2.7.10
* curl 7.43.0 (x86_64-apple-darwin15.0) libcurl/7.43.0 SecureTransport zlib/1.2.5
Protocols: dict file ftp ftps gopher http https imap imaps ldap ldaps pop3 pop3s rtsp smb smbs smtp smtps telnet tftp
Features: AsynchDNS IPv6 Largefile GSS-API Kerberos SPNEGO NTLM NTLM_WB SSL libz UnixSockets

### 背景
现在的诈骗信息是越来越多了 信息安全意识稍差的人极有可能中招  
今天群里一哥们公司的老总就被[http://www.lcoud.cn.com/](http://www.lcoud.cn.com/)这个钓鱼网站钓了。。。  
为此群里大牛们决定写脚本去塞爆这个钓鱼网站(其实是无聊 找点乐子 hhhhh)
受巨神们聊天的启发 整理了一下稍加改进就有了这篇随笔

### 思路
利用 curl 获得钓鱼网站登陆界面的代码 找出关键部分(文本输入框及提交按钮)  
写一个python脚本  在 while 1 里利用 post 方式提交伪造的用户名和密码  


### 实现
1、利用 curl 获得钓鱼网站登陆界面的代码并存到 source.txt 文件中  

```scss
wcq-062821@wcqdeMacBook-Pro:~/IOSCrack/tmp
> curl http://www.lcoud.cn.com/ > source.txt
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  9623  100  9623    0     0   7336      0  0:00:01  0:00:01 --:--:--  7334
```
查看 source.txt 搜索 action得到关键代码如下：  

```scss
    <div class="main">

        <form name="form" action="/Login" method="post" target="_top">
            <div class="top"><em><img src="./index_files/yun.png" height="25"></em><span><a href="index.htm#" class="shuom"></a><a href="http://www.apple.com/cn/icloud/setup/" target="blank"><img src="./index_files/wenh.png"></a></span></div>
            <div class="login_main">
                <div class="login">
                    <div class="del">

                        <ul>
                            <li><input type="text" id="accountname" name="username" value="" errormsg="Apple ID" placeholder="Apple ID" class="l_text" autocomplete="off" style="margin-left:10px; background:none; font-family:Arial, Helvetica, sans-serif"></li>

                            <li>
                                <input type="password" id="accountpassword" name="password" value="" errormsg="Apple 密码" placeholder="Apple 密码" class="l_text" autocomplete="off" style="margin-left:10px; background:none">






                                <input class="btn" src="./index_files/btn.png" type="image" style="margin-right:10px; margin-top:6px" onClick="this.form.action='login.do';this.form.submit()">

```
对应的界面如下：  

![img](/img/in-post/post-python-post1.jpg)

由此可知 这个页面的数据是要提交到 http://www.lcoud.cn.com/Login 这个页面处理  
Apple ID 输入文本框的名字是 username ， Apple 密码 输入文本框的名字是password  
提交按钮即那个向右的箭头执行的动作是 login.do 好了 有了这些信息 我们就可以写脚本来自动提交这些东西了  

2、写 Python 脚本
新建一个 post.py 脚本文件 填入下面内容

```scss
import urllib2
import urllib
import random
import string
def upper_generator(size=random.randint(1,2), chars=string.ascii_uppercase): return ''.join(random.choice(chars) for _ in range(size))
def lower_generator(size=random.randint(1,2), chars=string.ascii_lowercase): return ''.join(random.choice(chars) for _ in range(size))
def digits_generator(size=random.randint(7,10), chars=string.digits): return ''.join(random.choice(chars) for _ in range(size))
def maildigits_generator(size=random.randint(3,5), chars=string.digits): return ''.join(random.choice(chars) for _ in range(size))

while 1:
    #dat = random.randint(100000000,9999999999)
    #int to string
    #tem = '%d' %dat    
    dat = upper_generator()
    dat1 = lower_generator()
    dat2 = maildigits_generator()
    tem = [dat,dat1,dat2]
    tem = ''.join(tem)
    mail_list = ['@163.com','@126.com','@qq.com','@hotmail.com','@gmail.com','@yahoo.com','@msn.com','@sina.com','@sohu.com','@hongkong.com','@wcq.com']
    usern = [tem,mail_list[random.randint(0,10)]]
    mail = "".join(usern)
    print mail

    upper = upper_generator()
    lower = lower_generator()
    digits = digits_generator()
    passwd = [upper,lower,digits]
    passwd = ''.join(passwd)
    print passwd
    
    data = {'username' : mail, 'password' : passwd}
    f = urllib2.urlopen(
                    url     = 'http://www.lcoud.cn.com/login.do',
                            data    = urllib.urlencode(data)
                                    )
    #print(f.read())
```
这个脚本伪造了各种邮箱做为 Apple ID 和 首字母大写后接小写字母最后接数字作为密码填入文本框  
然后打开http://www.lcoud.cn.com/login.do 这个 url 就是相当于按下提交按键(右箭头)  
由于这里写成了死循环 只要执行这个程序不关闭 它就会一直伪造提交  

3、实验  

```scss
wcq-062821@bogon:~/IOSCrack/tmp
> python post.py
Ukb80474@gmail.com
Ulc4720709
Qoe42012@hongkong.com
Xlr3656909
Fri15942@qq.com
Xmw0606662
Mxq00155@hotmail.com
Qvw2920952
Zmw76757@sohu.com
Oql2026629
Pjg16223@sina.com
Rkk9558398
Vje95418@hotmail.com
Amr6831312
Jqx26086@hongkong.com
Typ0289151
Jev95873@msn.com
Skv8212235
Nvu71617@sina.com
Vuh3587969
Wxl07924@126.com
Rzn8374092
```
去掉#print(f.read())这一行的#还可以看到提交后的页面的代码详情  
注意这里print(f.read())的缩进一定要比while大一个TAB 否则就不在死循环里得不到执行  



### 总结
这是一个十分弱智的钓鱼网站 页面仿得十分粗糙 域名也一点都不像在浏览器上连 http://都没有  
而且即使什么都不填 直接点右箭头 一样可以进入下一个界面。。。。。  
而且连保持我的登陆状态前面的框都勾不上。。。 好弱智啊！！！  
当然我们这种python post 的方式也比较弱智 效率不高 据说可以用 curl 或 lua 来实现类似功能  
有兴趣的可以试一下  
为了提升效率 我们还可以这样 运行的时候用 python post.py& 来后台运行  
多开几个就快了 比如我开了 4 个。。。  

![img](/img/in-post/post-python-post3.jpg)

下次还看到弱智钓鱼网站 无聊的话就可以用这种方法在电脑后台挂着 我相信我也坚信 挂着挂着 钓鱼网站就会变成这样  

![img](/img/in-post/post-python-post2.jpg)

2333



