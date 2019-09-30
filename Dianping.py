>>> def index(num):
	# get your target urls by inputting a specific address or the name of the mall into the searching box of Dianping
	urls=['http://www.dianping.com/search/keyword/8/0_%E4%BD%B3%E7%81%B5%E8%B7%AF7%E5%8F%B7%E7%BA%A2%E7%89%8C%E6%A5%BC%E5%B9%BF%E5%9C%BA/p{}'.format(x) for x in range(1,int(num)+1)]
	headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Cookie': '_lxsdk_cuid=16b9d4635cdc8-05fa639d710291-37627e02-fa000-16b9d4635cec8; _lxsdk=16b9d4635cdc8-05fa639d710291-37627e02-fa000-16b9d4635cec8; _hc.v=475230f3-10b7-a156-972c-b99e4f9d538c.1561711753; cy=8; cye=chengdu; s_ViewType=10; cityid=1; default_ab=shop%3AA%3A5; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1567496760; Hm_lpvt_dbeeb675516927da776beeb1d9802bd4=1567496760; wed_user_path=33775|0; aburl=1; _lxsdk_s=16cf60e718a-6f1-23f-b5a%7C%7C369', 'Host': 'www.dianping.com', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
	# create three dataframes for three different kinds of information we need
	df1 = pd.DataFrame()
	df2 = pd.DataFrame()
	df3 = pd.DataFrame()
	for url in urls:
		response = requests.get(url=url, headers=headers)
		ls=response.text
		soup=BeautifulSoup(ls,'lxml')
		title=soup.select('div[class="shop-list J_shop-list shop-all-list"] ul li div[class="tag-addr"] span[class="addr"]')
		titles=[]
		for t in title:
			titles.append(t.get_text())
		for x in range(0,len(titles)):
			pp=list(titles[x])
			address = [number_dict1.get(k) if k in number_dict1.keys() else k for k in pp]
			addr = ["".join(address)]
			dfb = pd.DataFrame([addr]).T
			dfb.columns = ["地址"]
			df2 = df2.append(dfb, ignore_index=True)
		mc=soup.select('div[class="shop-list J_shop-list shop-all-list"] ul li div[class="tit"] a h4')
		mcs=[]
		for m in mc:
			mcs.append(m.get_text())
		dfa = pd.DataFrame([mcs]).T
		dfa.columns = ["名称"]
		df1 = df1.append(dfa, ignore_index=True)
		with open("b.html", "w", encoding="utf-8") as f:
			 f.write(response.text)
		html= etree.HTML(response.text)
		with open("b.html", "r", encoding="utf-8") as f:
			a = f.read()
		html = etree.HTML(a)
		ul = html.xpath("//div[@id='shop-all-list']/ul")[0]
		ul_li = html.xpath("//div[@id='shop-all-list']/ul/li")
		number = len(ul_li)
		for i in range(1, number + 1):
			people_money = ul.xpath("//ul/li[{}]/div[@class='txt']/div[@class='comment']/a[@class='mean-price']/b//text()".format(i))
			people_money = [number_dict.get(j) if j in number_dict.keys() else j for j in people_money]
			people_money = ["".join(people_money)]
			dfc = pd.DataFrame([people_money]).T
			dfc.columns = ["人均消费"]
			df3 = df3.append(dfc, ignore_index=True)
	df = df1.join(df2,how='outer')
	df = df.join(df3,how='outer')
	df.to_excel("****".xlsx)
	return df

>>> if __name__ == '__main__':
	'''
	 Because of the lack of skills, the following instructions are all the things writer can figure out to successfully
	 crawl the price and address data 
	 Since the converting codes for Dianping are all the same in 24 hours, you can get the codes url by digging into the
	 original web page and then searching for the urf url
	 After getting the urf url, you can download the .woff document for price and address from that page
	 Upload these two documents at 'http://fontstore.baidu.com/static/editor/' an after that you can get the relationship between
	 the codes and the character
	'''
	number_dict = {'\uf318': '0', '\ued3d':'1','\uf6ac': '2', '\ue257': '3', '\uef35': '4', '\uf15d': '5', '\ue888': '6', '\ue98b': '7', '\uefa7': '8', '\ue364': '9'}
	number_dict1 = {'\ued92': '0', '\ued88':'1','\uf25d': '2', '\ue8e3': '3', '\ue155': '4', '\uf391': '5', '\ueaf8': '6', '\uea2b': '7', '\ue529': '8', '\uf516': '9','\uf130': '一', '\ue9ed':'二','\ue211': '三', '\uf1c4': '四', '\uf68e': '五','\ued00': '六', '\uea10':'七','\ue9e6': '八', '\ue1ae': '九', '\ue373': '十', '\ued29': '楼', '\ue362': '层', '\ue361': '号'}
	df=index(17)
