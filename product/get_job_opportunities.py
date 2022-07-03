"""
パーソルテクノロジースタッフのサイトからITエンジニアの求人情報を取得する
"""
import csv
import os
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
from db.db_utils import DbUtils


class GetJobOpportunities():

    def __init__(self):
        option = Options()
        option.add_argument('--headless')
        self.browser = webdriver.Chrome(executable_path=f'{path}/chromedriver', options=option)
        self.url = "https://persol-tech-s.co.jp/jobsearch/result/"
        self.db_operation = DbUtils
        self.db_connection = self.db_operation.connection(self)

    def start(self):
        """スクレイピング処理
        """
        self.browser.implicitly_wait(10)
        self.browser.get(self.url)

        print('start scraping...')

        try:
            # 最後のページURL取得
            end_url = self.browser.find_elements(By.XPATH, '//*[@class="p-pagination__link"]')[-1].get_attribute('href')
            while True:
                count = len(self.browser.find_elements(By.XPATH, '//*[@class="p-section--lv2"]'))
                # 取得した求人情報リストを順番にDBに登録する
                for i in range(count):
                    title = self.browser.find_elements(By.XPATH, '//*[@class="p-section--lv2"]/div/ul/li/div[1]/div[1]/h3/a')
                    occupation = self.browser.find_elements(By.XPATH, '//*[@class="p-section--lv2"]/div/ul/li/div[3]/div[1]/table/tbody/tr[1]/td')
                    salary = self.browser.find_elements(By.XPATH, '//*[@class="p-section--lv2"]/div/ul/li/div[3]/div[1]/table/tbody/tr[2]/td')
                    work_location = self.browser.find_elements(By.XPATH, '//*[@class="p-section--lv2"]/div/ul/li/div[3]/div[1]/table/tbody/tr[3]/td')
                    working_hours = self.browser.find_elements(By.XPATH, '//*[@class="p-section--lv2"]/div/ul/li/div[3]/div[1]/table/tbody/tr[4]/td')

                    # DB登録
                    self.insert_db(title[i].text, occupation[i].text, salary[i].text, work_location[i].text, working_hours[i].text)
                    self.db_connection.commit()

                # 現在のページURL取得
                cur_url = self.browser.current_url
                if cur_url == end_url:
                    jobs = self.select_db()
                    labels = ['TITLE', 'OCCUPATION', 'SALARY', 'WORK_LOCATION', 'WORKING_HOURS', 'CREATED_AT']
                    with open(f'{path}/csv/result.csv', 'w') as f:
                        writer = csv.DictWriter(f, fieldnames=labels)
                        writer.writeheader()
                        for job in jobs:
                            writer.writerow(job)
                    print('End scraping')
                    break

                # 次のページへ遷移
                next_page = self.browser.find_elements(By.XPATH, '//*[@class="p-pagination__item"]')[-2]
                next_page.click()

        except Exception as e:
            print(e)
        finally:
            self.browser.close()
            self.browser.quit()

    def insert_db(self, title, occupation, salary, work_location, working_hours):
        """取得した情報をDBに登録する

        Args:
            title(str): タイトル
            occupation(str): 職種
            salary(str): 給与
            work_location(str): 勤務地
            working_hours(str): 勤務時間
        """
        SQL_FILE = f'{path}/db/sql/insert.sql'
        with open(SQL_FILE, 'r', encoding='utf-8') as f:
            query = f.read().format(title=title,
                                    occupation=occupation,
                                    salary=salary,
                                    work_location=work_location,
                                    working_hours=working_hours)
        self.db_operation.write(self, query, SQL_FILE)

    def select_db(self):
        """DBに登録した情報をcsvに出力する

        Returns:
            jobs(list): 求人情報リスト
        """
        SQL_FILE = f'{path}/db/sql/select.sql'
        with open(SQL_FILE, 'r', encoding='utf-8') as f:
            query = f.read().format()
        jobs = self.db_operation.read(self, query, SQL_FILE)
        return jobs


if __name__ == '__main__':
    exec = GetJobOpportunities()
    exec.start()
