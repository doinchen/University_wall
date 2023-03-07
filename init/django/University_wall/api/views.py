from django.shortcuts import render
import requests
import re
import os
import time
from app01 import models,consumers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from django.forms.models import model_to_dict
from baidu import baidu_cs
from automatic_check import check
from django.conf import settings
from urllib import parse
from django.db.models import Q
URL = "http://192.168.42.111:15050/"
class Logined(APIView):
    def post(self,request,*args,**kwargs):

        print(request.data.get("stu_num"))
        b = models.UserInfo.objects.filter(id=request.data.get("stu_num"),student_number=request.data.get("stu_num"))
        print(model_to_dict(b.get()).get("avatarurl"))
        asd = URL+'media/user/'+ str(model_to_dict(b.get()).get("avatarurl"))
        return Response({"status":True,"asd":asd})
class LoginView(APIView):
    def post(self,request,*args,**kwargs):# print(request.data)#        {'student_id': '210809039040', 'password': '210809039040'}#         print(request.data.get('student_id'))#         print(request.data.get('password'))
        user_have_or_not = models.UserInfo.objects.filter(student_number=request.data.get('student_id'))# print(user_have_or_not)
        if not models.UserInfo.objects.filter(student_number=request.data.get('student_id')):
            return Response({"status": "null","message":"没有此用户"})
        user_login = models.UserInfo.objects.filter(student_number=request.data.get('student_id'),password=request.data.get('password'))
        if not user_login :
            return Response({"status":False,"message":"用户名或密码错误"})# print(user_login.first().username)
        user_login_1 = model_to_dict(user_login.get())
        a = user_login_1.get('avatarurl')
        user_login_1['avatarurl'] = URL+'media/user/'+str(a)# a2 = models.Campus.objects.filter(id=user_login_1.get('campus'))# print("原来",a2)# print("列表",list(a2))# print("get",a2.get())# print("字典",model_to_dict(a2.get()))# print("first",str(a2.first()))# user_login_1['campus'] = str(a2.first())
        if user_login_1['gender'] == 1:
            user_login_1['gender'] = '男'
        else:
            user_login_1['gender'] = '女'
        user_login_1['campus'] = str(models.Campus.objects.filter(id=user_login_1.get('campus')).first())
        user_login_1['department'] = str(models.Department.objects.filter(id=user_login_1.get('department')).first())
        user_login_1['profession'] = str(models.Profession.objects.filter(id=user_login_1.get('profession')).first())
        user_login_1['level'] = str(models.UserLevel.objects.filter(id=user_login_1.get('level')).first())# print(user_login_1)# , "user_login": model_to_dict(user_login)
        return Response({"status": True,"message":"登陆成功", "user_login":user_login_1})
class UpLoad_avatar(APIView):
    def post(self,request,*args,**kwargs):
        print(request.data)
        print(request.POST)
        print(request.FILES)
        img_name = request.POST.get("id")
        file_object = request.FILES.get(img_name)
        print(file_object)
        file = os.path.splitext(str(file_object))
        filename, type = file
        time = request.POST.get("time")
        pattern = re.compile('[0-9]\d*')
        # # str = request.POST.get("time")
        a = ""
        for s in pattern.findall(time):
            a = a + s
        img_name = img_name+a+type
        b = '%s/user/%s' % (settings.MEDIA_ROOT,img_name)
        print('asdfafdasfdsafafdsafas',b)
        f = open(b, mode='wb')
        for chunk in file_object.chunks():#chunk相当于文件块一点一点上传
            f.write(chunk)      #读取一点写一点
        f.close()
        models.UserAvatar.objects.create(
            name=request.POST.get("per_name"),
            student_id=request.POST.get("id"),
            username=request.POST.get("name"),
            avatarurl=img_name,
        )
        # print(img_name)
        # print(b)
        lest = baidu_cs.baidu_image('%s/user/%s' % (settings.MEDIA_ROOT,img_name), '0')
        ass=lest
        b = ass.replace("false","False")
        add=eval(b)
        # print(add.get("conclusionType"))
        if add.get("conclusionType") == 1:
            # print("通过")
            models.UserInfo.objects.filter(id=request.POST.get("id")).update(avatarurl=img_name)
            return Response(data=True)
        return Response({"图片违规"})
class Change_username(APIView):
    def post(self,request,*args,**kwargs):
        print(request.data)
        new_username = request.data.get("new_username")
        print(len(new_username.encode()))
        if len(new_username.encode())<=30:
            a = parse.quote(new_username)
            ass = baidu_cs.baidu_text(a)
            b = ass.replace("false", "False")
            add = eval(b)
            print(add["conclusionType"])
            if add["conclusionType"] ==1:
                models.UserInfo.objects.filter(id=request.data.get("id"),student_number=request.data.get("stu_num")).update(username=new_username)
                user = models.UserInfo.objects.filter(id=request.data.get("stu_num"),student_number=request.data.get("stu_num"))
                print(model_to_dict(user.get()).get("username"))
                username=model_to_dict(user.get()).get("username")
                return Response({"status": True,"username":username})
        return Response({"status":False})
