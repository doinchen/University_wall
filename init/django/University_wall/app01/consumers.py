import json
import re
import time
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from app01 import models
from urllib import parse
from baidu import baidu_cs
from automatic_check import check
from rest_framework import serializers
from django.forms.models import model_to_dict
URL = "http://192.168.42.111:15050/"
global re_back
CONN_LIST = []
MESS_LIST = []
class ChatConsumer(WebsocketConsumer):

    def websocket_connect(self,message):
        #接受客户端连接

        # 有客户端来向后端发送websocket连接的请求时，自动触发。
        # 服务端允许和客户端创建连接。|
        print("web数据推送",message)

        self.accept()
        print("数据推送",self)
        CONN_LIST.append(self)
        # [object Object]



    def websocket_receive(self,message):
        # 浏览器基于websocket向后端发送数据，自动触发接收消息。
        text = message['text']
        print('sdfasdfadafasdf',message)

        #print("接收消息",text)
        data = json.loads(text)
        #print(data.get('re_user'))
        if data.get('type') == "open":
            asse = 0
            for one in MESS_LIST:
                print(one.get('stu'))
                if one.get('stu') == data.get('stu'):
                    asse = 1
            if asse == 0:
                print('开始',self)
                dice = { "stu": data.get('stu'),"mess":self }
                MESS_LIST.append(dice)
                print('开始',MESS_LIST)




        if data.get('type') == "message":
            if data.get('app_stu') > data.get('user_stu'):
                room_number = data.get('app_stu') + data.get('user_stu')
            elif data.get('app_stu') < data.get('user_stu'):
                room_number = data.get('user_stu') + data.get('app_stu')
            print(room_number)
            models.message.objects.create(
                message=data.get('input'),
                type=data.get('type'),
                time_TS=check.AutoTS(data.get('time')),
                create_time=data.get('time'),
                user_id=data.get('app_stu'),
                re_user_id=data.get('user_stu'),
                room_num=room_number,
                read="false",
            )
            message_one = models.message.objects.filter(room_num=room_number).all().order_by('time_TS')
            cer = messageModelSerializer(instance=message_one, many=True)
            a = 0
            for on in cer.data:
                on.get('id')['rank'] = a
                # print("on",on.get('id').get('rank'))
                a = a + 1

            #print(cer.data)
            for x in MESS_LIST:
                print('xxxxx',x)
                if x.get('stu') == data.get('user_stu') or x.get('stu') ==  data.get('app_stu'):
                    print(x.get('stu'),x.get('mess'))
                    x.get('mess').send(json.dumps([{'list':cer.data}]))

                    #     x.get('mess').send(cer.data)  conn.send(json.dumps([{'aaa':'2'},{'list':cer.data}]))

        if data.get('type') == "comment":

            if data.get('re_user') == "0":
                re_user = None
            else:
                re_user = data.get('re_user')
            # re_back = data.get('content_text')
            # print(re_back)
            type_tit = models.Admin_send.objects.filter(title_type="comment").get().title

            if type_tit == "True":
                a = parse.quote(data.get('content_text'))
                ass = baidu_cs.baidu_text(a)
                #print(ass)
                b = ass.replace("false", "False")
                add = eval(b)
                #print(add["conclusionType"])
                if add["conclusionType"] == 1:
                    #print("passaaaaa")

                    time = data.get("create_time")
                    #print(time)
                    pattern = re.compile('[0-9]\d*')
                    TS = ""
                    for s in pattern.findall(time):
                        TS = TS + s
                    #print(TS)
                    models.CommentRecord.objects.create(
                        news_TS=data.get('news_TS'),
                        news_ustu=data.get('news_ustu'),
                        content_text=data.get('content_text'),
                        user_id=data.get('user'),
                        create_time=data.get('create_time'),
                        root_id=data.get('root_id'),
                        depth=data.get('depth'),
                        re_user_id= re_user,
                        time_TS=TS,
                    )



                    #print(cer.data)
                    if data.get('depth') == '1':
                        newlist = models.CommentRecord.objects.filter(depth='1', news_TS=data.get('news_TS'),news_ustu=data.get('news_ustu'), ).all().order_by('-time_TS')
                        ser = commentModelSerializer(instance=newlist, many=True)
                        for conn in CONN_LIST:
                            conn.send(json.dumps([{'aaa':'1'},{'list':ser.data}]))
                    if data.get('depth') != '1':
                        moreback = models.CommentRecord.objects.filter(root_id=data.get('root_id'),news_TS=data.get('news_TS'), news_ustu=data.get('news_ustu'), ).all().order_by('-time_TS')
                        cer = commentModelSerializer(instance=moreback, many=True)
                        for conn in CONN_LIST:
                            conn.send(json.dumps([{'aaa':'2'},{'list':cer.data}]))





                else:
                    re_back="发言不合规"
                    self.send(re_back)
        #self.send(text)
        #self.close()

    #def websocket_message
    def websocket_disconnect(self,message) :
        # 客户端与服务端断开连接时，自动触发。
        print("断开连接")

        raise StopConsumer()

class messageModelSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    #re_user = serializers.SerializerMethodField()
    class Meta:
        model = models.message
        fields = ['id', 'user', 're_user',  'time_TS','message','type','create_time','room_num']

    def get_id(self, obj):
        print(obj.id)
        return {'id':obj.id,'rank':None}
    def get_user(self, obj):
        print('45464646846464688',obj.user.student_number)
        return {'username': obj.user.username, 'avatarurl': URL + 'media/user/' + str(obj.user.avatarurl),
                'campus': str(obj.user.campus), 'student_num': str(obj.user.student_number)}

    # def get_re_user(self, obj):
    #     if obj.re_user == None:
    #         return ("null")
    #     # print('aasaaaaaa01',obj.re_user)
    #     # print('aasaaaaaa02',obj.user)
    #     # return ('1111')
    #     return {'username': obj.re_user.username, 'avatarurl': URL + 'media/user/' + str(obj.re_user.avatarurl),
    #             'campus': str(obj.re_user.campus), 'student_num': str(obj.re_user.student_number)}


class commentModelSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    re_user = serializers.SerializerMethodField()
    create_time = serializers.SerializerMethodField()
    fill_comment_favor = serializers.SerializerMethodField()
    class Meta:
        model = models.CommentRecord
        fields = ['id','news_TS','news_ustu','content_text','user','re_user','depth','root_id','time_TS','create_time','type','favor_count','viewer_count','comment_count','report_num','fill_comment_favor']

    def get_user(self,obj):
        #print(obj.user)
        return {'username':obj.user.username,'avatarurl':URL+'media/user/'+str(obj.user.avatarurl),'campus':str(obj.user.campus),'student_num':str(obj.user.student_number)}
    def get_re_user(self,obj):
        if obj.re_user == None:
            return ("null")
        # print('aasaaaaaa01',obj.re_user)
        # print('aasaaaaaa02',obj.user)
        #return ('1111')
        return {'username':obj.re_user.username,'avatarurl':URL+'media/user/'+str(obj.re_user.avatarurl),'campus':str(obj.re_user.campus),'student_num':str(obj.re_user.student_number)}
    def get_create_time(self,obj):
        # print(obj.create_time)
        #print(obj.time_TS)
        global ass_time
        ass_time = ''
        # print(time.strftime('%Y',time.localtime()))
        # print(obj.time_TS[:4])
        if obj.time_TS[:4] == time.strftime('%Y',time.localtime()):
            # print(time.strftime('%m%d', time.localtime()))
            # print(obj.time_TS[4:8])
            if int(obj.time_TS[4:8]) - int(time.strftime('%m%d', time.localtime())) ==0:
                # print(time.strftime('%M', time.localtime()))
                # print(obj.time_TS[-4:-2])

                ac = int(time.strftime('%H', time.localtime())) - int(obj.time_TS[-6:-4])
                if ac<6:
                    if ac<1:
                        ab = int(time.strftime('%M', time.localtime()))-int(obj.time_TS[-4:-2])
                        # print(str(ab)+"分钟前")
                        ass_time =str(ab)+"分钟前"

                    else:
                        # print(str(ac)+"小时前")
                        ass_time =str(ac)+"小时前"
                else:
                    # print("今天",obj.time_TS[-6:-4]+":"+obj.time_TS[-4:-2])
                    ass_time ="今天"+obj.time_TS[-6:-4]+":"+obj.time_TS[-4:-2]

            elif int(obj.time_TS[4:8]) - int(time.strftime('%m%d', time.localtime())) ==1:
                # print("昨天",obj.time_TS[-6:-4]+":"+obj.time_TS[-4:-2])
                ass_time ="昨天"+obj.time_TS[-6:-4]+":"+obj.time_TS[-4:-2]
            else:
                #print('aaa',obj.time_TS[4:6]+'-'+obj.time_TS[6:8])
                ass_time = obj.time_TS[4:6]+'-'+obj.time_TS[6:8]


        else:
            # print(obj.time_TS)
            # print(obj.time_TS[:4]+"-"+obj.time_TS[4:6]+"-"+obj.time_TS[6:8])
            ass_time = obj.time_TS[:4]+"-"+obj.time_TS[4:6]+"-"+obj.time_TS[6:8]
        return {"time01":ass_time,"time02":str(obj.create_time),"time03":obj.time_TS}
    def get_fill_comment_favor(self,obj):
        #print('safsdafas',obj)
        return ""

    # def get_type_text(self,obj):
    #     #print(model_to_dict(obj))
    #     #print(obj.type_text,obj.time_TS,obj.type)
    #
    #     if obj.type == 'text':
    #         #print("text")
    #         dict_text = models.Task.objects.filter(time_TS=obj.time_TS,stu_id=obj.type_text)
    #         #print(dict_text.get().text)
    #         return dict_text.get().text
    #     elif obj.type == 'image':
    #         #print('image')
    #         dict_image = models.Task.objects.filter(time_TS=obj.time_TS, stu_id=obj.type_text)
    #         #print(len(dict_image))
    #         num = 0
    #         assds = []
    #         for asses in dict_image:
    #
    #             if asses.hide == 'True':
    #                 #print(asses.hide)
    #                 assds.append({'url':asses.text})
    #
    #
    #                 num = num + 1
    #
    #
    #         return assds
    #     elif obj.type == 'video':
    #         #print("video")
    #         dict_video = models.Task.objects.filter(time_TS=obj.time_TS, stu_id=obj.type_text)
    #         #print(dict_video)
    #         video_dif = {}
    #         for ins in dict_video:
    #             #print(ins)
    #             if ins.hide == 'True':
    #                 #assds.append({'url': ins.text})
    #                 #print(ins.text[-4:])
    #                 if ins.text[-4:] == '.mp4':
    #                     #print('ssssssssssssssssssssss')
    #                     video_dif["video_url"] = ins.text
    #                 else:
    #                     video_dif["video_image"] = ins.text
    #         return video_dif