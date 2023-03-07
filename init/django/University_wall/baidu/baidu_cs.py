import base64
import urllib
import requests
from django.conf import settings

API_KEY = "GUQ1GDI8a6p3Epwgr1IhyLzI"
SECRET_KEY = "77Gt9l9npw5cIme5e4Kcx0EzQ198gGrE"

def baidu_text(a):
    url = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined?access_token=" + get_access_token()

    payload = 'text='+a
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)
    return response.text


def baidu_image(a,b):
    url = "https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/v2/user_defined?access_token=" + get_access_token()

    # image 可以通过 get_file_content_as_base64("C:\fakepath\1673784796178.jpg",True) 方法获取
    bt64 = get_file_content_as_base64(a, True)
    payload = 'image='+bt64+'&imgType='+b
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)
    return response.text


def baidu_video(videoid,video_name,videoUrl):
    url = "https://aip.baidubce.com/rest/2.0/solution/v1/video_censor/v2/user_defined?access_token=" + get_access_token()

    payload = 'extId='+videoid+'&name='+video_name+'&videoUrl='+videoUrl
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return response.text

def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    a = str(requests.post(url, params=params).json().get("access_token"))
    return a


# if __name__ == '__main__':
#     baidu_image()
#






