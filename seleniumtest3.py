import os
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

chromedriver = r"D:\python\chromedriver_win32\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver

#driver = webdriver.Firefox()


#d1 = datetime.date.today()
d1 = datetime.date(2015,9,20)
d2 = d1 + datetime.timedelta(1)

#http://hotel.qunar.com/city/kyoto_kyo/dt-213/?_=1#from=hoteldetail&cityurl=kyoto_kyo&HotelSEQ=kyoto_kyo_213&fromDate=2015-09-15&toDate=2015-09-16&rnd=1441020825943&sgroup=-1&roomNum=1
#http://hotel.qunar.com/city/kyoto_kyo/dt-213/?#from=hoteldetail&cityurl=kyoto_kyo&HotelSEQ=kyoto_kyo_213&fromDate=2015-09-25&toDate=2015-09-26&rnd=1441021428122&sgroup=-1&roomNum=1
url1 = "http://hotel.qunar.com/city/kyoto_kyo/dt-213/?#from=hoteldetail&cityurl=kyoto_kyo&HotelSEQ=kyoto_kyo_213&"
#fromDate=2015-12-10
#&
#toDate=2015-12-11
url2="&rnd=1441020825943&sgroup=-1&roomNum=1"


f = open('dt-213.txt','w+',encoding='utf-8')

try:
    count=1
    while count<100:
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


