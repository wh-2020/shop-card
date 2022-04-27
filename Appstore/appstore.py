import ddddocr
import time
import urllib.parse
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "Referer": "https://inquiry.zihexin.net/PC/query.html",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Accept": "application/json,text/javascript,*/*;q=0.01",
    "Origin": "https://inquiry.zihexin.net",
    "Host": "inquiry.zihexin.net",
    "X-Requested-With": "XMLHttpRequest",
}
#新建session会话，可以不用在加header和cookies
session = requests.session()
session.headers = headers
def Getyzm(card):
    time1 = time.strftime('%H:%M:%S',time.localtime(time.time()))
    url = "https://inquiry.zihexin.net/kaptcha.jpg?"+time1+urllib.parse.quote(" GMT 0800 (中国标准时间)")
    resp = session.get(url=url)
    with open('code.png','wb') as f:
        f.write(resp.content)
        # print("验证码下载成功")
    ocr = ddddocr.DdddOcr()
    img_bytes = resp.content
    #验证码识别结果
    res = ocr.classification(img_bytes)
    # print(res)
    GetCard(res,card)
    time.sleep(1)

def GetCard(res,card):

    url = "https://inquiry.zihexin.net/query.cp"
    data = {
        "barCode":"",
        "csCardNo":"",
        "appleCardNo": card,
        "verifyCode": res
    }
    try:
        resp = session.post(url=url,data=data)
        data = resp.json()
        if resp.status_code == 200 :
            # print(resp.json())
            # 卡金额
            amount = data.get("data").get("amount")
            # 卡号
            appleCardNo = data.get("data").get("appleCardNo")
            # 类型
            # OPT_TYPE = data.get("data")['cardActiveInfo'][0]['OPT_TYPE']
            # 激活时间
            TRANS_DATE = data.get("data")['cardActiveInfo'][0]['TRANS_DATE']
            # print(data.get("data")['cardExchangeInfo'])
            info = ""
            if data.get("data")['cardExchangeInfo']:
                pass
                # print("激活")
            else:
                info = "卡未使用"
            # #消费时间
            # print("amount:{},appleCardNo:{}".format(amount,appleCardNo))
            content = "卡号{},面值{},激活时间:{},{}".format(appleCardNo, amount, TRANS_DATE, info)
            writeFile(content)
    except:
        print("出现异常")
        print(resp.status_code)
def writeFile(content):
    with open("./applecard_resp.txt","a",encoding="utf-8") as f:
        f.write(content+"\n")
def main():
    f = open("applecard.txt")
    while True:
        line = f.readline()
        if not line:
            break
        card = line.strip('\n')
        # print(card)
        print("正在查询卡号:{}".format(card))
        Getyzm(card)
    f.close()
    print("*" * 25)
    print("卡号已查询完毕")
if __name__ == '__main__':

    main()