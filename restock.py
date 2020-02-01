import requests

class StockCheck:

    def __init__(self, name, url, checkMethod, encoding):
        self.name = name
        self.url = url
        self.checkMethod = checkMethod
        self.encoding = encoding
        self.last_status = False


    def getResponse(self):
        URL = self.url
        # 컴퓨터임을 인지하면 크롤링을 막는 웹사이트를 위해 user-agent 지정
        HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
        
        return requests.get(URL, headers = HEADERS)


    def check(self):
        res = self.getResponse()

        if res.encoding != self.encoding:
            res.encoding = self.encoding

        return self.checkMethod(res)

    def statusChanged(self):
        status = self.check()

        if (self.last_status != status):
            self.last_status = status
            return (True, not(self.last_status), self.last_status, self)
        
        return (False, self.last_status, status, self)


    def __str__(self):
        return "{} is {}".format(self.name, self.last_status)


if __name__ == "__main__":
    def accessoiresCheck(res):
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(res.text, 'html.parser')
        stock_div = soup.find("div", attrs={"id": "addToCartFormHolder"})

        if stock_div == None:
            return False

        class_list = stock_div['class']

        if 'hide' in class_list:
            return True

        return False


    multi_pochette_accessoires = StockCheck("멀티 포쉐트 악세수아"
        , "https://kr.louisvuitton.com/kor-kr/products/multi-pochette-accessoires-monogram-nvprod1770359v"
        , accessoiresCheck, "utf-8")
    stock = multi_pochette_accessoires.check()
    print(multi_pochette_accessoires.name, "Available? ", stock)
    (status_changed, last_status, current_status) = multi_pochette_accessoires.statusChanged()
    print(multi_pochette_accessoires.name, "Status Changed? ", status_changed, ", Last Status? ", last_status, ", Current Status? ", current_status)