class Receive(APIView):
    def post(self,request,*args,**kwargs):
        global statusmess
        global textmess
        global datamess
        time = request.data.get("create_time")        # print(time)
        pattern = re.compile('[0-9]\d*')
        TS = ""
        for s in pattern.findall(time):
            TS = TS + s        # print(TS)
        campus = models.Campus.objects.filter(title=request.data.get("campus")).get()
        department = models.Department.objects.filter(title=request.data.get("department")).get()
        profession = models.Profession.objects.filter(title=request.data.get("profession")).get()
        sss = models.Task.objects.filter(time_TS=TS).first()
        models.NewsMessage.objects.filter().create(
            # id=TS,
            #username=request.data.get("username"),
            user_id=request.data.get("student_number"),
            student_number=request.data.get("student_number"),
            #avatarurl =request.data.get("avatarurl"),
            campus = campus,
            department =department,
            profession=profession,
            create_time =request.data.get("create_time"),
            admin_hide ="0",
            user_hide ="True",
            type =request.data.get("type"),
            text =request.data.get("text"),
            type_text =request.data.get("student_number"),
            time_TS = TS,
        )
        if request.data.get("type") == "text":
            models.Task.objects.create(
                stu_id=request.data.get("student_number"),
                text=request.data.get("text"),
                create_time=request.data.get("create_time"),
                hide="0",
                time_TS=TS
            )
        print(sss)
        print("baidu_"+ request.data.get("type"))
        type_tit = models.Admin_send.objects.filter(title_type="baidu_"+ request.data.get("type")).get().title
        print(type_tit)
        if type_tit == "True":
            a = parse.quote(request.data.get("text"))
            ass = baidu_cs.baidu_text(a)
            print(ass)
            b = ass.replace("false", "False")
            add = eval(b)
            print(add["conclusionType"])
            if add["conclusionType"] == 1:
                print("发布成功")
                # admin_hide = models.NewsMessage.objects.filter(time_TS = TS,student_number=request.data.get("student_number")).get().admin_hide
                # admin_hide = int(admin_hide)+1
                models.NewsMessage.objects.filter(time_TS = TS,student_number=request.data.get("student_number")).update(admin_hide ='1')
                if request.data.get("type") == "text":
                    hide = models.Task.objects.filter(time_TS=TS, stu_id=request.data.get("student_number")).get().hide
                    hide = int(hide) + 1
                    models.Task.objects.filter(time_TS=TS,stu_id=request.data.get("student_number")).update(hide=str(hide))
                statusmess = True
                textmess = "发布成功"
                datamess = ''# return Response({"status": True,"text":"发布成功"})
            else:# models.NewsMessage.objects.filter().delete()print('aaaaaaaaaaaaaaaaaaaaaaaaaaaa')# models.Task.objects.filter().delete()print("发不失败")
                statusmess = False
                textmess = "发布失败"
                datamess = add["data"]# return Response({"status": False, "text": "发布失败","data":add["data"]})
        else:
            statusmess = False
            textmess = "管理员关闭了自审核"
            datamess = ''# return Response({"status": False, "text": "管理员关闭了自审核"})
        if request.data.get("type") == "image":
            print('image类型')# return Response({"status": True, "text": "image类型"})
        if request.data.get("type") == "video":
            print('video类型')# return Response({"status": True, "text": "video类型"})
        check.Check(TS,request.data.get("student_number"))
        return Response({"status": statusmess,"text":textmess,"data": datamess })
class Upload_Pictures(APIView):
    def post(self,request,*args,**kwargs):
        # print(request.data)
        # print(request.POST)
        #
        # print(request.FILES)
        img_name = request.POST.get("name")
        len = request.POST.get("len")

        file_object = request.FILES.get(img_name)
        file = os.path.splitext(str(file_object))

        filename, type = file
        time = request.POST.get("time")

        pattern = re.compile('[0-9]\d*')
        # str = request.POST.get("time")
        a = ""
        for s in pattern.findall(time):
            a = a + s

        img_name = a+img_name+type
        # print(img_name)
        b = '%s/taskimg/%s' % (settings.MEDIA_ROOT,img_name)
        f = open(b, mode='wb')
        for chunk in file_object.chunks():#chunk相当于文件块一点一点上传
            f.write(chunk)      #读取一点写一点
        f.close()
        models.Task.objects.create(create_time=request.data.get('time'),
                                   hide='0',
                                   text=URL+'media/taskimg/'+img_name,
                                   time_TS=a,
                                   stu_id=request.data.get('id'))
        mass = models.Task.objects.filter(stu_id=request.data.get('id'),time_TS=a,).all()
        # print(model_to_dict(mass))
        # print(mass)
        p=0
        for ss in mass:
            p=p+1
            # print(ss)
        # print('p',p)
        # print('len',len)
        if str(p) == len:
            title = models.Admin_send.objects.filter(title_type='baidu_image').get().title
            # print('图片上传完毕',title)
            if title =="True":
                # print("允许百度审核")
                for mess in mass:
                    # print(mess.hide)
                    # print(mess.id)


                    hide = mess.hide
                    hide = int(hide) + 1
                    models.Task.objects.filter( id=mess.id,time_TS=a, stu_id=request.data.get("id")).update(hide='1')

        # lest = baidu_cs.baidu_image('%s/user/%s' % (settings.MEDIA_ROOT, img_name), '0')
        # print(lest)
            check.Check(a,request.data.get("id"))


        return Response({"status":111})
