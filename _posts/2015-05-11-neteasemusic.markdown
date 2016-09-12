---
layout:     post
title:      "网易云音乐从第三方添加歌曲"
subtitle:   "居家旅行，行走江湖必备"
date:       2016-09-11
author:     "Wcq"
header-img: "img/black_man.jpg"
tags:
    - 
    - 
---


> 据说每一个猿的指尖都隐藏着改变世界的力量  LOL

这个星期被拉到初中的一个微信群 突然就想了很多以前的事 其中就想到了  
一本正经的模仿歌词写作文然后被老师拿出来批判一番  
正打算 Download 下来的时候 尼玛竟然开始要收费了。。。   
翻一下歌单 果然一些以前下好的歌都变灰色了  

![img](/img/in-post/post-neteasemusic.jpg)

为了不被网易云音乐绑架  
也为了那三块钱软妹币巨款 在下踏上了“奋斗”之路。。。

---

### 环境
* 已越狱 ios 系统
* 网易云音乐 3.6.0
* SqLite3.x   这个工具用来修改数据库
* 有网易云音乐的帐号 能联网

### 思路
* 
破解这个软件使我们直接是 VIP 帐户 但是我只是想下载个音乐啊  
没必要为了一首歌搞这么大动静 性价比太低 而且版本升级什么的可能就不能用了  
也不能实现跨平台 对于不搞灰黑产的我的来讲  
这实在不是一条应该走的路(安全圈很鄙视灰黑产啊) 果断放弃

* 
直接绕过这个机制 从第三方网站下载好歌曲歌词 直接替换骗过播放器 显然这应该是最简单的了 下面开始记录过程


### 过程
以下内容针对开发者 普通用户可以看最后面

对面 ios 应用来说 由于沙盒机制 正常情况下每个应用都只能对它本身所拥有的文件有写权限  
也就是说这个应用如果要创建文件夹什么的只能是在它自己的Documents  Library  tmp 目录下  
像这些歌曲这些一般来说就是在 Documents 目录下了  


1、找到 网易云音乐的 Documents 目录 确认歌曲信息  

```scss
wcq-062821@bogon:~/.ssh
> sudo ssh localhost -p 3333
root@localhost's password:
```
这里我是用   usbmuxd    来转发端口来代替 wifi 连接 事实上这个协议通过 usb 模拟 TCP 协议使之可以直接用 USB 端口来传输 速度比 wifi 连接快超多   
  没有搭这个环境的可以直接  ssh root@iphone_ip   来 ssh 登陆
    
打开网易云音乐这个应用  

```scss
wcqde-iPad:~ root# ps -e | grep App  
   81 ??         0:00.71 /System/Library/CoreServices/AppleIDAuthAgent  
  218 ??         0:09.15 /System/Library/PrivateFrameworks/ApplePushService.framework/apsd  
  391 ??         0:00.07 /System/Library/PrivateFrameworks/AppSupport.framework/Support/cplogd  
  393 ??         0:00.77 /Applications/MobileCal.app/MobileCal  
  562 ??         0:05.27 /Applications/MobileMail.app/MobileMail  
  1094 ??         0:00.27 /private/var/db/stash/_.zZDbNY/Applications/MobileCal.app/PlugIns/CalendarWidget.appex/CalendarWidget  
 3071 ??         0:00.34 /System/Library/CoreServices/CacheDeleteAppContainerCaches  
 3077 ??         0:00.14 /private/var/db/stash/_.zZDbNY/Applications/MobileSafari.app/webbookmarksd  
 4857 ??         0:09.29 /var/mobile/Containers/Bundle/Application/754116CA-5A57-45DB-9441-59F9BE391A43/neteasemusic.app/neteasemusic  
 5130 ttys000    0:00.01 grep App  
```
  
用 ps -e \| grep App 容易知道neteasemusic 就是网易云音乐了  

```scss
wcqde-iPad:~ root# cycript -p neteasemusic
cy# [[NSFileManager defaultManager] URLsForDirectory:NSDocumentDirectory inDomains:NSUserDomainMask][0]
#"file:///var/mobile/Containers/Data/Application/ADD802B1-2407-4869-9FB8-0F677C617325/Documents/“  
#?exit
```

使用cycript -p neteasemusic 把 cycript 附加到neteasemusic进程 通过  

```scss
[[NSFileManager defaultManager] URLsForDirectory:NSDocumentDirectory inDomains:NSUserDomainMask][0] 
```
这个命令输出 Documents目录的路径 并 ?exit 退出Cycript  

