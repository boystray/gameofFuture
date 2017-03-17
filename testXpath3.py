# -*- coding:utf-8 -*
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from lxml import etree  
from array import array


def getEastMoney(eastMoneyURL):

    
    driver = webdriver.Firefox()  
    driver.get(eastMoneyURL)  

    try:
        #等待数据结果出现
        element = WebDriverWait(driver, 200).until(
            EC.presence_of_all_elements_located((By.XPATH, r"//ul[@id='ulCjl']/li"))
        )
        #返回整个页面
        webElement = driver.find_element_by_xpath("/html")
        #print(webElement.get_attribute("outerHTML"));
        return webElement.get_attribute("outerHTML")
        #elem = driver.find_element_by_xpath(r'//*[@id="q-ra-171"]/div[1]')
        #elem = driver.find_element_by_class_name("js-room-title")
            
        #print(elem.text.replace("\n", " "))
        #f.write(str(d1)+" ")          
        #f.write(elem.text.replace("\n", " "))
        #f.write("\n")
    except : 
        print("timeout") 

    finally:
        driver.close()
        driver.quit()

        #print "end"


"""
东方财富网期货的成交/多头/空头数据，可以通过网页进行分析
<ul id="ulCjl">

<li id="80071840_1" style="background-color: rgb(255, 255, 255);">
<span class="IFe1"><span class="V2Top3">1</span></span>
<span class="IFe2"><a href="http://data.eastmoney.com/futures/sh/position.html?date=2017-03-15&amp;me=80071840" target="_blank">海通期货</span>
<span class="IFe3">372304</span>
<span class="IFe4"><span class="red">58770</span></span>
</li>


<li><span class="IFe5">本日合计</span>
<span class="IFe3">1809877</span>
<span class="IFe4"><span class="red">232260</span></span>
</li>

<li><span class="IFe5">上日合计</span>
<span class="IFe3">1606942</span>
<span class="IFe4">&nbsp;</span></li>

<li><span class="IFe5">总量增减</span>
<span class="IFe3"><span class="red">202935</span></span>
<span class="IFe4">&nbsp;</span></li></ul>

</ul>
"""
#查找列表信息:分为两个部分，期货公司列表，统计汇总信息。其中统计汇总信息格式不规范，需要判断是否有子节点
def tryFindChild(element):

    children = element.getchildren()
    if len(children):
        #return  children[0].getchildren()[0].text,children[1].text,children[2].text
        if len(children) == 3:
            #汇总信息
            children1 = children[1].getchildren()
            children2 = children[2].getchildren()
            
            if len(children1):
                return  children[0].text.strip(),children[1].getchildren()[0].text.strip(),children[2].text.strip()            
            elif len(children2):
                return  children[0].text.strip(),children[1].text.strip(),children[2].getchildren()[0].text.strip() 
            else :
                return  children[0].text.strip(),children[1].text.strip(),children[2].text.strip()
                                
        elif     len(children) == 4:
            #期货公司列表信息
            #print children[1].getchildren()[0].text
            
            #为了处理这样的...
            #<li><span class="IFe1">...</span><span class="IFe2">...</span><span class="IFe3">...</span><span class="IFe4">...</span></li>
            if len(children[0].getchildren()):
                return  children[0].getchildren()[0].text.strip(),children[1].getchildren()[0].text.strip(),children[2].text.strip(),children[3].getchildren()[0].text.strip()
            
        return element.text
    
def parseHtml(html):
        tree = etree.HTML(html)  

        #下面开始查找交易统计  
        # <ul id="ulDtcc"></ul>
        listTrade=[]
        hyperlinks = tree.xpath(u'//ul[@id="ulCjl"]/li')  
        print "hyperlinks:",hyperlinks  
        
        for hyperlink in hyperlinks:   
            #print hyperlink.tag
            if tryFindChild(hyperlink):
                listTrade.append(tryFindChild(hyperlink))
                #for it in  tryFindChild(hyperlink):
                #    print it 
         
        #下面开始查找多头 
        # <ul id="ulKtcc"></ul>
        listCall=[]
        hyperlinks = tree.xpath(u'//ul[@id="ulDtcc"]/li')  
        print "hyperlinks:",hyperlinks  
        
        for hyperlink in hyperlinks:   
            #print hyperlink.tag
            if tryFindChild(hyperlink):
                listCall.append(tryFindChild(hyperlink))
                #for it in  tryFindChild(hyperlink):
                #    print it 
                 
        #下面开始查找空头
        # <ul id="ulKtcc"></ul> 
        listPut=[]
        hyperlinks = tree.xpath(u'//ul[@id="ulKtcc"]/li')  
        print "hyperlinks:",hyperlinks  
        
        for hyperlink in hyperlinks:   
            #print hyperlink.tag
            if tryFindChild(hyperlink):
                listPut.append(tryFindChild(hyperlink))
                #for it in  tryFindChild(hyperlink):
                #    print it 
         
        return (listTrade,listCall,listPut)
 
def game(URL):
    html=getEastMoney(URL);
    #print html
    
    print "test parse html"
    summary = parseHtml(html)
    
    '''
    for list1 in   summary :
            for item in list1 :
                if len(item) == 4:
                    print item,'列表'
                else :
                    print item,'汇总' 
    '''                
    #检查交易量最大的前三
    #每一个品种的交易量大小不一样，螺纹多，焦炭少
    listtrade = summary[0]
    for i in range(3):
        if abs(int(listtrade[i][3])) > 10000:
            print "注意交易量变化",listtrade[i][0],listtrade[i][1],listtrade[i][2],listtrade[i][3]
    #检查多头前三
    listcall = summary[1]
    for i in range(3):
        if abs(int(listcall[i][3])) > 10000:
            print "注意多头仓位变化",listcall[i][0],listcall[i][1],listcall[i][2],listcall[i][3]
    #检查空头前三
    listput = summary[2]
    for i in range(3):
        if abs(int(listput[i][3])) > 10000:
            print "注意空头变化",listput[i][0],listput[i][1],listput[i][2],listput[i][3]
    
    #自动下载交易量前3名的
    #http://data.eastmoney.com/futures/sh/timeline.html?ex=069001005&va=RB&ct=rb1705
    #需要选好交易所，品种，合约，期货公司，然后点击查询，等待更新结果    

if __name__ == "__main__":  
    
    print "test html download"
    eastMoneyURLS=[r"http://data.eastmoney.com/futures/sh/data.html?date=&ex=069001007&va=I&ct=i1705",
                   r"http://data.eastmoney.com/futures/sh/data.html?date=&ex=069001005&va=RB&ct=rb1705",
                   r"http://data.eastmoney.com/futures/sh/data.html?date=&ex=069001007&va=J&ct=j1705"
                   ]
    
    eastMoneyTitle=['i1705',
                    'rb1705']
    for it in eastMoneyURLS:
        game(it)

    