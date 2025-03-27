import requests
from bs4 import BeautifulSoup
import csv
import time
import os
class ProductScraper:
    def __init__(self,url):
        """初始化爬虫，设置 URL 和请求头"""
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
        self.soup = None

    def fetch_page(self):
        """发送请求，获取网页内容"""
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            self.soup = BeautifulSoup(response.text, "html.parser")
        else:
            print(f"请求失败，状态码: {response.status_code}")
            self.soup = None

    def extract_info(self):
        """提取商品信息"""
        if not self.soup:
            return None

        title = self.soup.find("h2", class_="name")
        price = self.soup.select_one(".price span")
        description = self.soup.find("div", class_="description")
        image_tag = self.soup.find("img", id="main-image")
        buy_button = self.soup.find("a", class_="buy-button")
        buy_link = buy_button["href"] if buy_button else "未找到购买链接"

        return {
            "商品名称": title.get_text(strip=True) if title else "未找到商品名称",
            "价格": price.get_text(strip=True) if price else "未找到价格",
            "描述": description.get_text(strip=True) if description else "未找到描述",
            "图片链接": image_tag["src"] if image_tag else "未找到图片",
            "购买链接": buy_link
        }

    def get_stats(self):
        """获取商品信息的公开方法"""
        self.fetch_page()
        return self.extract_info()


class get_all_products_links():
    def __init__(self,url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
        self.soup = None

    def fetch_page(self):
        """发送请求，获取网页内容"""
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            self.soup = BeautifulSoup(response.text, "html.parser")
        else:
            print(f"请求失败，状态码: {response.status_code}")
            self.soup = None

    def extract_all_products_links(self):
        if not self.soup:
            return None
        product_links = []
        for a_tag in self.soup.find_all("a", href=True):
            if "/product/" in a_tag["href"]:
                full_link = "https://ec.horipro-international.com" + a_tag["href"]
                product_links.append(full_link)
        return list(set(product_links))

if __name__ == '__main__':
    main_url = input("请输入网址: ")

    main_url = "https://ec.horipro-international.com/liyuu"
    product_scraper = get_all_products_links(main_url)
    product_scraper.fetch_page()
    product_links = product_scraper.extract_all_products_links()

    if product_links:
        print(f"找到 {len(product_links)} 个商品")
    else:
        print("未找到商品链接，可能网站结构变动或请求失败")

    folder = "E:\\Coding-Project\\Scraper-Test\\Data"
    os.makedirs(folder, exist_ok=True)
    csv_filename = os.path.join(folder,"Liyuu官网爬虫测试.csv")

    if not os.path.exists(csv_filename):
        with open(csv_filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["商品名称", "价格", "描述", "图片链接", "购买链接"])
            writer.writeheader()

    for idx, product_url in enumerate(product_links):
        print(f"\n[{idx + 1}/{len(product_links)}] 爬取商品: {product_url}")

        scraper = ProductScraper(product_url)
        product_info = scraper.get_stats()

        if product_info:
            with open(csv_filename, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["商品名称", "价格", "描述", "图片链接", "购买链接"])
                writer.writerow(product_info)
            print(f"已保存: {product_info['商品名称']}")

        time.sleep(1)