class Upload_Video(APIView):
    def post(self,request,*args,**kwargs):
        global textmess
        global file_type
        global video_TS
        global lems
        lems = request.data.get('id')
        # print(request.data)
        # print(request.POST)
        # print(request.FILES)
        video_name = request.POST.get("name")
        file_object = request.FILES.get(video_name)
        file = os.path.splitext(str(file_object))

        filename, type = file
        # print(type)
        if type == '.mp4' or type == '.jpg' or type == '.png' or type == 'svg' or type == '.webp' :
            # print('视频类型')
            time = request.POST.get("time")

            pattern = re.compile('[0-9]\d*')
            # str = request.POST.get("time")
            video_TS = ""
            for s in pattern.findall(time):
                video_TS = video_TS + s

            img_name = video_TS + video_name + type
            # print(img_name)
            b = '%s/taskimg/%s' % (settings.MEDIA_ROOT, img_name)
            f = open(b, mode='wb')
            for chunk in file_object.chunks():  # chunk相当于文件块一点一点上传
                f.write(chunk)  # 读取一点写一点
            f.close()
            models.Task.objects.create(create_time=request.data.get('time'),
                                       hide='0',
                                       text=URL + 'media/taskimg/' + img_name,
                                       time_TS=video_TS,
                                       stu_id=request.data.get('id'))
            if type == '.mp4':
                file_type = "video"
            elif type == '.jpg' or type == '.png' or type == 'svg' or type == '.webp' :
                file_type = "image"
            # print('baidu_'+file_type)

            title = models.Admin_send.objects.filter(title_type='baidu_'+file_type).get().title
            # print('图片上传完毕', title)
            if title == "True":
                # print("允许百度审核")
                # hide = models.Task.objects.filter(time_TS=video_TS, stu_id=request.data.get("id")).get().hide
                # hide = int(hide) + 1
                # models.Task.objects.filter(time_TS=video_TS, stu_id=request.data.get("id")).update(hide=str(hide))
                if type == '.mp4':
                    # videourl = URL+'media/taskimg'+img_name
                    # ass = baidu_cs.baidu_video('%s/taskimg/%s' % (settings.MEDIA_ROOT, img_name),img_name,'%s/taskimg/%s' % (settings.MEDIA_ROOT, img_name))
                    # ass = baidu_cs.baidu_video('http://192.168.42.111:15050/media/taskimg/20230207224453210809039040.mp4', img_name,
                    #                            'http://192.168.42.111:15050/media/taskimg/20230207224453210809039040.mp4')
                    # print(ass)
                    #b = ass.replace("false", "False")
                    #add = eval(b)
                    # print(add["conclusionType"])
                    add = 1
                    if add == 1:
                        # hide = models.Task.objects.filter(text=URL + 'media/taskimg/' + img_name,time_TS=video_TS,stu_id=request.data.get('id')).get().hide
                        # hide = int(hide) + 1
                        models.Task.objects.filter(text=URL + 'media/taskimg/' + img_name,time_TS=video_TS,stu_id=request.data.get('id')).update(hide='1')
                        textmess = '上传成功'
                    else:
                        textmess = '审核未通过'





                elif type == '.jpg' or type == '.png' or type == 'svg' or type == '.webp':
                    #ass = baidu_cs.baidu_image(URL+'media/taskimg/'+img_name,'0')
                    ass = baidu_cs.baidu_image('%s/taskimg/%s' % (settings.MEDIA_ROOT, img_name), '0')
                    b = ass.replace("false", "False")
                    add = eval(b)
                    if add["conclusionType"] == 1:
                        # hide = models.Task.objects.filter(text=URL + 'media/taskimg/' + img_name,time_TS=video_TS,stu_id=request.data.get('id')).get().hide
                        # hide = int(hide) + 1
                        models.Task.objects.filter(text=URL + 'media/taskimg/' + img_name,time_TS=video_TS,stu_id=request.data.get('id')).update(hide='1')
                        textmess = '上传成功'
                    else:
                        textmess = '审核未通过'
            else:
                textmess = '管理员禁止了自动审核'





        else:
            textmess = '封面格式不支持gif，视频格式仅支持mp4'

        # video_list = models.Task.objects.filter(time_TS=video_TS, stu_id=request.data.get('id'))
        # print('API页面Task', len(video_list))
        video_text = models.NewsMessage.objects.filter(time_TS=video_TS, student_number=request.data.get('id')).all()
        # print('API页面NewsMessage', len(video_text))
        # abc = 0
        # for one in video_list:
        #     print(one.hide)
        #     if one.hide == '1':
        #         abc = abc+1
        #     else:
        #         return
        # if str(abc) == '2':
        if len(video_text) == 1:
            check.Check(video_TS,lems)
        return Response({"status":textmess})





        # if type == '.mp4':
        #     print('视频类型')
        #     title = models.Admin_send.objects.filter(title_type='baidu_video').get().title
        #     print('图片上传完毕', title)
        #     if title == "True":
        #         # videourl = URL+'mdeia/tasking'+img_name
        #         # ass = baidu_cs.baidu_video(videourl,img_name,videourl)
        #         # b = ass.replace("false", "False")
        #         # add = eval(b)
        #         # print(add["conclusionType"])
        #         add = {"conclusionType":1}
        #
        #         if add["conclusionType"] == 1:
        #             aaa = models.NewsMessage.objects.filter(time_TS=video_TS, student_number=request.data.get("id"))
        #             print('aasadfasa',aaa)
                    # if aaa == None:
                    #     print('xu')
                    #     models.NewsMessage.objects.create(
                    #         student_number=request.data.get("id"),
                    #         create_time =request.data.get("create_time"),
                    #         admin_hide ="True",
                    #         user_hide ="True",
                    #         type_text =request.data.get("id"),
                    #         time_TS = video_TS,)
                    # else:
                    #     models.NewsMessage.objects.filter(time_TS=video_TS, student_number=request.data.get("id")).update(admin_hide="vido")


                    # models.NewsMessage.objects.filter(time_TS=a, student_number=request.data.get("id")).update(
                    # admin_hide="True")
        #             return Response({"status":'视频审核成功'})
        #
        # elif type == '.jpg' or type == '.png' or type == 'svg' or type == '.webp' :
            # title = models.Admin_send.objects.filter(title_type='baidu_video').get().title
            # print('图片上传完毕', title)
            # if title == "True":
            #     videourl = URL + 'mdeia/tasking' + img_name
            #     ass = baidu_cs.baidu_image(videourl,0)
            # print('图片类型')
        # else:
        #     return Response({"status": '封面格式不支持gif，视频格式仅支持mp4'})



        #return Response({"status": 22})