现在进入 Documents 目录看看有什么东西  
一翻查找发现在下载下来的歌都存放在 Documents/UserData/Download/done 下面  
现在在网易云音乐上面随便下载一首歌  

在 done 目录下 ls -l 显示所有歌曲的详细信息如下：  
-rw-r--r-- 1 mobile mobile  2594944 Sep  8 01:26 192000-18668448-.mp3  
根据上面的Sep  8 01:26 就是这个文件创建的时间  我们找到时间最新的那个所对应的 mp3 文件就是你刚刚下载下来的歌了  
这个文件的第二个字段18668448是歌词的索引 要替换歌词的话还得靠它  

2、从第三方网站下站歌曲和歌词  
这个自己想办法 推荐用google 不会用就用必应 还不行就百度吧。。。  


3、替换歌曲歌词并修改数据库  

* 替换歌曲

```scss
//先在电脑上通过 scp 命令把下载下来的歌曲和歌词传到 ipad 上如下：
wcq-062821@bogon:~/Downloads
>scp Magical_Smile.mp3 root@192.168.1.123:/var/mobile/Containers/Data/Application/ADD802B1-2407-4869-9FB8-0F677C617325/Documents/UserData/Download/done/
root@192.168.1.123's password:																					'


//通过终端完成替换
//在 done 目录下 把Magical_Smile.mp3 覆盖为192000-18668448-.mp3
wcqde-iPad:/var/mobile/Containers/Data/Application/ADD802B1-2407-4869-9FB8-0F677C617325/Documents/UserData/Download/done root# mv Magical_Smile.mp3 192000-18668448-.mp3

```
* 修改数据库
//从Documents/UserData/ 目录把music_storage_v2.sqlite3 拷贝到电脑上修改  

```scss
wcq-062821@bogon:~/IOSCrack/neteasemusic
> scp root@192.168.1.123:/var/mobile/Containers/Data/Application/ADD802B1-2407-4869-9FB8-0F677C617325/Documents/UserData/music_storage_v2.sqlite3 .

//使用sqlite3 打开数据库并把我们感兴趣的表导出来到 playinglist.txt 中
//.table 查看所有的表
//.output 重定向输出
//.dump 把表导出
wcq-062821@bogon:~/IOSCrack/neteasemusic
> sqlite3 music_storage_v2.sqlite3
SQLite version 3.8.10.2 2015-05-20 18:17:19
Enter ".help" for usage hints.
sqlite> .table
djradioPlayInfo       localPrivateMsg       playlisttrack
downloadmv            localevent            recentplay
downloadprogram       myplaylistorder       recentplaycollection
downloadtrack         playinglist           specialplaylist
ipodSong              playlist              track
sqlite> .output playinglist.txt
sqlite> .dump playinglist
sqlite> .exit
```

//打开 playinglist.txt 查看发现下面内容

