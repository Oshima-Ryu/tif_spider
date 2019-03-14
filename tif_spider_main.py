import os

import requests
from bs4 import BeautifulSoup

# url = "http://data.ess.tsinghua.edu.cn/data/temp/Fromglc2015tif/0E_0N.tif"
# url = "http://data.ess.tsinghua.edu.cn/fromglc2015_v1.html"

def one_level_spider(url):
    response = requests.get(url)
    # html = response.text
    # soup = BeautifulSoup(html, features="lxml")
    html = response.content
    soup = BeautifulSoup(html)
    url_list = soup.find_all("a")
    for url_temp in url_list:
        print(url_temp.text.split(" ")[0])
        if url_temp.text.split(" ")[0] == "ftp":
            continue
        href = url_temp.get("href")
        # print(href.split(".")[-1])
        extension_str = href.split(".")[-1]
        if extension_str == "tif" or extension_str == "gz" or extension_str == "rar" or extension_str == "tar" or extension_str == "docx" or extension_str == "doc" or extension_str == "pdf":
            path_arr = href.split("/")
            path_str = "/".join(path_arr[3:-1]) + "/"
            # print(path_str)
            if not os.path.exists(path_str):
                os.makedirs(path_str)
            file_name = "/".join(path_arr[3:])
            print(file_name)
            if os.path.exists(file_name):
                continue
            print(href)
            with open(file_name, "wb") as f:
                f.write(response.content)
                f.close()
            # tif_response = requests.get(href)
            # print("status_code", tif_response.status_code)
            # if tif_response.status_code == 200:
            #     with open(file_name, "wb") as f:
            #         f.write(tif_response.content)
            #         f.close()

def two_level_spider(url, start_index=0):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features="lxml")
    url_list = soup.find_all("a")
    index = 0
    for url_temp in url_list:
        index += 1
        if index <= start_index:
            continue
        # print(url_temp.text)
        if url_temp.text.strip() == "view table":
            # print(url_temp)
            target_url = "http://data.ess.tsinghua.edu.cn" + url_temp.get("href")[1:]
            print(target_url)
            one_level_spider(target_url)


def start(url_dict):
    # 包含二级目录two_level_directory=True，是一级目录two_level_directory=False
    if url_dict.get("two_level_directory"):
        two_level_spider(url_dict.get("url"), url_dict.get("start_index"))
    else:
        one_level_spider(url_dict.get("url"))



if __name__ == "__main__":
    # url = "http://data.ess.tsinghua.edu.cn/landsat_pathList_fromglc_0_1.html"

    # 该url若包含二级目录two_level_directory=True，若是一级目录two_level_directory=False
    # url_dict = {
    #     "url": "http://data.ess.tsinghua.edu.cn/fromglc2017v1.html",
    #     "two_level_directory": False
    # }

    url_dict = {
        "url": "http://data.ess.tsinghua.edu.cn/landsat_pathList_fromglc_0_1.html",
        "two_level_directory": True,
        "start_index": 0,
    }
    start(url_dict)




    # test_url = "http://data.ess.tsinghua.edu.cn/data/temp/Fromglc2015tif/0E_0N.tif"
    # tif_response = requests.get(test_url)
    # print("status_code", tif_response.status_code)
    # if tif_response.status_code == 200:
    #     with open("asdasd.tif", "wb") as f:
    #         f.write(tif_response.content)
    #         f.close()