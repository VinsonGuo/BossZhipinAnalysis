import requests
from pyquery import PyQuery
import time
import pandas as pd
import math

headers = {
    # ":authority": "www.zhipin.com",
    # ":method": "GET",
    # ":path": "/c101280600/?query=Android&page=1&ka=page-1",
    # ":scheme": "https",
    # "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    # "accept-encoding": "gzip, deflate, br",
    # "accept-language": "zh-CN,zh-HK;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6,zh-TW;q=0.5",
    "cache-control": "max-age=0",
    "cookie": "lastCity=101280600; _uab_collina=156032408779522233715365; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1560324088; __c=1560324088; __g=-; __l=l=%2Fwww.zhipin.com%2F&r=https%3A%2F%2Fwww.google.com%2F; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1560324705; __a=44027020.1560324088..1560324088.5.1.5.5",
    # "dnt": "1",
    # "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36",
}


def main():
    for i in range(20, 30):
        parse_page(i)


def parse_page(page):
    url = "https://www.zhipin.com/c101280600/?query=Android&page=%s&ka=page-%s" % (
        page, page)
    r = requests.get(url, headers=headers)
    print(r.url)
    print(r.status_code)
    pq = PyQuery(r.text)
    job_items = pq("div.job-primary")
    # job_name  salary  company_name    company_number   company_location    exprience   education
    info_list = []
    for item in job_items.items():
        info_item = []
        info_item.append(item(".info-primary .job-title").text())
        info_item.append(item(".info-primary .red").text())
        info_item.append(item(".info-company .name>a").text())
        split_char = PyQuery("|")

        c = item(".company-text>p")
        cchild = c.find("em.vline")
        cchild.replace_with(split_char)
        cinfo = item(".company-text>p").text()
        cinfos = cinfo.split("\n|\n")
        info_item.append(cinfos[-1])

        i = item(".info-primary>p")
        child = i.find("em.vline")
        child.replace_with(split_char)
        info = item(".info-primary>p").text()
        infos = info.split("\n|\n")
        info_item.append(infos[0])
        info_item.append(infos[1])
        info_item.append(infos[2])
        info_list.append(info_item)
    print(info_list)

    df = pd.DataFrame(data=info_list, columns=[
        'job_name', 'salary', 'company_name', 'company_number', 'company_location', 'exprience', 'education'])
    df.to_csv('zhipin_android_jobs%s.csv' % page, index=False)
    print('已保存为csv文件.')
    time.sleep(30)


if __name__ == "__main__":
    main()
