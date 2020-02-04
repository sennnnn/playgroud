# 文本处理入门

## 预处理

之前从没有尝试过对于文本处理相关的深度学习，一直都在图像领域和 cnn 里面打转，文本处理入门首先是要知道其预处理方法。  
读入文本，然后对文本中的词进行统计，然后将所有的词按出现频率排序之后做成词表，即词到数字的映射表，而后保存起来，然后  
将每首古诗都做成一串数字，预处理就结束了，自然语言处理好像有点意思。  

## 模型

### self 关键字理解

``` python
# 关于 self 关键字的使用。
# 首先明确一点，self 并不是一个关键字，只是大家都喜欢这样用而已。
class a:
    def pr_class(a):
        # 类方法
        print(a)

    def pr_object(self,a):
        # 实例方法
        print(a)

    def pr_object_(this,a):
        print(a)

a.pr_class(1)
a().pr_object(1)
a().pr_object_(1)
```

### 装饰器理解以及 functools 模块

代码中用到了装饰器，之前一直对装饰器一直半解，现在写个例子来看看自己是否理解

``` python
# 讨厌的装饰器，看来是不得不用了。
# 举个简单的装饰器的例子：
def trace(func):
    print("hi!")
    print("done!")
    return func

@trace
def show():
    print("show something!")

def show_():
    print("show something!")

show_ = trace(show_)
show()
show_()

# 运行上面的例子可以看出实际上，@trace 其实就是执行了一次 func = trace(func)
# 而更复杂的装饰器，例如要包装带参数的函数，或者装饰器本身就带有参数，就是另外一种形式了：(当然一般装饰器都是这样用的)
def trace(func):
    print("hi!")
    def _call(*args, **kwargs):
        print("function is wraped!")
        ret = func(*args, **kwargs)
        print("wrapping done !")
        return ret
    return _call

def trace_(log_level):
    print("second hi!")
    def _call(func):
        print('[{}]: warped function :{}'.format(log_level, func.__name__))
        return func
    return _call


@trace_('DEBUG')
@trace
def add(a,b,quiet=False):
    sum = a+b
    if(not quiet):
        print("a + b is {}".format(sum))
    return sum

def add_(a,b,quiet=False):
    sum = a+b
    if(not quiet):
        print("a + b is {}".format(sum))
    return sum

temp = trace_('DEBUG')
add_ = temp(trace(add_))

add_(1,2)
add(1,2)

# 之后是终于进入正题 functools.wraps 到底有什么用
def partial(func,*args,**kwargs):
    def _call(*fargs,**fkwargs):
        newkeywords = fkwargs.copy()
        newkeywords.update(kwargs)
        return func(*args,*fargs,**newkeywords)
    return _call

WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__qualname__', '__doc__',
                       '__annotations__')
WRAPPER_UPDATES = ('__dict__',)
def update_wrapper(wrapper,
                   wrapped,
                   assigned = WRAPPER_ASSIGNMENTS,
                   updated = WRAPPER_UPDATES):
    """Update a wrapper function to look like the wrapped function

       wrapper is the function to be updated
       wrapped is the original function
       assigned is a tuple naming the attributes assigned directly
       from the wrapped function to the wrapper function (defaults to
       functools.WRAPPER_ASSIGNMENTS)
       updated is a tuple naming the attributes of the wrapper that
       are updated with the corresponding attribute from the wrapped
       function (defaults to functools.WRAPPER_UPDATES)
    """
    for attr in assigned:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            pass
        else:
            setattr(wrapper, attr, value)
    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
    # Issue #17482: set __wrapped__ last so we don't inadvertently copy it
    # from the wrapped function when updating __dict__
    wrapper.__wrapped__ = wrapped
    # Return the wrapper so this can be used as a decorator via partial()
    return wrapper

def wraps(wrapped,
          assigned = WRAPPER_ASSIGNMENTS,
          updated = WRAPPER_UPDATES):
    """Decorator factory to apply update_wrapper() to a wrapper function

       Returns a decorator that invokes update_wrapper() with the decorated
       function as the wrapper argument and the arguments to wraps() as the
       remaining arguments. Default arguments are as for update_wrapper().
       This is a convenience function to simplify applying partial() to
       update_wrapper().
    """
    return partial(update_wrapper, wrapped=wrapped,
                   assigned=assigned, updated=updated)

# 下面来举例子喽。
def wrapper(func):
    @wraps(func)
    def _call(*args,**kwargs):
        print("wrapped!")
        ret = func(*args,**kwargs)
        print("done!")
        return ret
    return _call

@wrapper
def add(a,b):
    return a+b


# 下面来解析一个带有 wraps 的装饰器到底是干了啥。
# 首先创建一个镜像函数。
def wrapper_(func):
    def _call(*args,**kwargs):
        print("wrapped!")
        ret = func(*args,**kwargs)
        print("done!")
        return ret
    return _call

def add_(a,b):
    return a+b

# @wrapper 之后 func 被传入包装函数中，而后定义 _call 闭包函数的时候又触发了 wraps 包装函数，此时执行
# 将执行 wraps(func) 来得到一个装饰器函数，func 被传入 wraps 之后又被传入 partial 偏函数之中，最后 wraps
# 返回一个能够将原有函数的一些属性赋值给闭包函数的装饰器。
add_.args = (1,2)
print(dir(add_))
up_wrapper = wraps(add_)
add_ = wrapper_(add_)
add_ = up_wrapper(add_)
print(dir(add_))
print(dir(add_.__wrapped__))
```

### 装饰器理解第二弹✌，@property 👊冲!!!

``` python
# 好吧，恶心的装饰器第二弹👊冲!!!
# 首先把 property 的实现摆出来就基本懂了。

class Property:
    def __init__(self,fget=None,fset=None,fdel=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        
    def __get__(self,instance,cls):
        if self.fget is not None:
            return self.fget(instance)
        
    def __set__(self,instance,value):
        if self.fset is not None:
            self.fset(instance,value)
            
    def __delete__(self,instance):
        if self.fdel is not None:
            self.fdel(instance)
            
    def getter(self,fn):
        self.fget = fn
        
    def setter(self,fn):
        self.fset = fn
        
    def deler(self,fn):
        self.fdel = fn

class a:
    def __init__(self,score):
        # 此时 _score 为类中的一个保护变量，则不能被 .score 直接访问，前加 __ 则为私有变量会被偷偷改名字
        self._score = score

    # 装饰后的方法被变成属性来使用
    @property
    def score(self):
        return self._score

    # 给被装饰成属性的方法添加写属性，如果不加这个的话那么就只有读属性了。
    @score.setter
    def get_score(self,x):
        self._score = x

    @score.deleter
    def del_score(self,x):
        del self._score

A = a(20)
print(A.score)
A.score = 50
print(A.score)
del A.score
print(dir(A))
print(A.score)
```