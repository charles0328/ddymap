import re, time, requests, certifi, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from pymongo import MongoClient

ca = certifi.where()
client = MongoClient('mongodb+srv://Sparta:SCXGQZH01HCkGvHo@cluster0.az0iq4u.mongodb.net/?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta

url = "https://map.seoul.go.kr/smgis2/seoulStory?tid=11103395&gucd="
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
req = requests.get(url, headers = headers)

driver = webdriver.Safari()
driver.implicitly_wait(10) #5초 안에 웹페이지를 load하면 바로 넘어가거나, 5초를 기다림
driver.get(url)

# 상점 리스트는 한 페이지에 10개, 페이지는 24까지 (마지막 페이지는 상점 2개만 있음)
# ID로 컨텐츠 정의
html_names = driver.find_elements(By.ID, "hContentsName") #ulContentsList > li:nth-child(1) > a
html_info = driver.find_elements(By.ID, "ulThemeBaseInfo")
html_detail = driver.find_elements(By.ID, "divContentsDetailInfo")
current_page = 1
current_shop = 1

#divPaging > span:nth-child(3~8) > a
# 페이지 넘기기 줄에는 버튼이 총 9개의 버튼이 있는데, 가운데 5개가 각각의 페이지이고, 8번째 버튼이 다음으로 넘어가는 버튼.
# 즉 1~5페이지를 훑은 후 6페이지로 넘어가려면 8번째 버튼인 nth-child(8)을 눌러줘야 한다.
# 그 다음 6페이지를 보려면 다시 nth-child(3)로 돌아가면 한다.


for p in range (5):
    for i in range (5):
        print('Current page is', current_page)
        # 페이지 로딩 시간이 있으므로 사이사이에 꼭 쉬어주기
        time.sleep(2)
        for n in range(1, 11):
            print('No.', current_shop)
            css_selector_list = f"#ulContentsList > li:nth-child({n}) > a"
            driver.find_element(By.CSS_SELECTOR, css_selector_list).click()
            time.sleep(5)
            # 가게 이름:
            for name in html_names:
                shop_name = name.text.strip()
                print('상호 :', shop_name)
            # 가게 분류 (카페, 리필샵 등)
            for category in html_info:
                category = re.findall(r'제로웨이스트상점 > (.*?)주소', category.text)
                shop_category = ''.join(category)
                print('분류 :', shop_category)
            # 가게 주소
            for info in html_info:
                address = re.findall(r'주소 : (.*?)연락처', info.text)
                shop_address = ''.join(address)
                print('주소 :', shop_address)

            # 위경도 변환 - 1. geopy 활용 (에러 나서 포기)
            # from geopy.geocoders import Nominatim
            # def geocoding(address):
            #     geolocoder = Nominatim(user_agent='South Korea', timeout=None)
            #     geo = geolocoder.geocode(address)
            #     crd0 = {str(geo.latitude), str(geo.longitude)}
            #     return crd0
            # crd0 = geocoding(shop_address)
            # crd = ', '.join(crd0)
            # print('위경도:', crd0)

            # 위경도 변환 - 2. 카카오 지도 API 활용 (에러 나서 포기)
            # def addr_to_lat_lon(addr):
            #     url = 'https://dapi.kakao.com/v2/local/search/address.json?query={shop_address}'.format(shop_address=addr)
            #     headers = {"Authorization": "KakaoAK 449a85241b162e919ca52c40935b9f15"}
            #     result = json.loads(str(requests.get(url, headers=headers).text))
            #     match_first = result['documents'][0]['address']
            #     return float(match_first['x']), float(match_first['y'])
            # crd0 = addr_to_lat_lon(shop_address)
            # crd = ', '.join(crd0)
            # print('위경도:', crd)

            # 몽고DB에 insert하기
            doc = {
                'Name': shop_name,
                'Category': shop_category,
                'Address': shop_address,
                #'crd': crd
                }
            db.wastemap.insert_one(doc)
            current_shop += 1

        # 페이지 넘기기 줄에서 i+4번째의 버튼을 눌러서 넘어 가라는 뜻
        css_selector_page = f"#divPaging > span:nth-child({i+4}) > a"
        driver.find_element(By.CSS_SELECTOR, css_selector_page).click()
        current_page += 1
        time.sleep(30)