```scss
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE playinglist(songid integer,persistid text,collectionid integer,collectiontype integer,eq text,userid integer,json text,extrainfo text,trackorder integer,unique(userid,songid));
INSERT INTO "playinglist" VALUES(18668448,'0',107241581,2,'pop',92182393,'{"id":"18668448","clientSongType":0,"album":{"id":"1711907","info":{},"picUrl":"http://p2.music.126.net/aoTO1gl7lQYOh_79Ex8xDw==/6636652186139220.jpg","company":"","pic":"6636652186139220","language":"","publishTime":0,"onSale":false,"sales":0,"songSize":0,"name":"Let It Be Me","paid":false},"ftype":0,"clientCommentCount":0,"artists":[{"id":"35397","albumSize":0,"name":"Jason Donovan","followed":false}],"hasring":0,"v":2,"popularity":0,"clientCollectionId":"107241581","mvid":"0","clientCollection":{"id":107241581,"subscribed":false,"specialType":5,"additional":{"essence":false},"playCount":1079,"tags":[],"trackUpdateTime":1473269837347,"commentThreadId":"A_PL_0_107241581","subscribedCount":0,"songCount":77,"creator":{"profile":{"vipType":0,"nickname":"望穿墙","userId":92182393,"authStatus":0,"avatar":"http://p3.music.126.net/LdFew32T7uAldtmy4TEGHw==/1365593506486450.jpg"}},"commentCount":0,"offlineSuccCount":69,"trackNumberUpdateTime":1473269837347,"coverImgUrl":"http://p1.music.126.net/NBRRX6l69enZKDqJQdxtCw==/528865094196130.jpg","shareCount":0,"name":"望穿墙喜欢的音乐","updateTime":1473269837347},"t":0,"disc":"","duration":165000,"clientCollectionType":2,"no":7,"name":"Sealed With A Kiss","clientEqString":"pop"}','',0);
INSERT INTO "playinglist" VALUES(4386589,'0',107241581,2,'pop',92182393,'{"id":"4386589","clientSongType":0,"album":{"id":"442695","info":{},"picUrl":"http://p1.music.126.net/SbJn22gsq-Pv6WLm8PK98A==/564049465093755.jpg","company":"","pic":"564049465093755","language":"","publishTime":0,"onSale":false,"sales":0,"songSize":0,"name":"Best I Never Had","paid":false},"ftype":0,"clientCommentCount":0,"artists":[{"id":"103121","albumSize":0,"name":"The Downtown Fiction","followed":false}],"hasring":0,"v":6,"popularity":0,"clientCollectionId":"107241581","mvid":"5293276","clientCollection":{"id":107241581,"subscribed":false,"specialType":5,"additional":{"essence":false},"playCount":1079,"tags":[],"trackUpdateTime":1473269837347,"commentThreadId":"A_PL_0_107241581","subscribedCount":0,"songCount":77,"creator":{"profile":{"vipType":0,"nickname":"望穿墙","userId":92182393,"authStatus":0,"avatar":"http://p3.music.126.net/LdFew32T7uAldtmy4TEGHw==/1365593506486450.jpg"}},"commentCount":0,"offlineSuccCount":69,"trackNumberUpdateTime":1473269837347,"coverImgUrl":"http://p1.music.126.net/NBRRX6l69enZKDqJQdxtCw==/528865094196130.jpg","shareCount":0,"name":"望穿墙喜欢的音乐","updateTime":1473269837347},"t":0,"disc":"","duration":200000,"clientCollectionType":2,"no":3,"name":"I Just Wanna Run","clientEqString":"pop"}','',1);

```
其实一般来说是在这个文件中搜索歌名来定位的  
这里因为我们要找的歌一定是我们最新下载的一首歌  
所以我们要找的信息肯定在第一条  看看播放器里有哪些是你看不顺眼的先记下来  
![img](/img/in-post/post-neteasemusic1.jpg)

在playinglist.txt里搜索你看不顺眼的字眼 然后改掉它  
我就改了三个地方 并且把不需要的东西删了改完后如下：

```scss
CREATE TABLE playinglist(songid integer,persistid text,collectionid integer,collectiontype integer,eq text,userid integer,json text,extrainfo text,trackorder integer,unique(userid,songid));
INSERT INTO "playinglist" VALUES(18668448,'0',107241581,2,'pop',92182393,'{"id":"18668448","clientSongType":0,"album":{"id":"1711907","info":{},"picUrl":"http://p2.music.126.net/aoTO1gl7lQYOh_79Ex8xDw==/6636652186139220.jpg","company":"","pic":"6636652186139220","language":"","publishTime":0,"onSale":false,"sales":0,"songSize":0,"name":"-Me-","paid":false},"ftype":0,"clientCommentCount":0,"artists":[{"id":"35397","albumSize":0,"name":"183Club","followed":false}],"hasring":0,"v":2,"popularity":0,"clientCollectionId":"107241581","mvid":"0","clientCollection":{"id":107241581,"subscribed":false,"specialType":5,"additional":{"essence":false},"playCount":1079,"tags":[],"trackUpdateTime":1473269837347,"commentThreadId":"A_PL_0_107241581","subscribedCount":0,"songCount":77,"creator":{"profile":{"vipType":0,"nickname":"望穿墙","userId":92182393,"authStatus":0,"avatar":"http://p3.music.126.net/LdFew32T7uAldtmy4TEGHw==/1365593506486450.jpg"}},"commentCount":0,"offlineSuccCount":69,"trackNumberUpdateTime":1473269837347,"coverImgUrl":"http://p1.music.126.net/NBRRX6l69enZKDqJQdxtCw==/528865094196130.jpg","shareCount":0,"name":"望穿墙喜欢的音乐","updateTime":1473269837347},"t":0,"disc":"","duration":165000,"clientCollectionType":2,"no":7,"name":"魔法 Smile","clientEqString":"pop"}','',0);

```
然后我们用这里的 SQL 语句来建一个新的表  
由于不能直接在数据库里面改 我们需要先把 playinglist 这个表删了再重建如下：  