class WX_indexModelSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    campus = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    profession = serializers.SerializerMethodField()
    create_time = serializers.SerializerMethodField()
    type_text = serializers.SerializerMethodField()
    class Meta:
        model = models.NewsMessage
        fields = ['id','user','campus','department','profession','create_time','admin_hide','user_hide',
            'type','text','type_text','favor_count','viewer_count','comment_count','time_TS'
        ]
    def get_user(self,obj):
        #print(obj.type_text)
        return {'username':obj.user.username,'avatarurl':URL+'media/user/'+str(obj.user.avatarurl),'type_text':obj.type_text}
    def get_campus(self,obj):
        return obj.campus.title
    def get_department(self,obj):
        return obj.department.title
    def get_profession(self,obj):
        return obj.profession.title
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
        return {"time01":ass_time,"time02":obj.create_time,"time03":obj.time_TS}
    def get_type_text(self,obj):
        #print(model_to_dict(obj))
        #print(obj.type_text,obj.time_TS,obj.type)

        if obj.type == 'text':
            #print("text")
            dict_text = models.Task.objects.filter(time_TS=obj.time_TS,stu_id=obj.type_text)
            #print(dict_text.get().text)
            return dict_text.get().text
        elif obj.type == 'image':
            #print('image')
            dict_image = models.Task.objects.filter(time_TS=obj.time_TS, stu_id=obj.type_text)
            #print(len(dict_image))
            num = 0
            assds = []
            for asses in dict_image:

                if asses.hide == 'True':
                    #print(asses.hide)
                    assds.append({'url':asses.text})


                    num = num + 1


            return assds
        elif obj.type == 'video':
            #print("video")
            dict_video = models.Task.objects.filter(time_TS=obj.time_TS, stu_id=obj.type_text)
            #print(dict_video)
            video_dif = {}
            for ins in dict_video:
                #print(ins)
                if ins.hide == 'True':
                    #assds.append({'url': ins.text})
                    #print(ins.text[-4:])
                    if ins.text[-4:] == '.mp4':
                        #print('ssssssssssssssssssssss')
                        video_dif["video_url"] = ins.text
                    else:
                        video_dif["video_image"] = ins.text
            return video_dif

    #     return obj.task.hide
class WX_index(APIView):
    def get(self,request,*args,**kwargs):
        newlist = models.NewsMessage.objects.filter(admin_hide='True').all().order_by('-time_TS')
        ser = WX_indexModelSerializer(instance=newlist,many=True)
        #print(ser)
        # for one in ser:
        #     print(one)
        # print(ser)


        return Response(ser.data,status=200)
class WX_video_groundModelSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    campus = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    profession = serializers.SerializerMethodField()
    create_time = serializers.SerializerMethodField()
    type_text = serializers.SerializerMethodField()
    class Meta:
        model = models.NewsMessage
        fields = ['id','user','campus','department','profession','create_time','admin_hide','user_hide',
            'type','text','type_text','favor_count','viewer_count','comment_count','time_TS'
        ]

    def get_user(self,obj):
        # print(obj.user.avatarurl)
        return {'username':obj.user.username,'avatarurl':URL+'media/user/'+str(obj.user.avatarurl),'type_text':obj.type_text}
    def get_campus(self,obj):
        return obj.campus.title
    def get_department(self,obj):
        return obj.department.title
    def get_profession(self,obj):
        return obj.profession.title
    def get_create_time(self,obj):
        # print(obj.create_time)
        # print(obj.time_TS)
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
        return {"time01":ass_time,"time02":obj.create_time,"time03":obj.time_TS}
    def get_type_text(self,obj):
        #print(model_to_dict(obj))
        #print(obj.type_text,obj.time_TS,obj.type)

        if obj.type == 'text':
            #print("text")
            dict_text = models.Task.objects.filter(time_TS=obj.time_TS,stu_id=obj.type_text)
            #print(dict_text.get().text)
            return dict_text.get().text
        elif obj.type == 'image':
            #print('image')
            dict_image = models.Task.objects.filter(time_TS=obj.time_TS, stu_id=obj.type_text)
            #print(len(dict_image))
            num = 0
            assds = []
            for asses in dict_image:

                if asses.hide == 'True':
                    #print(asses.hide)
                    assds.append({'url':asses.text})


                    num = num + 1


            return assds
        elif obj.type == 'video':
            #print("video")
            dict_video = models.Task.objects.filter(time_TS=obj.time_TS, stu_id=obj.type_text)
            #print(dict_video)
            video_dif = {}
            for ins in dict_video:
                #print(ins)
                if ins.hide == 'True':
                    #assds.append({'url': ins.text})
                    #print(ins.text[-4:])
                    if ins.text[-4:] == '.mp4':
                        #print('ssssssssssssssssssssss')
                        video_dif["video_url"] = ins.text
                    else:
                        video_dif["video_image"] = ins.text
            return video_dif
