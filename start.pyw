import requests
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication


class Main:
    app = QApplication([])
    ui = uic.loadUi('ui/main.ui')

    url = 'https://xn--b1afk4ade.xn--90adear.xn--p1ai/proxy/check/driver'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}
    proxy = {'https': 'https://proxy_ip:port'}  #  HTTPS Proxy required for non-Russian IP addresses

    def __init__(self):
        self.ui.statusbar.showMessage("ver. 1.3")
        self.ui.submit.clicked.connect(self.get_result)
        self.render_ui()

    def parse_response(self, response):  #  Data validation func
        if response['code'] == 100:
            self.ui.textBrowser.setText(f"Номер В/У: {response['doc']['num']}\n")
            self.ui.textBrowser.append(f"Дата выдачи: {response['doc']['date']}\n")
            self.ui.textBrowser.append(f"Срок действия В/У: {response['doc']['srok']}\n")
            self.ui.textBrowser.append(f"Категиории: {response['doc']['cat']}\n")
            try:
                self.ui.textBrowser.append(f"Дата рождения владельца: {response['doc']['bdate']}\n")
            except Exception:
                self.ui.textBrowser.append("Дата рождения владельца: нет информации\n")
            try:
                self.ui.textBrowser.append(f"Стаж c: {response['doc']['stag']}\n")
            except Exception:
                self.ui.textBrowser.append("Стаж с: нет информации\n")
            try:
                self.ui.textBrowser.append(f"Последняя операция: {response['doc']['nameop']}\n")
            except Exception:
                self.ui.textBrowser.append("Последняя операция: нет информации\n")
            try:
                self.ui.textBrowser.append(f"Кем выдано: {response['doc']['division']}")
            except Exception:
                self.ui.textBrowser.append("Кем выдано: нет информации")
            self.ui.number.clear()
            self.ui.issue_date.clear()
        elif response['code'] == 200:
            self.ui.textBrowser.setText(f'{response["message"]}')
        else:
            self.ui.textBrowser.setText("Нет ответа от сервера ГБДД [parse_response ERROR]")

    def get_result(self):
        if self.ui.number.text().isdigit() and self.ui.issue_date.text().isdigit():
            try:
                data = self.ui.issue_date.text()
                payload = {"num": f"{self.ui.number.text()}",
                           "date": f"{data[4:]}-{data[2:4]}-{data[0:2]}"}  #  Normalize date to form: yyyy-MM-dd
                response = requests.post(url=self.url, headers=self.headers, params=payload, proxies=self.proxy).json()
                self.parse_response(response)
            except Exception:
                self.ui.textBrowser.setText("Ошибка соединения!!!")
        else:
            self.ui.textBrowser.setText("Введите корректный номер В/У или дату выдачи")

    def render_ui(self):
        self.ui.show()
        self.app.exec()


if __name__ == "__main__":
    Main()