```scss
wcq-062821@bogon:~/IOSCrack/neteasemusic
> sqlite3 music_storage_v2.sqlite3
SQLite version 3.8.10.2 2015-05-20 18:17:19
Enter ".help" for usage hints.
//查看表
sqlite> .table
djradioPlayInfo       localPrivateMsg       playlisttrack
downloadmv            localevent            recentplay
downloadprogram       myplaylistorder       recentplaycollection
downloadtrack         playinglist           specialplaylist
ipodSong              playlist              track
//删表
sqlite> drop table playinglist;
sqlite> .table
djradioPlayInfo       localPrivateMsg       recentplay
downloadmv            localevent            recentplaycollection
downloadprogram       myplaylistorder       specialplaylist
downloadtrack         playlist              track
ipodSong              playlisttrack
//用playinglist.txt里的两条语句来建表
sqlite> CREATE TABLE playinglist(songid integer,persistid text,collectionid integer,collectiontype integer,eq text,userid integer,json text,extrainfo text,trackorder integer,unique(userid,songid));
sqlite> INSERT INTO "playinglist" VALUES(18668448,'0',107241581,2,'pop',92182393,'{"id":"18668448","clientSongType":0,"album":{"id":"1711907","info":{},"picUrl":"http://p2.music.126.net/aoTO1gl7lQYOh_79Ex8xDw==/6636652186139220.jpg","company":"","pic":"6636652186139220","language":"","publishTime":0,"onSale":false,"sales":0,"songSize":0,"name":"-Me-","paid":false},"ftype":0,"clientCommentCount":0,"artists":[{"id":"35397","albumSize":0,"name":"183Club","followed":false}],"hasring":0,"v":2,"popularity":0,"clientCollectionId":"107241581","mvid":"0","clientCollection":{"id":107241581,"subscribed":false,"specialType":5,"additional":{"essence":false},"playCount":1079,"tags":[],"trackUpdateTime":1473269837347,"commentThreadId":"A_PL_0_107241581","subscribedCount":0,"songCount":77,"creator":{"profile":{"vipType":0,"nickname":"望穿墙","userId":92182393,"authStatus":0,"avatar":"http://p3.music.126.net/LdFew32T7uAldtmy4TEGHw==/1365593506486450.jpg"}},"commentCount":0,"offlineSuccCount":69,"trackNumberUpdateTime":1473269837347,"coverImgUrl":"http://p1.music.126.net/NBRRX6l69enZKDqJQdxtCw==/528865094196130.jpg","shareCount":0,"name":"望穿墙喜欢的音乐","updateTime":1473269837347},"t":0,"disc":"","duration":165000,"clientCollectionType":2,"no":7,"name":"魔法 Smile","clientEqString":"pop"}','',0);
sqlite> .table
djradioPlayInfo       localPrivateMsg       playlisttrack
downloadmv            localevent            recentplay
downloadprogram       myplaylistorder       recentplaycollection
downloadtrack         playinglist           specialplaylist
ipodSong              playlist              track
//由于没有重定向输出所以结果显示在终端上
sqlite> .dump playinglist
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE playinglist(songid integer,persistid text,collectionid integer,collectiontype integer,eq text,userid integer,json text,extrainfo text,trackorder integer,unique(userid,songid));
INSERT INTO "playinglist" VALUES(18668448,'0',107241581,2,'pop',92182393,'{"id":"18668448","clientSongType":0,"album":{"id":"1711907","info":{},"picUrl":"http://p2.music.126.net/aoTO1gl7lQYOh_79Ex8xDw==/6636652186139220.jpg","company":"","pic":"6636652186139220","language":"","publishTime":0,"onSale":false,"sales":0,"songSize":0,"name":"-Me-","paid":false},"ftype":0,"clientCommentCount":0,"artists":[{"id":"35397","albumSize":0,"name":"183Club","followed":false}],"hasring":0,"v":2,"popularity":0,"clientCollectionId":"107241581","mvid":"0","clientCollection":{"id":107241581,"subscribed":false,"specialType":5,"additional":{"essence":false},"playCount":1079,"tags":[],"trackUpdateTime":1473269837347,"commentThreadId":"A_PL_0_107241581","subscribedCount":0,"songCount":77,"creator":{"profile":{"vipType":0,"nickname":"望穿墙","userId":92182393,"authStatus":0,"avatar":"http://p3.music.126.net/LdFew32T7uAldtmy4TEGHw==/1365593506486450.jpg"}},"commentCount":0,"offlineSuccCount":69,"trackNumberUpdateTime":1473269837347,"coverImgUrl":"http://p1.music.126.net/NBRRX6l69enZKDqJQdxtCw==/528865094196130.jpg","shareCount":0,"name":"望穿墙喜欢的音乐","updateTime":1473269837347},"t":0,"disc":"","duration":165000,"clientCollectionType":2,"no":7,"name":"魔法 Smile","clientEqString":"pop"}','',0);
COMMIT;
sqlite> .exit
```
至此数据库就改完了 为什么后面那些不用加了呢？  
因为这是第一首歌的信息只要第一首歌的信息存在 就说明这不是一张空表  
剩下的那些信息 app 检查到没有的时候会自动帮你从云端同步 可以不用管  
当然你闲得蛋疼也可以一条一条加 233333  
关闭网易云音乐  
把music_storage_v2.sqlite3 拷贝回  

