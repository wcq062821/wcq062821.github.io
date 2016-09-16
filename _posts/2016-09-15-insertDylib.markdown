---
layout:     post
title:      "IOS 动态库注入攻击"
subtitle:   "最简单的 HelloWorld程序演示"
date:       2016-09-15
author:     "Wcq"
header-img: "img/in-post/post-insertDylib.jpg"
tags:
    - 
    - 
---


> 据说每一个猿的指尖都隐藏着改变世界的力量  LOL


### 环境
* Xcode Version 7.3.1(7D1014)
* SDK : iPhoneOS9.3
* 越狱  IOS 8.2

### 背景知识
下面是 HelloWorld.m 的源码：

```scss
#import <Foundation/Foundation.h>

@interface SaySomething : NSObject
- (void) say: (NSString *) phrase;
@end

@implementation SaySomething

- (void) say: (NSString *) phrase {
    printf("%s\n", [ phrase UTF8String ]);
}

@end

int main(void)
{
    SaySomething *saySomething  = [[SaySomething alloc] init];
    [saySomething say: @"Wcq Hello World!"];
    [saySomething release ];
    return 0;
}
```
main 函数里面可以用 C 来实现 如下：

```scss
objc_msgSend(
    objc_msgSend(
             objc_msgSend(
                 objc_msgSend(
                          objc_getClass("SaySomething"), NSSelectorFromString(@"alloc")),
                          NSSelectorFromString(@"init")),
                 NSSelectorFromString(@"say:"), @"wcq Hello World"),
             NSSelectorFromString(@"release:"));

```
objc_msgSend 的原型如下：  
id objc_msgSend(id self, SEL op, ...)  

self(接收方) 是一个消息发送给类的实例的指针， op(选择器) 是类中用于处理消息的方法  
id 可以表示任意类型 关于它的详细介绍你可以在 /usr/include/objc/objc.h中找到  
这里 objc_msgSend 返回的 id 就是上层 objc_msgSend 的第一个参数 self  

例如OC 里的 [SaySomething alloc] 与 C 里的  
objc_msgSend( objc_getClass("SaySomething"), NSSelectorFromString(@"alloc")) 等价  
OC 里通过类的实例调用方法的底层都是objc_msgSend(self, op, ...);  
类方法的定义如下：  

```scss
struct objc_method {  
	SEL method_name;  
	char *method_types;  
	IMP method_imp;  
};  
```
method_name 是选择器即根据不同的名来调用不同的方法  
method_types 包含接受的参数类型字符串  
___method_imp___ 是一个指针 指向内存中方法的实际地址  
因此我们要注入自己的代码的话只要把 method_imp 改成我们自己的代码的地址就可以了  


### 实现
新建一个 helloworld.m  内容如下：
```scss
#import <Foundation/Foundation.h>


@interface SaySomething : NSObject
- (void) say: (NSString *) phrase;
@end

@implementation SaySomething

- (void) say: (NSString *) phrase {
    printf("%s\n", [ phrase UTF8String ]);
}

@end

int main(void)
{
    SaySomething *saySomething  = [[SaySomething alloc] init];
    [saySomething say: @"Wcq Hello World!"];
    [saySomething release ];
    return 0;
}
```
再建一个injection.c 这是我们用来注入的代码 内容如下：  

```scss
#include <stdio.h>
#include <objc/objc.h>

id evil_say(id self, SEL op)
{
	printf("WcqIOS ! Hello World!\n");
	return self;
}

static void __attribute__((constructor)) initialize(void)
{
	class_replaceMethod(objc_getClass("SaySomething"), \
						sel_registerName("say:"), \
						evil_say, \
						"@:");
}
```
新建一个 Makefile 内容如下：  

```scss
all: injection.o
	clang -o hello helloworld.m -arch armv7 -isysroot \
		/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk \
		-framework Foundation -lobjc
	ld -dylib -lsystem -lobjc -o injection.dylib injection.o -syslibroot \
		/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk

injection.o : injection.c
	clang -c -o injection.o injection.c -arch armv7 -isysroot \
		/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk -fPIC

clean:
	rm hello 
	rm *.o
	rm injection.dylib
```
注意 clang 前是一个 Tab 否则可能会有问题  
如果你的 SDK 不是 ios9.3 路径可能会有点差异 自己找到改过来即可  
执行 make 之后生成 hello injection.dylib  
要清除编译的目标文件可以执行 make clean  

##### 用 ldid签名之后拷贝到 ios 设备中运行 如下：  
如果没有装 ldid 的可以点这[ldid](http://joedj.net/ldid)下载 把 ldid 放到当前目录运行  

```scss
./ldid -S hello  
./ldid -S injection.dylib  
```
即可给 hello 和 injection.dylib 签名   
拷贝到 ios 设备的 /var/mobile/Downloads 下做实验  

```scss
scp ./hello root@192.168.1.123:/var/mobile/Downloads/  
scp ./injection.dylib root@192.168.1.123:/var/mobile/Downloads/  
```

ssh 登录 ios 设备并执行程序：  

```scss
ssh root@192.168.1.123
root@192.168.1.123's password:
wcqde-iPad:~ root# cd /var/mobile/Downloads/
wcqde-iPad:/var/mobile/Downloads root# export DYLD_INSERT_LIBRARIES="./injection.dylib"
wcqde-iPad:/var/mobile/Downloads root# ./hello
WcqIOS ! Hello World!
```
我们通过export DYLD_INSERT_LIBRARIES="./injection.dylib"  
DYLD_INSERT_LIBRARIES它 是一个使用冒号分隔的动态库路径字符串，表示一个将要加载运行的动态库额外依赖的其它动态库。通过这个环境变量，我们就可以向应用中注入自己的动态库，进而改变应用运行时的特定行为。而这种方式，也正是mobileSubstrate所使用的最基本方法。  

这样在运行 hello 的程序的时候就会先加载injection.dylib   
这个库的初始化函数里就调用了 class_replaceMethod 来替换掉 hello 里面的 say 方法  
所以hello最终执行的是evil_say方法打印出了 WcqIOS ! Hello World!  

### 结束
如果目标是一个 ipa 的话就要用 yololib 可在这里[https://github.com/KJCracks/yololib](https://github.com/KJCracks/yololib)下载  
然后用 Xcode 打开它的那个工程  

![img](/img/in-post/post-insertDylib1.jpg)

把 target改成你现在的 MAC的 OS X的版本 点击调试按钮会自动编译并运行  
鼠标移到 yololib 下右键在 Finder 中显示然后拷贝出来就可以用 yololib 命令了  
用这个可以实现地一个 ipa 里面的 binary 进行插入动态库 最后重新打包 签名就可以运行了