class WX_video_ground(APIView):
    def get(self, request, *args, **kwargs):
        newlist = models.NewsMessage.objects.filter(admin_hide='True',type="video").all().order_by('-time_TS')
        ser = WX_video_groundModelSerializer(instance=newlist,many=True)
        i = 1
        for ass in ser.data:
            print(ass.get('id'), len(ser.data))
            ass["id"]=str(i)
            i=i+1
        for ass in ser.data:
            print(ass.get('id'), len(ser.data))

        #print(ser)
        # for one in ser:
        #     print(one)
        # print(ser)


        return Response(ser.data,status=200)
class WX_detailModelSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    campus = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    profession = serializers.SerializerMethodField()
    create_time = serializers.SerializerMethodField()
    type_text = serializers.SerializerMethodField()
    class Meta:
        model = models.NewsMessage
        fields = ['id','user','campus','department','profession','create_time','admin_hide','user_hide',
            'type','text','type_text','favor_count','viewer_count','comment_count','time_TS'
        ]

    def get_user(self,obj):
        # print(obj.user.avatarurl)
        return {'username':obj.user.username,'avatarurl':URL+'media/user/'+str(obj.user.avatarurl),'type_text':obj.type_text}
    def get_campus(self,obj):
        return obj.campus.title
    def get_department(self,obj):
        return obj.department.title
    def get_profession(self,obj):
        return obj.profession.title
    def get_create_time(self,obj):
        # print(obj.create_time)
        # print(obj.time_TS)
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
        return {"time01":ass_time,"time02":obj.create_time,"time03":obj.time_TS}
    def get_type_text(self,obj):
        #print(model_to_dict(obj))
        #print(obj.type_text,obj.time_TS,obj.type)

        if obj.type == 'text':
            #print("text")
            dict_text = models.Task.objects.filter(time_TS=obj.time_TS,stu_id=obj.type_text)
            #print(dict_text.get().text)
            return dict_text.get().text
        elif obj.type == 'image':
            #print('image')
            dict_image = models.Task.objects.filter(time_TS=obj.time_TS, stu_id=obj.type_text)
            #print(len(dict_image))
            num = 0
            assds = []
            for asses in dict_image:

                if asses.hide == 'True':
                    #print(asses.hide)
                    assds.append({'url':asses.text})


                    num = num + 1


            return assds
        elif obj.type == 'video':
            #print("video")
            dict_video = models.Task.objects.filter(time_TS=obj.time_TS, stu_id=obj.type_text)
            #print(dict_video)
            video_dif = {}
            for ins in dict_video:
                #print(ins)
                if ins.hide == 'True':
                    #assds.append({'url': ins.text})
                    #print(ins.text[-4:])
                    if ins.text[-4:] == '.mp4':
                        #print('ssssssssssssssssssssss')
                        video_dif["video_url"] = ins.text
                    else:
                        video_dif["video_image"] = ins.text
            return video_dif
