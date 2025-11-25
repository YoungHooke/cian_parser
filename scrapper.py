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
url = "https://nn.cian.ru/snyat-kvartiru/"

#запрос на сайт для получения главной html-страницы
def download_html_page(): 
    responce = requests.Session().get(url, headers=headers)
    cookies = responce.cookies.get_dict()
    time.sleep(random.randint(1, 5))
    responce = requests.Session().get(url, headers=headers, cookies=cookies)

    if responce.status_code == 200:
        with open("cian_page.html", "w", encoding="utf8") as file:
            file.write(responce.text)

    else:
        print(f"Error: responce status code : {responce.status_code}")

#скачиваем все страницы аренды квартир
def page_parsing_download() :
    with open ('cian_page.html', "r", encoding="utf-8") as file:
        source = file.read()
    soap = BeautifulSoup(source, 'lxml')
    links = soap.find("div", class_="x31de4314--fb02f2--wrapper").find_all("a", class_="x31de4314--_416c6--media")
    counter = 0
    responce = requests.Session().get(url, headers=headers)
    cookies = responce.cookies.get_dict()
    time.sleep(random.randint(1, 5))

    counter = 0
    for link in links:
        responce = requests.Session().get(link.get('href'), headers=headers, cookies=cookies)
        time.sleep(random.randint(1, 5))
        counter += 1
        with open(f"rentanalyser/data/cian_page_flat№{counter}.html", "w", encoding="utf8") as file:
            file.write(responce.text)
        # soap = BeautifulSoup(responce.text, 'lxml')
        # price = soap.find("div", class_="xa15a2ab7--fc68b9--amount").find("span").text
        
        # break

#обработка каждой html-страницы из папки /data
def page_parsing():
    for counter in range(1, 29):
        with open(f"rentanalyser/data/cian_page_flat№{counter}.html", "r", encoding="utf-8") as file:
            soap = BeautifulSoup(file, 'lxml')
            price1div = soap.find("div", class_="xa15a2ab7--e39360--aside")
            if price1div:
                price2div = price1div.find("div", class_="xa15a2ab7--fc68b9--amount")
                if price2div:
                    price = price2div.find("span").text
            adress1div = soap.find("div", class_="xa15a2ab7--_3e6a9--header-information")
            if adress1div:
                adress2div = adress1div.find("span")
                if adress2div:
                    adress = adress2div.get('content')
            
            square1div = soap.find("div", class_="xa15a2ab7--_2be4c--text")
            square = None
            if square1div:
                square2div = square1div.find("span", style="letter-spacing: -0.2px;", class_="xa15a2ab7--_7735e--color_text-primary-default xa15a2ab7--_2697e--lineHeight_6u xa15a2ab7--_2697e--fontWeight_bold xa15a2ab7--_2697e--fontSize_16px xa15a2ab7--_17731--display_block xa15a2ab7--dc75cc--text")
                if square2div:
                    square = square2div.text
            description1div = soap.find("div", class_="xa15a2ab7--_3e6a9--header-information")
            if description1div:
                description = description1div.find("h1").text
                #записываем кортеж файлов. . .
            with open("full_data.csv", "a", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow((description, adress, square, price))



#main-функция
def main():
    page_parsing()

#исполнение программы, вызовом главной функции
main()

