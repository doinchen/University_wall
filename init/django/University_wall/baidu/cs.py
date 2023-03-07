# import os
#
# # f = open('../media/taskimg/20230115195450.jpg', mode='wb')
# # f.truncate()
# # f.close()
# os.remove('../media/taskimg/210809039040.png')


# import requests
#
# API_KEY = "GUQ1GDI8a6p3Epwgr1IhyLzI"
# SECRET_KEY = "77Gt9l9npw5cIme5e4Kcx0EzQ198gGrE"
# urlid = 'http://192.168.42.111:15050/media/taskimg/20230207224453210809039040.mp4'
# name = '11a.mp4'
# urlname = 'http://192.168.42.111:15050/media/taskimg/20230207224453210809039040.mp4'
#
#
# def main(urlid,name,urlname):
#     url = "https://aip.baidubce.com/rest/2.0/solution/v1/video_censor/v2/user_defined?access_token=" + get_access_token()
#
#     payload = 'extId='+urlid+'&name='+name+'&videoUrl='+urlname
#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded',
#         'Accept': 'application/json'
#     }
#
#     response = requests.request("POST", url, headers=headers, data=payload)
#
#     print(response.text)
#
#
# def get_access_token():
#     """
#     使用 AK，SK 生成鉴权签名（Access Token）
#     :return: access_token，或是None(如果错误)
#     """
#     url = "https://aip.baidubce.com/oauth/2.0/token"
#     params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
#     return str(requests.post(url, params=params).json().get("access_token"))
#
#
# if __name__ == '__main__':
#     main(urlid,name,urlname)