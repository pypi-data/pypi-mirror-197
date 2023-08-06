def distrib(list_, method):
	"""按元素指定属性进行归并
    rst = distrib(a, lambda x:x['location'])
    for k, v in rst:
	    print(k, v)
    """
	tmp = {}
	for item in list_:
		key = method(item)
		if key in tmp:
			tmp[key].append(item)
		else:
			tmp[key] = [item]
	for k, v in tmp.items():
		yield k, v
  
  
def organize(list_, method):
    """按元素指定属性进行分块组合
    """
    tmp = []
    for k, v in distrib(list_, method):
        tmp += v
    return tmp


def unique(list_, method):
    """按元素指定属性去重"""
    keys = []
    items = []
    for item in list_:
        key = method(item)
        if key in keys:
            continue
        else:
            keys.append(key)
            items.append(item)
    return items
