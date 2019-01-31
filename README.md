[TOC]

# Execptions

## #0 GitHub

```

```

## #1 环境

```
Python3.6
Django==2.0.7
djangorestframework==3.8.2
```

## #2 需求分析
- django REST Framework中的系统异常抛出的信息是detail:"xxxx",需要把detail改成统一的"msg"
- 系统抛出的异常,改成我们想要的格式


## #3 开始

### #3.1 新建一个django项目
### #3.2 把"detail"改成"msg"

```
{
    "detail": "Method \"PUT\" not allowed."
}
```
改成

```
{
    "msg": "Method \"PUT\" not allowed."
}
```

新建文件(这里命名为execption.py,名字随意)

execption.py
```
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework import status

def custom_exception_handler(exc,context):
    response = exception_handler(exc,context) #获取本来应该返回的exception的response
    if response is not None:
        try:
            response.data["msg"] = response.data['detail'] #改这里
            del response.data['detail']
        except:pass
    return response


```

settings.py

```
REST_FRAMEWORK = {
    ...
    'EXCEPTION_HANDLER': 'app.execption.custom_exception_handler', # 指定刚刚新建的execption.py文件 
}
```

### #3.3 序列化抛出的异常改成自己的格式

系统异常

```
{
    "name": [
        "This field is required."
    ],
    "age": [
        "This field is required."
    ]
}
```

改后


```
{
    "code": "422",
    "message": "Validation Failed",
    "errors": [
        {
            "field": "name",
            "message": "This field is required."
        },
        {
            "field": "age",
            "message": "This field is required."
        }
    ]
}
```






