#匯入selenium 執行網頁模擬自動化
from selenium import webdriver
#匯入Keys，讓程式按鍵盤上的案件指令(確認、刪除那種)
from selenium.webdriver.common.keys import Keys
#匯入time函式插入模擬使用網頁步驟，因為伺服器連線會延遲，以免造成爬不到資料的錯誤
import time
#把文字資料寫在csv裡
import csv
#要下載圖片匯入檔案處理os
import os
#wget可以在網路上下載東西
import wget

#我的chromedriver路徑
PATH = "./chromedriver.exe"
driver = webdriver.Chrome(PATH)

#開啟訂房網網頁(Booking)
driver.get("https://www.booking.com/index.zh-tw.html?aid=1725925;label=competitors-chinese-zh-xt-9Q88Z6LD74pzKEYVyiHCPwS533248621385:pl:ta:p1:p2:ac:ap:neg:fi:tikwd-97178419:lp9040380:li:dec:dm:ppccp=UmFuZG9tSVYkc2RlIyh9YbMgw1lSrhIuP8sID6VbpyE;ws=&gclid=CjwKCAiAm7OMBhAQEiwArvGi3J-eMa20ch50HOXOV2BnyN014CGBaiA_NDmRfaP3CNDm6y6_xJ6XIxoC8u0QAvD_BwE")

#以下為模擬使用網頁
#先用滑鼠選擇入住人數為2人成人
driver.find_element_by_id("xp__guests__toggle").click()
time.sleep(0.5)
#滑鼠選擇入住時間11/19、11/20
driver.find_element_by_xpath("//form[@id='frm']/div/div[2]/div/div[3]/div/div/div/div/span").click()
time.sleep(0.5)
driver.find_element_by_xpath("//form[@id='frm']/div/div[2]/div[2]/div/div/div[3]/div/table/tbody/tr[3]/td[6]").click()
time.sleep(0.5)
driver.find_element_by_xpath("//form[@id='frm']/div/div[2]/div[2]/div/div/div[3]/div/table/tbody/tr[3]/td[7]/span/span").click()
time.sleep(0.5)
#搜尋目的地打台中火車站，F12以name的方式找尋輸入框
search = driver.find_element_by_name("ss")
search.send_keys("台中火車站")
time.sleep(0.5)
#鼠標停在搜尋欄，按下Enter確認搜尋
search.send_keys(Keys.RETURN)
time.sleep(1)
#按下先以價格排序
Link=driver.find_element_by_link_text('價格（低價優先）')
Link.click()

'''
time.sleep(1.5)
#按下只顯示私人房間(單獨套房)
Link=driver.find_element_by_link_text('只顯示私人房間')
Link.click()
'''

# 開啟輸出的 CSV 檔案，有中文要utf-8否則亂碼
f=open('hotel.csv', 'w', encoding='utf-8',newline='')
# 建立writer物件，物件名稱為csvWriter
csvWriter = csv.writer(f)
# 寫入一維串列當做標題
csvWriter.writerow(['飯店名稱','價錢','評分','床型','距離目的地多遠'])

#命名圖片資料夾，並把路徑儲存在變數裡
path = os.path.join('hotel_Img')
#會依照路徑與名稱創建一個資料夾
os.mkdir(path)
#建立圖片命名 飯店名稱陣列
img_name=[]

#⬇⬇爬資料的函式
def findData():
    #創建用來儲存飯店名稱的陣列，儲存圖片命名用，每次再次跑此函式會清空所有元素
    
    
    #等到1.5秒後網頁載入再開始爬
    time.sleep(1.5)
    #以class_name用class名稱查找資料
    #elements表示查找所有符合的資料(找一個用element)
    #評分處發現有重複的class_name所以使用css_selector來查找
    titles = driver.find_elements_by_class_name("_c445487e2") #飯店名稱
    prices = driver.find_elements_by_class_name("_e885fdc12") #價格
    scores = driver.find_elements_by_css_selector("._9c5f726ff.bd528f9ea6") #評分
    distances = driver.find_elements_by_css_selector("span.af1ddfc958 span.e36b9d9c39") #距離
    bed_count= driver.find_elements_by_css_selector("div._2075f7b46 div._4abc4c3d5") #床型數量
    imgs = driver.find_elements_by_class_name("e75f1d9859") #圖片
    
    #讀取飯店名稱、價格資料，使用zip()分別從各個 list 中取一個元素配成同一組tuple
    for title,price,score,bed,distance in zip(titles,prices,scores,bed_count,distances):
        print(title.text,price.text,score.text,bed.text,distance.text)
        csvWriter.writerow([title.text,price.text,score.text,bed.text,distance.text])
        img_name.append(title.text)
        #把飯店名稱加在陣列裡
        print(len(img_name))
        


    #每次讀取陣列都從[元素0]開始
    countC=0
    #讀取圖片並下載下來
    for img in imgs:
        #必須套個判斷，因為countC變數後面會+1，如果countC變數等於或大於陣列元素個數的話會出現錯誤!
        if countC < len(img_name):
            print(img.get_attribute("src"))#顯示圖片的scr
            #下載到剛剛創建的資料夾路徑，圖片的命名方式是由img_name陣列中的[元素0]開始
            save_as = os.path.join(path,'Img_' + str(img_name[countC]) + '.jpg')
            #下載圖片:download(圖片的src,存到圖片資料夾裡)
            wget.download(img.get_attribute("src"),save_as)
            #存完一個圖片後countC +1，等於讀取img_name陣列元素會+1，陣列往下一個一個命名，才會是正確的飯店圖片
            countC += 1
            print(countC)
        else:
            break
    img_name.clear()
    
#按下一頁，預計要抓6頁
count=0
while count<5:
    #呼叫讀取資料函式
    findData()
    count+=1
    #以class_name搜尋，按下一頁
    driver.find_element_by_class_name("_ea2496c5b").click()
    #等待網頁跳轉1.5秒
    time.sleep(1.5)
#關閉csv檔
f.close()
#關閉網頁
driver.close()







