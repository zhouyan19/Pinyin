#! usr/bin/python
# -*- coding: utf-8 -*-
import sys
import json
import time
import random
from tqdm import tqdm
import requests
from fake_useragent import UserAgent

fpath = r"D:/大二下/人智导/拼音输入法/src/zhihu/"
ua = UserAgent()


def get_data(url):
    # headers = {
    #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    # }
    headers = {'User-Agent': ua.random}
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r = r.content.decode('utf-8')
        return r
    except requests.HTTPError as e:
        print(e)
        print("HTTPError")
        return ""
    except requests.RequestException as e:
        print(e)
        print("RequestException")
        return ""
    except Exception as e:
        print(e)
        print("Other Error")
        return ""


def parser(html):
    json_data = json.loads(html)['data']
    contents = []
    try:
        for item in json_data:
            if "content" in item:
                text = item['content']
                contents.append(text)
        return contents
    except Exception as e:
        print(e)
        print("Other error in parser.")


def save(contents, file):
    if not contents:
        return
    for content in contents:
        file.write(content)
        file.write('\n')


if __name__ == "__main__":
    # idx = sys.argv[1]
    idx = "28"
    fp = fpath + "zhihu_"
    fp += idx
    fp += ".txt"
    url_head = "https://www.zhihu.com/api/v4/questions/"
    url_ids = [
        "281271203",
        "46711189",
        "29364545",
        "26441300",
        "319258164",
        "38708083",
        "316017797",
        "393092090"
    ]
    url_mid = "/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=5&offset="
    url_tail = "&platform=desktop&sort_by=default"
    with open(fp, 'a', encoding="utf-8") as f:
        for idu in url_ids:
            print(idu)
            url_base = url_head + idu + url_mid
            url = url_base + '5' + url_tail
            html = get_data(url)
            if html == "":
                continue
            totals = json.loads(html, encoding="utf-8")['paging']['totals']
            print("Total number:", totals)
            page = 0
            for i in tqdm(range(totals // 5)):
                url = url_base + str(page) + url_tail
                html = get_data(url)
                contents = parser(html)
                save(contents, f)
                page += 5
                time.sleep(random.uniform(1.0, 3.0))
    print("done")
