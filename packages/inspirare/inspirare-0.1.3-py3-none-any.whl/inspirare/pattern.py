import re 

 # regexp = r'page=([0-9]*)&'
 #        pgn = int(re.findall(regexp,cur_page)[0])
 #        nxt_page = re.sub(regexp,'page=%d&'%(pgn+1),cur_page)
 #        browser.get(nxt_page)

        
def match(pattern, string):
	'''匹配模式
	match(r'[0-9]*abc','1abcd')    //True
	'''
	return True if re.search(pattern,string) else False

def extract(pattern, string):
	'''根据模式提取文本
	extract('job/(.*).html','job/michael.html')    //michael
	'''
	return re.search(pattern, string).group(1)

def split(pattern, string):
	'''根据模式分割文本
	split('[0-5]{2}','116622773388')    //['', '66', '77', '88']
	'''
	return re.split(pattern, string)


# import re 


# test_string = 'asjdhjabcsdhabc'
# pattern = re.compile(r'abc')
# matches = pattern.finditer(test_string)
# for match in matches:
# 	print(match.group())
# exit()
# test_string = 'asjdhjabcsdhabc'
# pattern = re.compile(r'abc')
# matches = pattern.search(test_string)
# print(matches)
# exit()

# test_string = 'asjdhjabcsdhabc'
# pattern = re.compile(r'abc')
# matches = pattern.match(test_string)
# print(matches)
# exit()
# test_string = 'asjdhjabcsdhabc'
# pattern = re.compile(r'abc')
# matches = pattern.findall(test_string)
# for match in matches:
# 	print(match)

# # abc
# # abc
# exit()
# test_string = 'asjdhjabcsdhabc'
# pattern = re.compile(r'abc')
# matches = pattern.finditer(test_string)
# for match in matches:
# 	print(match)