class WX_detail(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        time_TS = request.data.get('time_TS')
        type_text = request.data.get('type_text')
       # print(time_TS,type_text)
        commentlen = models.CommentRecord.objects.filter( news_TS=request.data.get('time_TS'),news_ustu=request.data.get('type_text'), ).all().order_by('-time_TS')

        #print(len(commentlen))
        models.NewsMessage.objects.filter(time_TS = request.data.get('time_TS'),type_text = request.data.get('type_text'), admin_hide='True').update(comment_count=len(commentlen))

        favorlen=models.Detail_favor.objects.filter(news_TS= request.data.get('time_TS'), news_ustu= request.data.get('type_text'))
        #print(len(favorlen))
        # print(favorlen)
        models.NewsMessage.objects.filter(time_TS = request.data.get('time_TS'),type_text = request.data.get('type_text')).update(favor_count=len(favorlen))





        #print(ser.data)

        #return Response({"status":'ok',"ass":ser.data},)



        list = models.CommentRecord.objects.filter(depth='1',news_TS = request.data.get('time_TS'),news_ustu = request.data.get('type_text'), ).all()
        for one in list:
            #print(one.id)
            number = models.CommentRecord.objects.filter(root_id=one.id,news_TS = request.data.get('time_TS'),news_ustu = request.data.get('type_text'), ).all()
            #print(len(number))
            models.CommentRecord.objects.filter(id=one.id,depth='1',news_TS = request.data.get('time_TS'),news_ustu = request.data.get('type_text'), ).update(comment_count=len(number))



        one = models.Detail_favor.objects.filter(news_TS=request.data.get('time_TS'),news_ustu=request.data.get('type_text'),
                                                 user=request.data.get('student_number')).first()
        #print(one)
        if one == None:
            fill_detail_favor = 0
        else:
            fill_detail_favor = 1

        two = models.Detail_viewer.objects.filter(news_TS=request.data.get('time_TS'),
                                                 news_ustu=request.data.get('type_text'),
                                                 user=request.data.get('student_number')).first()
        #models.Detail_viewer.objects.filter().delete()
        #print(two)
        if two == None:
            #print("+1")
            TS = check.AutoTS(request.data.get("create_time"))
            models.Detail_viewer.objects.filter().create(
                    news_TS=request.data.get('time_TS'),
                    news_ustu =request.data.get('type_text'),
                    user_id = request.data.get('student_number'),
                    create_time = request.data.get('create_time'),
                    time_TS = TS,
                )
        viewerlen=models.Detail_viewer.objects.filter(news_TS= request.data.get('time_TS'), news_ustu= request.data.get('type_text'))
        #print(len(favorlen))
        # print(favorlen)
        models.NewsMessage.objects.filter(time_TS = request.data.get('time_TS'),type_text = request.data.get('type_text')).update(viewer_count=len(viewerlen))















        newlist = models.NewsMessage.objects.filter(time_TS = request.data.get('time_TS'),type_text = request.data.get('type_text'), admin_hide='True')
        #print(newlist.get().type_text)
        #global FABL
        FABL = '0'
        if newlist.get().type_text != request.data.get('student_number'):
            one = models.Fans_Blogger.objects.filter(fans_id=request.data.get('student_number'),Blogger_id=newlist.get().type_text).first()
            print(one)
            if one == None:
                #models.Fans_Blogger.objects.create(fans=request.data.get('app_stu'),Blogger=request.data.get('user_stu'))
                #print('关注')
                FABL = '0'
            else:
                FABL = '1'

        ser = WX_detailModelSerializer(instance=newlist.all(), many=True)


        commentlist = models.CommentRecord.objects.filter(depth='1', news_TS=request.data.get('time_TS'),news_ustu=request.data.get('type_text'), ).all().order_by('-time_TS')
        cer = consumers.commentModelSerializer(instance=commentlist,many=True)



        for once in cer.data:
            #print(once.get("id"))
            one = models.Comment_favor.objects.filter(
                news_TS=request.data.get('time_TS'),
                news_ustu=request.data.get('type_text'),
                user=request.data.get('student_number'),
                depth="1",
                comment_id=once.get("id"),
            ).first()
            if one==None:
                #print("空")
                once["fill_comment_favor"]=""
            else:
                #print("_fill")
                once["fill_comment_favor"] = "_fill"

        return Response({"data":ser.data,"comment":cer.data,"fill_detail_favor":fill_detail_favor,
                         "FABL":FABL,
                         "status":200})
class SecondComment(APIView):
    def post(self, request, *args, **kwargs):
        # print(request.data)
        # print(request.data.get('time_TS'))
        # print(request.data.get('id'))
        # print(request.data.get('user'))
        # time_TS = request.data.get('time_TS')
        # id = request.data.get('id')
        # user = request.data.get('user')

        # print(time_TS)
        # print(id)
        # print(user)

        #
        commenthead = models.CommentRecord.objects.filter(time_TS = request.data.get('time_TS'),id = request.data.get('id'),user_id = request.data.get('user')).all().order_by('-time_TS')
        ser = consumers.commentModelSerializer(instance=commenthead,many=True)

        commentlist = models.CommentRecord.objects.filter(root_id=request.data.get('id')).all().order_by('-time_TS')
        cer = consumers.commentModelSerializer(instance=commentlist, many=True)
        #print(cer.data)
        for once in cer.data:
            #print(once.get("id"))
            one = models.Comment_favor.objects.filter(
                ~Q(depth="1"),
                comment_id=once.get("id"),
                news_TS=request.data.get('news_TS'),
                news_ustu=request.data.get('news_ustu'),
                user=request.data.get('user_check'),


            ).first()
            if one==None:
                #print("空")
                once["fill_comment_favor"]=""
            else:
                #print("_fill")
                once["fill_comment_favor"] = "_fill"


        return Response({"data": ser.data,"datalist":cer.data,"status":200})
class Detail_favor(APIView):
    def post(self, request, *args, **kwargs):
        #print(request.data)
        #print(request.POST)
        one = models.Detail_favor.objects.filter(news_TS=request.data.get('news_TS'),news_ustu=request.data.get('news_ustu'),user=request.data.get('user')).first()
        #print(one)
        TS = check.AutoTS(request.data.get("create_time"))
        if one == None:
            print("+1")
            models.Detail_favor.objects.create(
                news_TS=request.data.get('news_TS'),
                news_ustu =request.data.get('news_ustu'),
                user_id = request.data.get('user'),
                yes_or_no = "yes",
                create_time = request.data.get('create_time'),
                time_TS = TS,
                whether_read ="false",
            )
            fill_detail_favor = 1
        else:
            models.Detail_favor.objects.filter(news_TS=request.data.get('news_TS'),news_ustu=request.data.get('news_ustu'), user=request.data.get('user')).delete()
            fill_detail_favor = 0

        commentlen=models.Detail_favor.objects.filter(news_TS=request.data.get('news_TS'), news_ustu=request.data.get('news_ustu'))
        #print(len(commentlen))
        #print(commentlen)
        models.NewsMessage.objects.filter(time_TS=request.data.get('news_TS'), type_text=request.data.get('news_ustu')).update(favor_count=len(commentlen))

        newlist = models.NewsMessage.objects.filter(time_TS=request.data.get('news_TS'),type_text=request.data.get('news_ustu'), admin_hide='True').all()
        #print('listfan',newlist)
        ser = WX_detailModelSerializer(instance=newlist, many=True)
        #print('点赞返回',ser.data)






        return Response({"data": ser.data,"fill_detail_favor":fill_detail_favor,"status":10086})
class Comment_fover(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        one = models.Comment_favor.objects.filter(
            news_TS=request.data.get('news_TS'),
            news_ustu=request.data.get('news_ustu'),
            user=request.data.get('user'),
            depth=request.data.get('depth'),
            comment_id=request.data.get('comment_id'),
            ).first()
        print(one)
        TS = check.AutoTS(request.data.get("create_time"))
        if one == None:
            #print("++1")
            models.Comment_favor.objects.create(
                news_TS=request.data.get('news_TS'),
                news_ustu=request.data.get('news_ustu'),
                user_id=request.data.get('user'),
                depth=request.data.get('depth'),
                comment_id=request.data.get('comment_id'),
                create_time=request.data.get('create_time'),
                time_TS=TS,
                yes_or_no="yes",
                whether_read="false",
            )
        else:
            models.Comment_favor.objects.filter(
                news_TS=request.data.get('news_TS'),
                news_ustu=request.data.get('news_ustu'),
                user=request.data.get('user'),
                depth=request.data.get('depth'),
                comment_id=request.data.get('comment_id'),
            ).delete()
        commentlen=models.Comment_favor.objects.filter(
            news_TS=request.data.get('news_TS'),
            news_ustu=request.data.get('news_ustu'),
            depth=request.data.get('depth'),
            comment_id=request.data.get('comment_id'),
            )
        print(len(commentlen))
        #print(commentlen)

        models.CommentRecord.objects.filter( news_TS=request.data.get('news_TS'),news_ustu=request.data.get('news_ustu'),depth=request.data.get('depth'),
            id=request.data.get('comment_id'),).update(favor_count=len(commentlen))

        commentlist = models.CommentRecord.objects.filter(depth="1", news_TS=request.data.get('news_TS'),news_ustu=request.data.get('news_ustu'), ).all().order_by('-time_TS')
        cer = consumers.commentModelSerializer(instance=commentlist,many=True)


        root_id = models.CommentRecord.objects.filter(id=request.data.get('comment_id'),).get().root_id
        print(root_id)
        sedcommentlist = models.CommentRecord.objects.filter(~Q(depth="1"), root_id=root_id, news_TS=request.data.get('news_TS'),news_ustu=request.data.get('news_ustu'), ).all().order_by('-time_TS')
        ser = consumers.commentModelSerializer(instance=sedcommentlist, many=True)


        for once in cer.data:
            #print(once.get("id"))
            one = models.Comment_favor.objects.filter(
                news_TS=request.data.get('news_TS'),
                news_ustu=request.data.get('news_ustu'),
                user=request.data.get('user'),
                depth="1",
                comment_id=once.get("id"),
            ).first()
            if one==None:
                #print("空")
                once["fill_comment_favor"]=""
            else:
                #print("_fill")
                once["fill_comment_favor"] = "_fill"
        for once in ser.data:
            #print(once.get("id"))
            one = models.Comment_favor.objects.filter(
                ~Q(depth="1"),
                news_TS=request.data.get('news_TS'),
                news_ustu=request.data.get('news_ustu'),
                user=request.data.get('user'),

                comment_id=once.get("id"),
            ).first()
            if one==None:
                #print("空")
                once["fill_comment_favor"]=""
            else:
                #print("_fill")
                once["fill_comment_favor"] = "_fill"




        return Response({"comment":cer.data,"sedcomment":ser.data,"status":10086})

    #return Response({ "comment": cer.data, "status": 200})
class Fans_Blogger(APIView):
    def post(self, request, *args, **kwargs):
        global FABLE
        print(request.data.get('user_stu'))
        print(request.data.get('app_stu'))

        if request.data.get('user_stu') != request.data.get('app_stu'):
            one = models.Fans_Blogger.objects.filter(fans_id=request.data.get('app_stu'),Blogger_id=request.data.get('user_stu')).first()
            print(one)
            if one == None:
                models.Fans_Blogger.objects.create(fans_id=request.data.get('app_stu'),Blogger_id=request.data.get('user_stu'))
                print('关注')
                FABLE = '1'
            else:
                models.Fans_Blogger.objects.filter(fans_id=request.data.get('app_stu'),Blogger_id=request.data.get('user_stu')).delete()
                print('取关')
                FABLE = '0'

        return Response({"FABL":FABLE})
class blogerModelSerializer(serializers.ModelSerializer):
    Blogger = serializers.SerializerMethodField()
    class Meta:
        model = models.Fans_Blogger
        fields = ['id','Blogger']

    def get_Blogger(self,obj):
        #print(obj.Blogger)
        return {'username':obj.Blogger.username,'avatarurl':URL+'media/user/'+str(obj.Blogger.avatarurl),'student_number':obj.Blogger.student_number}
class Active(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        #models.Fans_Blogger.objects.filter(fans_id=request.data.get('userstu')).delete()
        bloger_num = models.Fans_Blogger.objects.filter(fans_id=request.data.get('userstu'))
        print(bloger_num.first())
        if bloger_num.first() == None:
            list = '您还未关注任何人'
            blog_list = '请去关注一个人'
            reser = 400

        else:
            filler = ''
            for once in bloger_num:
                print(str(once.Blogger.student_number))
                if filler == '':
                    filler = Q(student_number=once.Blogger.student_number)
                else:
                    filler = filler|Q(student_number=once.Blogger.student_number)
            filler = filler&Q(admin_hide='True')
            print(filler)
            # ass = Q(student_number='210809039040')&Q(student_number='210809039040')
            ass = models.NewsMessage.objects.filter(filler).all().order_by('-time_TS')
            print(ass)
            ser = WX_indexModelSerializer(instance=ass,many=True)
            print(ser.data)
            list = ser.data
            cer = blogerModelSerializer(instance=bloger_num.all().order_by('-id'), many=True)
            blog_list = cer.data
            reser = 200
        return Response({
            "list":list,"blog_list":blog_list,
            "reses":reser})
class blog_once(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        if request.data.get('type') == 'once':
            fillter = Q(student_number=request.data.get('stu'))
        elif request.data.get('type') == 'all':
            bloger_num = models.Fans_Blogger.objects.filter(fans_id=request.data.get('stu'))
            fillter = ''
            for once in bloger_num:
                #print(str(once.Blogger.student_number))
                if fillter == '':
                    fillter = Q(student_number=once.Blogger.student_number)
                else:
                    fillter = fillter | Q(student_number=once.Blogger.student_number)
        fillter = fillter&Q(admin_hide='True')
        print(fillter)
        ass = models.NewsMessage.objects.filter(fillter).all().order_by('-time_TS')
        #print(ass)
        ser = WX_indexModelSerializer(instance=ass, many=True)
        #print(ser.data)
        return Response({"list":ser.data})
class user_US(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)

        Blogger = len(models.Fans_Blogger.objects.filter(Blogger_id = request.data.get("stu")))
        Fans = len(models.Fans_Blogger.objects.filter(fans_id=request.data.get("stu")))

        print(Fans)


        user_once = models.UserInfo.objects.filter(student_number=request.data.get("stu"))
        print(user_once.get().student_number)
        FABLE='-1'
        if user_once.get().student_number != request.data.get('student_number'):
            print('111111111')
            one = models.Fans_Blogger.objects.filter(fans_id=request.data.get('student_number'),Blogger_id=user_once.get().student_number).first()
            #print(one)
            if one == None:
                #models.Fans_Blogger.objects.create(fans=request.data.get('app_stu'),Blogger=request.data.get('user_stu'))
                print('0')
                FABLE = '0'
            else:
                FABLE = '1'
                print('1')


        ser = user_USModelSerializer(instance=user_once.all(), many=True)
        oneself = models.NewsMessage.objects.filter(admin_hide='True',type_text=request.data.get("stu")).all().order_by("-time_TS")
        favor_count = 0
        for one in oneself:
            #print(one.favor_count)
            favor_count = favor_count + one.favor_count
        #print(favor_count)

        cer = WX_indexModelSerializer(instance=oneself,many=True)



        #print(ser.data)
        return Response({"FABLE":FABLE,
            "favor_count":favor_count,"Blogger":Blogger,"Fans":Fans,
            "head":ser.data,"list": cer.data})

class user_USModelSerializer(serializers.ModelSerializer):

    avatarurl = serializers.SerializerMethodField()
    campus = serializers.SerializerMethodField()

    class Meta:
        model = models.UserInfo


        fields = ['id','username','avatarurl','student_number','campus',]

    def get_avatarurl(self,obj):
        #print(obj.avatarurl)
        return URL+'media/user/'+str(obj.avatarurl),

    def get_campus(self, obj):

        return str(obj.campus)

class type_click(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        if request.data.get("type") == "all":
            type_once = models.NewsMessage.objects.filter(type_text=request.data.get('stu')).all().order_by("-time_TS")
        else:
            type_once = models.NewsMessage.objects.filter(type=request.data.get('type'),type_text=request.data.get('stu')).all().order_by("-time_TS")
        ser = WX_indexModelSerializer(instance=type_once,many=True)
        print(ser.data)
        return Response({
            "list":ser.data,
            "status":200})

class room_messsage(APIView):
    def post(self, request, *args, **kwargs):
        print('room_messsage',request.data)

        # time = request.data.get("time")
        # pattern = re.compile('[0-9]\d*')
        # # str = request.POST.get("time")
        # a = ""
        # for s in pattern.findall(time):
        #     a = a + s
        # print(a)
        if request.data.get('app_stu')>request.data.get('user_stu'):
            room_number = request.data.get('app_stu') + request.data.get('user_stu')
        elif request.data.get('app_stu')<request.data.get('user_stu'):
            room_number = request.data.get('user_stu') + request.data.get('app_stu')
        message_one = models.message.objects.filter(room_num=room_number).all().order_by('time_TS')
        cer =consumers.messageModelSerializer(instance=message_one, many=True)
        print(len(cer.data))
        a = 0
        for on in cer.data:
            on.get('id')['rank']=a
            #print("on",on.get('id').get('rank'))
            a=a+1



        one = models.room.objects.filter(member=request.data.get('app_stu'),room_num=room_number).first()
        two = models.room.objects.filter(member=request.data.get('user_stu'), room_num=room_number).first()
        print(one,two)
        if one== None and two ==None:
            print("船检")
            models.room.objects.create(member=request.data.get('app_stu'),room_num=room_number)
            models.room.objects.create(member=request.data.get('user_stu'), room_num=room_number)
        # else:
        #     print("已创建")



        return Response({
            #"list":ser.data,
            "status":200,
            "list":cer.data
        })

class searchclick(APIView):
    def post(self, request, *args, **kwargs):

        print(request.data)
        newlist = models.NewsMessage.objects.filter(text__contains=request.data.get('text')).all()
        ser = WX_indexModelSerializer(instance=newlist,many=True)
        print(ser.data)
        return Response({"list":ser.data,"asdf":200})

class top_search(APIView):
    def get(self, request, *args, **kwargs):
        newlist=models.NewsMessage.objects.all()
        print(newlist)
        for ones in newlist:
            models.NewsMessage.objects.filter(time_TS=ones.time_TS,type_text=ones.type_text).update(heat_num = ones.favor_count + ones.viewer_count - ones.report_num)
        getheat = models.NewsMessage.objects.all().order_by("-heat_num")[0:5]
        for x in getheat:
            print(x.heat_num)
        ser = WX_indexModelSerializer(instance=getheat,many=True)
        return Response({"list": ser.data,"asdf": 200})
