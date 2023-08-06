import re
   

def retrieve(dict_, keys):
    """字典解构赋值
    params = {'a': 1, 'b': 2}
    a, b = get(params, ['a', 'b'])
    a, c = get(params, ['a', 'c'])
    """
    tmp = ()
    for key in keys:
        tmp += (dict_.get(key),)
    return tmp


def access(obj, attrs):
    """对象解构赋值"""
    tmp = ()
    for attr in attrs:
        tmp += (getattr(obj, attr),)
    return tmp


def map_dict(dict_, map_):
    """字典键值替换
    { 'test': 'test1' }
    """
    tmp = {}
    for k, v in map_.items():
        tmp[v] = dict_[k]
    return tmp

def lowcase(text):
    """驼峰转下划线
    lowcase('sayHello')
    """
    ls = list(set(re.findall('[a-z][A-Z]', text)))
    ll = [x[0] + '_' + chr(ord(x[1]) + 32) for x in ls]
    for x, y in zip(ls, ll):
        text = text.replace(x, y)
    return text


def camel(text):
    """下划线转驼峰"""
    if isinstance(text, str):
        if '_' in text:
            first, *others = text.split('_')
            return ''.join([first.lower(), *map(str.title, others)])
        else:
            return text
    else:
        return text


def dict_snake2camel(dict_):
    return {camel(x): dict_[x] for x in dict_}


def iter_dic(dic, fun):
    """遍历转化字典键"""
    rt_dic = {}
    for key, value in dic.items():
        if isinstance(value, dict):
            rt_dic[fun(key)] = iter_dic(value, fun)
        elif isinstance(value, list):
            rt_dic[fun(key)] = iter_lis(value, fun)
        else:
            rt_dic[fun(key)] = value
    return rt_dic


def iter_dic_value(dic, func):
    """遍历转化字典值"""
    rt_dic = {}
    for key, value in dic.items():
        if isinstance(value, dict):
            rt_dic[key] = iter_dic_value(value, func)
        elif isinstance(value, list):
            rt_dic[key] = iter_lis_value(value, func)
        else:
            rt_dic[key] = func(value)
    return rt_dic


def iter_lis(lis, func):
    """遍历转化列表值(字典按键处理)"""
    rt_lis = []
    for value in lis:
        if isinstance(value, dict):
            rt_lis.append(iter_dic(value, func))
        elif isinstance(value, list):
            rt_lis.append(iter_lis(value, func))
        else:
            rt_lis.append(value)
    return rt_lis


def iter_lis_value(lis, func):
    """遍历转化列表值(字典按值处理)"""
    rt_lis = []
    for value in lis:
        if isinstance(value, dict):
            rt_lis.append(iter_dic_value(value, func))
        elif isinstance(value, list):
            rt_lis.append(iter_lis_value(value, func))
        else:
            rt_lis.append(value)
    return rt_lis


def to_lowcase(dic):
    return {lowcase(k): dic.get(k) for k in dic}


def iter_lowcase(dic):
    return iter_dic(dic, lowcase)


def to_camel(dic):
    return {camel(k): dic.get(k) for k in dic}


def iter_camel(dic):
    return iter_dic(dic, camel)


def iter_slashize(dic): 
    """文字空值转斜杆"""
    slashize = lambda x: '/' if x == None else x
    return iter_dic_value(dic, slashize)

