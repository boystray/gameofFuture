# -*- coding:utf-8 -*
#该程序是对百度的首页进行分析，并提取出其搜索框上面的导航条  
import httplib2  
import urllib2  
import re  
from lxml import etree  
"""
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
def tryFindChild(element):

    children = element.getchildren()
    if len(children):
        #return  children[0].getchildren()[0].text,children[1].text,children[2].text
        if len(children) == 3:
            children1=children[1].getchildren()
            children2 = children[2].getchildren()
            if len(children2):
                return  children[0].text,children[1].text,children[2].getchildren()[0].text
            elif len(children1):
                return  children[0].text,children[1].getchildren()[0].text,children[2].text
            else :
                return  children[0].text,children[1].text,children[2].text
                                
        elif     len(children) == 4:
            #print children[1].getchildren()[0].text
            return  children[0].getchildren()[0].text,children[1].getchildren()[0].text,children[2].text,children[3].getchildren()[0].text
            
        return element.text
    
def main():  
        #http = httplib2.Http()  
        #response,content = http.request("http://data.eastmoney.com/futures/sh/data.html?date=&ex=069001005&va=RB&ct=rb1705",'GET')  
        #print "response:",response  
        content = u"/home/strayboy/eastmoneyRB.html"
        print "content:",content  
        all_the_text = open(content).read( )
        tree = etree.HTML(all_the_text)  

        #上面的注释为要查找的部分html  
        # <ul id="ulCjl"></ul>
        # <ul id="ulDtcc"></ul>
        # <ul id="ulKtcc"></ul>
      
        #下面开始查找交易统计  
        hyperlinks = tree.xpath(u'//ul[@id="ulCjl"]/li')  
        print "hyperlinks:",hyperlinks  
        
        for hyperlink in hyperlinks:   
             #print hyperlink.tag
             for it in  tryFindChild(hyperlink):
                 print it 
         
        #下面开始查找多头 
        hyperlinks = tree.xpath(u'//ul[@id="ulDtcc"]/li')  
        print "hyperlinks:",hyperlinks  
        
        for hyperlink in hyperlinks:   
             #print hyperlink.tag
             for it in  tryFindChild(hyperlink):
                 print it 
                 
        #下面开始查找空头 
        hyperlinks = tree.xpath(u'//ul[@id="ulKtcc"]/li')  
        print "hyperlinks:",hyperlinks  
        
        for hyperlink in hyperlinks:   
             #print hyperlink.tag
             for it in  tryFindChild(hyperlink):
                 print it          
              
if __name__ == "__main__":  
        main()  