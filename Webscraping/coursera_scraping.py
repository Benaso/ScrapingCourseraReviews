import xlrd
import requests
import xlwt
from bs4 import BeautifulSoup

wb = xlwt.Workbook(encoding="utf-8")
sheet = wb.add_sheet('webs')
sheet.write(0, 0, "webs")
data = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67"
}
query_params_ = {
    "page": 1
}
workbook = xlrd.open_workbook("datalists/pyRelClasses.xls")
sheet1 = workbook.sheet_by_index(0)

for row in range(1, sheet1.nrows):
    url = sheet1.cell_value(row, 0)
    response = requests.get(url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    div_tag = soup.find("div", class_="cds-9 css-0 cds-11 cds-grid-item cds-76")
    if div_tag is not None:
        url_update = url + '/reviews'
        # 爬取每节课的评论
        should_break = False
        while True:
            response_ = requests.get(f'{url_update}?{query_params_}', headers=headers)
            html_ = response_.text
            soup_ = BeautifulSoup(html_, "html.parser")
            p_tags = soup_.select("p")
            div_tag_ = soup_.find("div", class_="cds-9 css-1kspkkz cds-10")
            if div_tag_ is None:
                should_break = True
                break

            for p_tag in p_tags:
                span_tags = p_tag.select("span")
                for span_tag in span_tags:
                    contents_string = span_tag.string
                    if contents_string and len(contents_string) >= 20 and contents_string not in data:
                        # data.append(contents_string)
                        print(contents_string)

            next_page_link_ = soup_.find("a", attrs={'class_': '_n3m6ner'})
            if next_page_link_ is None:
                should_break = True
                break
            query_params_["page"] += 1

        if should_break:
            break