```scss
/var/mobile/Containers/Data/Application/ADD802B1-2407-4869-9FB8-0F677C617325/Documents/UserData/music_storage_v2.sqlite3 
```
覆盖掉原来的数据库

```scss
wcq-062821@bogon:~/IOSCrack/neteasemusic
> scp music_storage_v2.sqlite3 root@192.168.1.123:/var/mobile/Containers/Data/Application/ADD802B1-2407-4869-9FB8-0F677C617325/Documents/UserData/music_storage_v2.sqlite3
```
现在重新打开网易云音乐 你会发现原来的歌看起来不见了 歌名和歌手信息都变成了你所改的  
播放的也确实是我们从第三方网站下载的歌 这个时候你点击下一首上一首按钮 会发现不好使  
这是因为playinglist 表中只有我们的第一首歌 你手动播放其他歌 然后再点上一首下一首  
这时候软件就会同步一些必要的信息到 playinglist 中到这里已经可以完成了  
如果想要改歌词的话接着往下看  

* 修改歌词文件使之和你下载的那首拿来掉包的歌词的格式一样

```scss
//把歌词文件拷贝到当前目录
wcq-062821@bogon:~/IOSCrack/neteasemusic
> scp root@192.168.1.123:/var/mobile/Containers/Data/Application/ADD802B1-2407-4869-9FB8-0F677C617325/Documents/UserData/Download/LyricsDone/18668448.lrc .
root@192.168.1.123's password:                                                                                           '
Magical_Smile.lrc                                                                          100% 1464     1.4KB/s   00:00  
```

mp3 可以直接覆盖 但是歌词不可以 因为一定要按原来你下载的那首歌的格式来写的歌词文件播放器才认 否则只要联网了一播放歌曲它就会自动从网上下载对应的歌词来覆盖掉你调包的歌词 这是一个大坑 MD   


下面开始修改歌词：
如我用来掉包的那个歌词文件的格式是这样的：

```scss
{"tlyric":{"version":3,"lyric":"[by:JoannaN]\n 中文歌词},"songId":"18668448","lrc":{"version":6,"lyric":"英文歌词"},"transUser":{"nickname":"JoannaN"}}  
```


注意：  网易云音乐的歌词只有一行 里面的\n 就是ASCII 字符换行符  
而我下载下来的歌词是这样的：  

```scss
[ti:魔法 Magical Smile]
[ar:183CLUB]
[al:王子变青蛙电视原声带]
[00:01.11]魔法 Smile Magical Smile (插曲)
[00:02.11]唱：183LCUB
[00:03.11]曲：Davor Julama/Jennifer Lee Hershman
[00:04.11]词：Davor Julama/Jennifer Lee Hershman 
[00:06.01]
[00:06.11]yeah
[00:08.39]i know how it feels
[00:11.55]when i see u smile
[00:17.16]
```

对于这个文件先备份一下 然后把不需要的删掉只留下

```scss
[00:01.11]魔法 Smile Magical Smile (插曲)
[00:02.11]唱：183LCUB
[00:03.11]曲：Davor Julama/Jennifer Lee Hershman
[00:04.11]词：Davor Julama/Jennifer Lee Hershman 
```
这种格式的真正歌词然后把用vim打开该文件   
把光标定位到第一个字符执行命令  

```scss
:%s/\n/\\n/g  
```
这条命令会把所有的换行符\n替换成普通字符\n  

