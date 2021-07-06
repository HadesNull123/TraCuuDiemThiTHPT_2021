import requests
import pandas as pd
import random
from bs4 import BeautifulSoup
import lxml

list_user_agent_pc = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/7.1.6 "
    "Safari/537.85.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.4.10 (KHTML, like Gecko) Version/8.0.4 "
    "Safari/600.4.10",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 "
    "Safari/537.78.2",
    "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 "
    "Mobile/12H321 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 "
    "Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 "
    "Safari/600.1.4",
    "Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 "
    "Mobile/11B554a Safari/9537.53",
    "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
]


class TraCuuDiemThi:
    def __init__(self, year, sbd):
        self.__year = year
        self.__sbd = sbd
        self.result = None

    def diem_thi_vietnamnet(self):
        """
        Get diem thi thong qua vietnamnet
        """
        try:
            url = "https://vietnamnet.vn/vn/giao-duc/tra-cuu-diem-thi-thpt/?y={}&sbd={}".format(self.__year, self.__sbd)
            headers = requests.utils.default_headers()
            headers.update({"User-Agent": list_user_agent_pc[int(random.randint(1, 10))]})
            raw_html = requests.get(url=url, headers=headers)
            df_list = pd.read_html(raw_html.text, encoding="utf-8")
            index = df_list[1].index
            response = {}
            for ind in range(0, len(index)):
                score = str(df_list[1].iloc[ind, 1])
                if score == "nan":
                    score = "Không tìm thấy"
                response.update({
                    str(df_list[1].iloc[ind, 0]): score
                })
            self.result = response
            return True
        except Exception as ex:
            return False

    def diem_thi_thptquocgia(self):
        """
        Get diem thi thong qua thptquocgia
        """
        try:
            url = "https://thptquocgia.edu.vn/diemthi/?sbd={}".format(self.__sbd)
            headers = requests.utils.default_headers()
            headers.update({"User-Agent": list_user_agent_pc[int(random.randint(1, 10))]})
            raw_html = requests.get(url=url, headers=headers)
            df_list = pd.read_html(raw_html.text, header=1)

            list_subjects = []
            list_score = []

            for sub in df_list[0]:
                list_subjects.append(str(sub))
            for score in df_list[0].values[0]:
                if str(score) == "nan":
                    list_score.append("Không tìm thấy")
                else:
                    list_score.append(str(score))

            response = dict(zip(list_subjects, list_score))
            self.result = response
            return True

        except Exception as ex:
            print(ex)
            return False

    def diem_thi_thanhnien(self):
        """
        Get diem thi thong qua thanhnien cac mon danh so tu D1->D12
        """
        try:
            list_score = []
            list_subjects = [
                "Toán", "Ngữ văn", "Vật lí", "Hóa học", "Sinh học", "KHTN",
                "Lịch sử", "Địa lí", "GDCD", "KHXH", "Ngoại ngữ", "D12"
            ]
            url = "https://thanhnien.vn/ajax/diemthi.aspx?kythi=THPT&nam={}&city=&text={}&top=no".format(
                self.__year,
                self.__sbd
            )

            headers = {
                "User-Agent": list_user_agent_pc[int(random.randint(1, 10))],
                "Host": "thanhnien.vn",
                "Referer": "https://thanhnien.vn/giao-duc/tuyen-sinh/2021/tra-cuu-diem-thi-thpt-quoc-gia.html",
                'Cookie': ".ASPXANONYMOUS=tYDLirsWThgnfg194a3vmVN4W5cY5hbC-GZLophHiCQgo3NLCgITNSn5LbYUNSC1kZcE \
                          nZ94sd1Ot8_7JCpdEpYYhB1dsVEO7pDYt7hqPZXTtkELP1rJAnNs_l9WAzg-Jc5lAtMt0-ibq8wQVPO0Vg2"
            }

            raw_html = requests.get(url=url, headers=headers)

            soup = BeautifulSoup(raw_html.text, features="lxml")

            all_td = soup.find_all("td")
            for score in all_td:
                if score.text == "":
                    list_score.append("Không tìm thấy")
                else:
                    list_score.append(str(score.text))
            response = dict(zip(list_subjects, list_score[6:]))
            self.result = response
            return True
        except Exception as ex:
            print(ex)
            return False

    def diem_thi_24h(self):
        """
        Get diem thi thong qua 2h.com.vn
        """
        try:
            url = "https://diemthi.24h.com.vn/?v_page=1&v_sbd={}&v_ten=&v_cum_thi=00".format(self.__sbd)
            headers = requests.utils.default_headers()
            headers.update({"User-Agent": list_user_agent_pc[int(random.randint(1, 10))]})
            raw_html = requests.get(url=url, headers=headers)
            df_list = pd.read_html(raw_html.text, header=1)

            list_subjects = []
            list_score = []

            for sub in df_list[0]:
                list_subjects.append(str(sub))
            for score in df_list[0].values[0]:
                if str(score) == "nan":
                    list_score.append("Không tìm thấy")
                else:
                    list_score.append(str(score))
            response = dict(zip(list_subjects[2:], list_score[2:]))
            response.pop("Trung bình", None)
            response.pop("Trung bình.1", None)
            self.result = response
            return True

        except Exception as ex:
            print(ex)
            return False


if __name__ == '__main__':
    tracuu = TraCuuDiemThi(year="2020", sbd="63001581")
    print(tracuu.diem_thi_thptquocgia())
    print(tracuu.diem_thi_vietnamnet())
    print(tracuu.diem_thi_thanhnien())
    print(tracuu.diem_thi_24h())