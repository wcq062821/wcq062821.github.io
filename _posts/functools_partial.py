import functools
#int() 函数可以把'1221'转换成十进制数
#默认base=10 所以返回的是十进制1221   当base改为16时意思是1221是16进制 所以返回的是十进制4641
#base是针对待转换的字符串内的数值 int()永远返回十进制数
print(int('1221'))
print(int('1001', base = 2))
print(int('1221', base=16))

#如果想要base默认是2 可以这样写
def int2(x, base = 2):
    return int(x, base)

print(int2('1001'))

#利用偏函数 可以这样写
int2_2 = functools.partial(int,base = 2)
print(int2_2('1001'))

#int2_2('1001') 相当于 
# kw = {'base : 2'}
# int('1001', **kw)       即base=2

#创建偏函数其实可以传三个参数 函数对象、*args 和 **kw 这3个参数
max2 = functools.partial(max, 10)
print(max2(1,5,7))
#以上max2返回的结果会是10  因为 10已经被当成 *args的一部分自动加到了 max2的形参中的第一个元素那里
#也就是说 max2(1,2,3) 相当于 args = (10,1,2,3)    max(*args)
