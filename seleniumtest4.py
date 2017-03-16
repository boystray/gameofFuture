import os
import datetime

from os import system
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

chromedriver = r"D:\python\chromedriver_win32\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver

#driver = webdriver.Firefox()




#http://hotel.qunar.com/city/kyoto_kyo/dt-41/?tag=kyoto_kyo#fromDate=2015-12-10&toDate=2015-12-11&q=&from=l-breadcrumbs&fromFocusList=0&filterid=93154be6-335e-4c0c-a279-53eb7ab9fa78_A&showMap=0&qptype=&QHFP=ZSS_A8294CE2
#http://hotel.qunar.com/city/kyoto_kyo/dt-41/?tag=kyoto_kyo#fromDate=2015-12-10&toDate=2015-12-11&q=%E7%9A%87%E5%86%A0%E5%81%87%E6%97%A5&from=list_page&fromFocusList=0&filterid=329998ec-5f4a-45da-87e5-0b0ade2ac025_A&showMap=0&qptype=brand&QHFP=ZSS_A835FE16
#http://hotel.qunar.com/city/kyoto_kyo/dt-41/?#tag=kyoto_kyo&fromDate=2015-12-17&toDate=2015-12-18&from=hoteldetail&cityurl=kyoto_kyo&HotelSEQ=kyoto_kyo_41&rnd=1441119594602&sgroup=-1&roomNum=1
url1 = "http://hotel.qunar.com/city/kyoto_kyo/dt-41/?#tag=kyoto_kyo&"
#fromDate=2015-12-10
#&
#toDate=2015-12-11
url2="&from=hoteldetail&cityurl=kyoto_kyo&HotelSEQ=kyoto_kyo_41&rnd=1441119594602&sgroup=-1&roomNum=1"


f = open('dt-41.txt','a+',encoding='utf-8')

#d1 = datetime.date.today()
d1 = datetime.date(2015,10,14)
d2 = d1 + datetime.timedelta(1)


try:
    count=1
    while count<60:
        url = url1+"fromDate="+str(d1)+"&"+"toDate="+str(d2)+url2
        #print(url)
        print(d1)
        #print(d2)

        try:
            driver = webdriver.Chrome(chromedriver)
            driver.get(url)

            print('hehe')
            #如果找到登陆窗口，点击关闭按钮。
            #//*[@id="QunarPopBox"]
            
            #print(logonPop.text)
            #logonPop = WebDriverWait(driver, 60).until(
            #    EC.presence_of_element_located((By.CLASS_NAME, r'q_widget_login'))
            #)
            logonPop2 = driver.find_element_by_class_name(r'q_widget_login')
            
            print(logonPop2.text)            
            if logonPop2:
                print("logon")
                logonPopClose= driver.find_element_by_css_selector(r'span.login_close.login_icon')
                logonPopClose.click();
            else:
                print("nologon")
                
            
        except NoSuchElementException  :
                 print("NoSuchElementException")
        except  : 
                 print("Exception") 
        finally:

               try:
                    element = WebDriverWait(driver, 60).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.htl-type-content.b_result_list_on"))
                    )
                    #elem = driver.find_element_by_xpath(r'//*[@id="q-ra-171"]/div[1]')
                    elem = driver.find_element_by_class_name("js-room-title")
            
                    print(elem.text.replace("\n", " "))
                    f.write(str(d1)+" ")          
                    f.write(elem.text.replace("\n", " "))
                    f.write("\n")
               except : 
                     print("timeout") 
               finally:
            
                    driver.quit()
            
                    d1 = d2 
                    d2 = d1 + datetime.timedelta(1)

                    count=count+1
finally:
    f.close()
    print ('关机ing')
    system('halt')


