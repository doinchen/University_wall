import re
from app01 import models

def Check(TS,stu_id):

    #print('check',TS,stu_id)

    mess_type = models.NewsMessage.objects.filter(time_TS=TS,type_text=stu_id).get().type
    #print(mess_type)
    admin_hide = models.NewsMessage.objects.filter(time_TS=TS,type_text=stu_id).get().admin_hide
    #print(admin_hide)

    if mess_type == 'text':

        print('text格式')
        if admin_hide == '1':
            models.NewsMessage.objects.filter(time_TS=TS, type_text=stu_id).update(admin_hide ='True')
            models.Task.objects.filter(time_TS=TS, stu_id=stu_id).update(hide ='True')
        else:

            models.NewsMessage.objects.filter(time_TS=TS, type_text=stu_id).update(admin_hide='False')
            models.Task.objects.filter(time_TS=TS, stu_id=stu_id).update(hide='False')

    elif mess_type == 'image':
        imglength = 0
        print('image格式')
        if admin_hide == '1':
            image_list = models.Task.objects.filter(time_TS=TS, stu_id=stu_id).all()
            # print('自动审核', len(image_list))
            if len(image_list)==0:
                # print('列表为空')
                return
            for one in image_list:
                # print('image_list',one.hide)
                # print(one.id)
                # print(one.text)
                if one.hide == '1':

                    models.Task.objects.filter(id=one.id,time_TS=TS, stu_id=stu_id).update(hide='True')
                    imglength = imglength +1
                else:
                    models.Task.objects.filter(time_TS=TS, stu_id=stu_id).update(hide='False')
            if imglength == len(image_list):
                models.NewsMessage.objects.filter(time_TS=TS, type_text=stu_id).update(admin_hide ='True')
            else:
                models.NewsMessage.objects.filter(time_TS=TS, type_text=stu_id).update(admin_hide='False')

        else:
            models.NewsMessage.objects.filter(time_TS=TS, type_text=stu_id).update(admin_hide='False')






    elif mess_type == 'video':
        print('video格式')
        global videolen
        videolen= 0
        if admin_hide == '1':
            video_list = models.Task.objects.filter(time_TS=TS, stu_id=stu_id).all()
            # print('自动审核', len(video_list))
            if len(video_list) < 2:
                # print('列表为空')
                return
            for video_one in video_list:
                print('image_list',video_one.hide)
                # print(video_one.id)
                # print(video_one.text)
                if video_one.hide == '1':

                    videolen = videolen + 1
                else:
                    return





            # print(videolen,len(video_list))
            if videolen == len(video_list):
                #print('7777777777777777777777777777777777777777777777777')
                for video_one in video_list:
                    if video_one.hide == '1':
                        models.Task.objects.filter(id=video_one.id, time_TS=video_one.time_TS, stu_id=video_one.stu_id).update(hide='True')
                    else:
                        models.Task.objects.filter(id=video_one.id, time_TS=video_one.time_TS,stu_id=video_one.stu_id).update(hide='False')
                models.NewsMessage.objects.filter(time_TS=TS, type_text=stu_id).update(admin_hide ='True')
            else:

                models.NewsMessage.objects.filter(time_TS=TS, type_text=stu_id).update(admin_hide='False')
        else:
            models.NewsMessage.objects.filter(time_TS=TS, type_text=stu_id).update(admin_hide='False')



def AutoTS(create):
    pattern = re.compile('[0-9]\d*')
    TS = ""
    for s in pattern.findall(create):
        TS = TS + s

    return TS





