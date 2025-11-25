import requests
from bs4 import BeautifulSoup
import time
import random
import csv

headers = {
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding" : "gzip, deflate, br, zstd",
        "Accept-Language" : "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Connection" : "keep-alive",
        "Host" : "nn.cian.ru",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0"
    }


#запрос на сайт для получения главной html-страницы
def main_page_download(counter, url, cookies):
    responce = requests.Session().get(url, headers=headers, cookies=cookies)
    time.sleep(random.randint(2, 4))
    if responce.status_code == 200:
        return responce.text
    else:
        print(f"Error: responce status code : {responce.status_code}")
        return None

    
#скачиваем все страницы аренды квартир и сразу обрабатываем
def flat_pages__download(source, cookies):
    soap = BeautifulSoup(source, 'lxml')
    links = soap.find("div", class_="x31de4314--fb02f2--wrapper").find_all("a", class_="x31de4314--_416c6--media")
    for link in links:
        responce = requests.Session().get(link.get('href'), headers=headers, cookies=cookies)
        page_parsing(responce.text) 
        time.sleep(random.randint(2, 4))


#обработка каждой html-страницы
def page_parsing(source):
    soap = BeautifulSoup(source, 'lxml')
    
    try:
        price =soap.find("div", class_="xa15a2ab7--fc68b9--amount").find("span").text
        price = price.split()[0] + price.split()[1]
    except:
        price = "не найдено"

    try:
        header_info = soap.find("div", class_="xa15a2ab7--_3e6a9--header-information")
        adress = header_info.find("span").get('content')
    except:
        adress = "не найдено"
    
    square = "не найдено"
    floor = "не найдено"
    building_year = "не найдено"
    try:
        block_under_pic = soap.find_all("span", class_="xa15a2ab7--_7735e--color_text-primary-default xa15a2ab7--_2697e--lineHeight_6u xa15a2ab7--_2697e--fontWeight_bold xa15a2ab7--_2697e--fontSize_16px xa15a2ab7--_17731--display_block xa15a2ab7--dc75cc--text")
        for item in block_under_pic:
            try:
                prev_sibling = item.previous_sibling
                while prev_sibling and (isinstance(prev_sibling, str) and prev_sibling.strip() == ""):
                    prev_sibling = prev_sibling.previous_sibling
                prev_text = prev_sibling.text
                if prev_text == "Общая площадь":
                    square = item.text.split()[0]
                elif prev_text == "Этаж":
                    floor = item.text 
                elif prev_text == "Год постройки":
                    building_year = item.text
            except:
                continue
    except:
        print("Ошибка block_under_pic")
    
    try:
        rooms = soap.find("div", class_="xa15a2ab7--_3e6a9--header-information").find("h1").text.split()[1][0]
        if rooms == "с":
            rooms = "студия"
    except:
        rooms = "не найдено"

    #записываем кортеж файлов. . .
    with open("full_data.csv", "a", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow((adress, rooms, square, floor, building_year, price))

#main-функция
def main():
    url = "https://nn.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&p=1&region=4885&type=4"
    responce = requests.Session().get(url, headers=headers)
    cookies = responce.cookies.get_dict()
    time.sleep(random.randint(2, 4))

    for counter in range(1,45):
        url = f"https://nn.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&p={counter}&region=4885&type=4"
        flat_pages__download(main_page_download(counter, url,cookies), cookies)
    return 0
#исполнение программы, вызовом главной функции
main()


