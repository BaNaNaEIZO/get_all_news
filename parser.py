import json
import pandas as pd
import requests
import datetime
import os
import shutil


class RamblePars:
    def __init__(self, days=1, pages=120, tag_file="tags.json", start_day=datetime.datetime.today()):
        current_time = start_day
        self.current_date = current_time
        self.days = days
        self.pages = pages
        self.tag_file = tag_file
        self.date_list = [current_time - datetime.timedelta(days=x) for x in range(days)]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"}
        self.tags = self.load_tag()

    def page_request(self):
        list_url = self.create_url()
        list_of_news = list()

        for day_url in list_url:
            current_page = 1
            list_value_annotation = list()
            # print(day_url)
            for page_url in day_url:
                current_page += 1
                data_json = requests.get(page_url, self.headers)
                data = json.loads(data_json.text)
                if data:
                    for i in range(len(data)):
                        value_annotation = data[i]["long_title"]
                        value_id = data[i]["id"]
                        value_normalized_title = data[i]["normalized_title"]
                        list_value_annotation.append([value_annotation, value_id, value_normalized_title])
                else:
                    print("{year}-{month}-{day}. ".format(year=self.current_date.year, month=self.current_date.month,
                                                          day=self.current_date.day), "Обработано страниц:",
                          current_page)
                    break
            yield list_value_annotation

    def search_news(self):
        all_tags = list()

        for key in self.tags.keys():
            all_tags.append(key)

        for list_value_annotation in self.page_request():
            file = f"files/news_{self.current_date.day}-{self.current_date.month}-{self.current_date.year}.xlsx"
            with pd.ExcelWriter(file) as news_xlsx_file:
                sum_news = [x * 0 for x in range(len(all_tags))]
                count_tag = 0
                for tag in all_tags:
                    news_list = []


                    for value_annotation in list_value_annotation:
                        for j in self.tags[tag]:
                            # print(value_annotation[i])
                            if value_annotation[0].find(j) > 0:
                                sum_news[count_tag] += 1
                                temp = value_annotation[0].replace('"', "")
                                my_str = '=HYPERLINK("{}", "{}")'.format(
                                    f"https://news.rambler.ru/{value_annotation[1]}-{value_annotation[2]}",
                                    temp)
                                # print(my_str, tag)
                                news_list.append(my_str)
                                # print(f"{self.current_date.day}-{self.current_date.month}-{self.current_date.year}")
                                # print(value_annotation, tag, j)
                                break
                    count_tag += 1
                    df = pd.DataFrame({"news": news_list})
                    # print(df)
                    df.to_excel(news_xlsx_file, sheet_name=f"{count_tag}_{tag}", index=True)
                sums_of_news = sum(sum_news)
                max_of_news = max(sum_news)
                percent = list()
                for news in sum_news:
                    percent.append(f"{round(news/max_of_news*100)}%")

                # print(sum_news)
                # print(sums_of_news)
                # print(max_of_news)
                # print(percent)

                df_total = pd.DataFrame()
                df_total["tag"] = all_tags
                df_total[max_of_news] = percent
                df_total[sums_of_news] = sum_news
                df_total.rename(index=lambda x: x+2)

                df_total.to_excel(news_xlsx_file, sheet_name="Итого", index=True)


    def load_tag(self):
        with open(self.tag_file, mode="r", encoding="utf-8") as r_file:
            data = r_file.read()
            data = json.loads(data)
            for item in data:
                tags = data[item].split(", ")
                tags = list(set([f" {x} " for x in tags]))
                data[item] = tags
        return data

    def create_url(self):
        for current_date in self.date_list:
            self.current_date = current_date
            full_day_url = list()
            for current_page in range(1, self.pages + 1):
                url = (f"https://peroxide.rambler.ru/v1/projects/1/clusters/?limit=50&page={current_page}&date="
                       f"{self.current_date.year}-{self.current_date.month}-{self.current_date.day}")
                full_day_url.append(url)
            yield full_day_url


def work_with_os():
    if os.path.isdir("files"):
        shutil.rmtree("files")
    os.mkdir("files")


def input_main():
    days = input("Введите количество дней: ")
    return int(days)


def choice_day():
    choice = input("Ввeдите дату или пропустите. Формат(dd/mm/yyyy): ")
    date = datetime.datetime.today()
    if choice:
        date = datetime.datetime.strptime(choice, '%d/%m/%Y').date()
    return date
