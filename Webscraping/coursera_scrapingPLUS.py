from urllib.parse import urlencode
import requests
import xlwt
from bs4 import BeautifulSoup
# 添加头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 "
                  "Safari/537.36 Edg/114.0.1823.67"
}

course_webs = []
# 使用正则表达式来定义一个
base_url = "https://www.coursera.org/courses"
query_params = {
    "query": 'python',
    "index": 'prod_all_launched_products_term_optimization',
    "page": 1
}
# 使用xlwt来存储
wb = xlwt.Workbook(encoding="utf-8")
sheet = wb.add_sheet('contents')
sheet.write(0, 0, "contents")
while True:

    url = f"{base_url}?{urlencode(query_params)}"
    response = requests.get(url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    # 查找包含img的a的标签，并提取href的值
    a_tag_with_img = soup.select("a:has(img)")
    for a_tag in a_tag_with_img:
        href_value = a_tag.get('href')
        if (('https' and 'http') not in href_value) \
                and len(href_value) >= 2 \
                and ('browse' not in href_value):
            contents_webs = 'https://www.coursera.org' + href_value
            course_webs.append(contents_webs)

    # 获取下一页的链接
    next_page_link = soup.find("a", attrs={'class': 'cds-119 cds-113 cds-115 label-text box arrow css-1smvlxt cds-142'})
    # 检查是否还有下一页，如果没有则退出循环
    if next_page_link is None:
        break
    # 更新页码参数
    query_params["page"] += 1
for i in range(len(course_webs)):
    sheet.write(i+1, 0, course_webs[i])
wb.save("pyRelClasses.xls")