由于18668448.lrc对应的原曲是英文歌 还有中文翻译 所以主歌词是英文歌词  
把这些整理后的歌词填入18668448.lrc 的英文歌词部分 中文歌词部分为空就好了  
最终结果如下:  

    {"tlyric":{"version":3,"lyric":"[by:JoannaN]\n"},"songId":"18668448","lrc":{"version":6,"lyric":"[00:01.11]魔法 Smile Magical Smile (插曲)\n[00:02.11]唱：183LCUB\n[00:03.11]曲：Davor Julama/Jennifer Lee Hershman\n[00:04.11]词：Davor Julama/Jennifer Lee Hershman\n[00:06.01]\n[00:06.11]yeah\n[00:08.39]i know how it feels\n[00:11.55]when i see u smile\n[00:17.16]\n[00:19.70]轻轻 你靠在我胸膛\n[00:27.17]Yeh\n[00:29.70]有一种奇特的力量 不能抵挡\n[00:37.79]\n[00:39.08]我开始乱了步伐 心还傻傻忘了跳\n[00:48.31]或许爱就是这样 让我甘心被你融化\n[01:43.05]或许爱就是这样 让人心甘情愿被你融掉\n[01:51.03][00:56.44]\n[02:33.10][01:51.32][00:57.12]看着你微笑 有一道光芒\n[02:37.93][01:56.15][01:01.64]打在我身上 像一种魔法\n[03:02.07][02:42.19][02:00.83][01:06.49]是你无心布下的爱情圈套\n[02:48.32][02:06.09][01:12.13]让我为了你疯狂 迷人的微笑\n[01:19.95]\n[01:21.26]Woo Baby\n[01:22.88]\n[01:23.27]轻轻 你开口说了话\n[01:32.66]像阵风吹进了心房 微微的发烫\n[01:41.89]\n[02:12.47]我像被施咒的青蛙\n[02:16.06]无法控制的就爱上她\n[02:21.88]不敢多做挣扎\n[02:26.05]难道这会是场梦吗\n[02:31.85]\n[02:57.25]打在我身上\n[02:53.99]see u smile\n[03:07.58]this feelin' is deep inside of me\n[03:13.00]i can't live my life without u\n[03:18.26]when i see u smile\n[03:22.50]when i see u smile\n[03:29.50]\n"},"transUser":{"nickname":"JoannaN"}}
    
关闭网易云音乐

```scss
//LyricsDone目录把18668448.lrc 拷贝到ipad 的/var/mobile/Containers/Data/Application/ADD802B1-2407-4869-9FB8-0F677C617325/Documents/UserData/Download/LyricsDone 目录
scp 18668448.lrc root@192.168.1.123:/var/mobile/Containers/Data/Application/ADD802B1-2407-4869-9FB8-0F677C617325/Documents/UserData/Download/LyricsDone/18668448.lrc
root@192.168.1.123's password: 
18668448.lrc                                                                         100% 1502     1.5KB/s   00:00
```
打开网易云音乐 这时候歌词也好了 哈哈
![img](/img/in-post/post-neteasemusic2.jpg)

如果你连图片也想改那也是可以的 自己弄吧  
方法都是一样的 就一个换字 理论上可行(虽然我没试过)。。。  


### 对于普通用户 以 windows 用户为例
打开电脑上的 xx 助手 这里以爱思助手为例  
点应用程序 再点网易云音乐右边的浏览 这时候出现下图  
![img](/img/in-post/post-neteasemusic3.jpg)
Documents已经出现了 上面提到的所有文件都在这个文件夹里找得到  
剩下的就是照着前面的思路一步一步修改文件再替换 如果没有装Sqlite3就装一个 Sqlite3 来改数据库了 不过这不是必须的 如果你只是想听歌的话  
你完全可以下载一首同名的歌来直接替换 这样省时省心 哈哈

### 结束
周五晚上开始准备用 github + jekyll 搭建个个人主页来写一些有趣的东西  
毛都不懂从零学起 折腾到周六晚上刚能用的时候 突然用了一下 git checkout  
当时只能用瑟瑟发抖来形容了 MDZZ  
今天中午开始写这第一篇文章 以前搞了个 360 图书馆于是就一味的转载转载  
真要动起笔来才发现做出来跟写出来 尼玛差别太大了  
这篇文章写了一天。。。。。。。。。。 不过总算写玩了  
这辛酸的第一次 一颗赛艇！  
写得不好别喷啊 (没使能评论插件你根本没得喷 哈哈!)

