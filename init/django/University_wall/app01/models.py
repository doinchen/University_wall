from django.db import models
from django.core.validators import validate_comma_separated_integer_list
# Create your models here.
class Administrtor (models.Model):
    admin_id = models.CharField(verbose_name="账号",max_length=32)
    password = models.CharField(verbose_name="密码",max_length=64)
    naminate_privilege = models.IntegerField(verbose_name="任命",null=True,blank=True)          #任命
    add_user_privilege = models.BooleanField(verbose_name="添加用户",max_length=32, null=True, blank=True)         #添加用户
    manage_user_privilege = models.BooleanField(verbose_name="管理用户",max_length=32, null=True, blank=True)       #管理用户
    manage_message_privilege = models.BooleanField(verbose_name="管理信息",max_length=32, null=True, blank=True)        #管理信息
    audit_privilege = models.BooleanField(verbose_name="审核",max_length=32, null=True, blank=True)                 #审核
class Campus (models.Model):
    title = models.CharField(verbose_name="校区",max_length=64)
    def __str__(self):
        return self.title

class Department(models.Model):
    title = models.CharField(verbose_name="院系", max_length=64)
    def __str__(self):
        return self.title

class Profession(models.Model):
    title = models.CharField(verbose_name="专业", max_length=64)
    def __str__(self):
        return self.title
class UserLevel(models.Model):
    title=models.CharField(verbose_name="层次", max_length=64)
    def __str__(self):
        return self.title

class UserInfo(models.Model):
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )

    id = models.CharField(verbose_name = "用户ID",max_length=64,primary_key=True)
    username = models.CharField(verbose_name = "用户名", max_length=32,null=True, blank=True)
    avatarurl = models.ImageField(verbose_name = "头像", upload_to="user",max_length=128,null=True, blank=True)
    name = models.CharField(verbose_name = "姓名", max_length=32)
    gender = models.SmallIntegerField(verbose_name="性别",choices=gender_choices)
    age = models.IntegerField(verbose_name = "年龄")
    student_number = models.CharField(verbose_name = "学号", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    campus = models.ForeignKey(verbose_name="校区",to="Campus", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(verbose_name="院系",to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)
    profession = models.ForeignKey(verbose_name="专业",to="Profession", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)
    #create_time = models.DateTimeField(verbose_name = "入学时间" )
    create_time = models.DateField(verbose_name = "入学时间" )
    #level = models.SmallIntegerField(verbose_name="层次",choices=level_choices)
    level = models.ForeignKey(verbose_name="层次", to="UserLevel", to_field="id", null=True, blank=True,on_delete=models.SET_NULL)

class Task(models.Model):
    # id = models.CharField(primary_key=True,max_length=64)
    stu_id=models.CharField(verbose_name = "用户ID",max_length=64,null=True)
    text = models.CharField(null=True,max_length=255)
    # image = models.CharField(null=True,max_length=255)  # 使用ImageField upload_to必不可少
    # video = models.CharField(null=True,max_length=255)
    create_time = models.DateTimeField(max_length=128,null=True)
    hide = models.CharField(max_length=255, null=True)
    time_TS = models.CharField(verbose_name="时间标志位", max_length=128, null=True, blank=True)


# Create your models here.
class UserAvatar(models.Model):
    student_id=models.CharField(verbose_name = "用户ID",max_length=64)
    name=models.CharField(verbose_name = "用户ID",max_length=64)
    username=models.CharField(verbose_name = "用户ID",max_length=64)
    avatarurl=models.CharField(verbose_name = "用户ID",max_length=64)
class NewsMessage(models.Model):
    #id = models.CharField(verbose_name = "用户ID",max_length=64,primary_key=True)
    #username = models.CharField(verbose_name="用户名", max_length=32, null=True, blank=True)
    user = models.ForeignKey(verbose_name="用户关联_id", to="UserInfo", to_field="id",null=True, blank=True,on_delete=models.SET_NULL)
    student_number = models.CharField(verbose_name="学号", max_length=32, null=True, blank=True)
    #avatarurl = models.CharField(verbose_name="头像",  max_length=128, null=True, blank=True)
    campus = models.ForeignKey(verbose_name="校区", to="Campus", to_field="id", null=True, blank=True,on_delete=models.SET_NULL)
    department = models.ForeignKey(verbose_name="院系", to="Department", to_field="id", null=True, blank=True,on_delete=models.SET_NULL)
    profession = models.ForeignKey(verbose_name="专业", to="Profession", to_field="id", null=True, blank=True,on_delete=models.SET_NULL)
    create_time = models.DateTimeField(verbose_name="发布时间")
    admin_hide = models.CharField(verbose_name="后台", max_length=32, null=True, blank=True)
    user_hide = models.CharField(verbose_name="用户", max_length=32, null=True, blank=True)
    type = models.CharField(verbose_name="类型", max_length=32, null=True, blank=True)
    text = models.CharField(verbose_name="文本内容", max_length=255, null=True, blank=True)
    type_text = models.CharField(verbose_name="多媒体内容", max_length=255, null=True,blank=True)
    favor_count=models.PositiveIntegerField(verbose_name="赞数",default=0)
    viewer_count = models.PositiveIntegerField(verbose_name="浏览数", default=0)
    comment_count = models.PositiveIntegerField(verbose_name="评论数", default=0)
    report_num = models.PositiveIntegerField(verbose_name="举报数", default=0)
    heat_num = models.PositiveIntegerField(verbose_name="热度", default=0)
    time_TS = models.CharField(verbose_name="时间标志位", max_length=128, null=True, blank=True)
class Admin_send(models.Model):
    title = models.CharField(verbose_name="是否开启AI审核", max_length=32, null=True, blank=True)
    title_type = models.CharField(verbose_name="类型", max_length=32, null=True, blank=True)


class CommentRecord(models.Model):
    news_TS = models.CharField(verbose_name="根新闻TS", max_length=32, null=True, blank=True)
    news_ustu = models.CharField(verbose_name="根新闻stu", max_length=32, null=True, blank=True)
    content_text = models.CharField(verbose_name="评论内容", max_length=32, null=True, blank=True)
    user = models.ForeignKey(verbose_name="用户关联_id",related_name="userinfo_user",max_length=32, to="UserInfo", to_field="id",null=True, blank=True,on_delete=models.SET_NULL)
    re_user = models.ForeignKey(verbose_name="回复用户关联_id",related_name="userinfo_reuser",max_length=32, to="UserInfo", to_field="id",null=True, blank=True,on_delete=models.SET_NULL)
    depth = models.CharField(verbose_name="评论等级", max_length=32, null=True, blank=True)
    root_id = models.CharField(verbose_name="根评论id", max_length=32, null=True, blank=True)
    type = models.CharField(verbose_name="类型", max_length=32, null=True, blank=True)
    time_TS = models.CharField(verbose_name="时间标志位", max_length=128, null=True, blank=True)
    create_time = models.DateTimeField(verbose_name="发布时间")
    favor_count = models.PositiveIntegerField(verbose_name="赞数", default=0)
    viewer_count = models.PositiveIntegerField(verbose_name="浏览数", default=0)
    comment_count = models.PositiveIntegerField(verbose_name="评论数", default=0)
    report_num = models.PositiveIntegerField(verbose_name="举报数", default=0)
    read = models.CharField(verbose_name="已读回执",max_length=164, null=True, blank=True,default="False")



class Detail_favor(models.Model):
    news_TS = models.CharField(verbose_name="根新闻TS", max_length=32, null=True, blank=True)
    news_ustu = models.CharField(verbose_name="根新闻stu", max_length=32, null=True, blank=True)
    user =  models.ForeignKey(verbose_name="用户关联_id",max_length=32, to="UserInfo", to_field="id",null=True, blank=True,on_delete=models.SET_NULL)
    yes_or_no = models.CharField(verbose_name="根新闻stu", max_length=32, null=True, blank=True)
    create_time = models.DateTimeField(verbose_name="发布时间",max_length=128, null=True, blank=True)
    time_TS = models.CharField(verbose_name="时间标志位", max_length=128, null=True, blank=True)
    whether_read = models.CharField(verbose_name="根新闻stu", max_length=32, null=True, blank=True)



class Detail_viewer(models.Model):
    news_TS = models.CharField(verbose_name="根新闻TS", max_length=32, null=True, blank=True)
    news_ustu = models.CharField(verbose_name="根新闻stu", max_length=32, null=True, blank=True)
    user = models.ForeignKey(verbose_name="用户关联_id", max_length=32, to="UserInfo", to_field="id", null=True,blank=True, on_delete=models.SET_NULL)
    create_time = models.DateTimeField(verbose_name="发布时间", max_length=128, null=True, blank=True)
    time_TS = models.CharField(verbose_name="时间标志位", max_length=128, null=True, blank=True)
class Comment_favor(models.Model):
    news_TS = models.CharField(verbose_name="根新闻TS", max_length=32, null=True, blank=True)
    news_ustu = models.CharField(verbose_name="根新闻stu", max_length=32, null=True, blank=True)

    user = models.ForeignKey(verbose_name="用户关联_id",max_length=32, to="UserInfo", to_field="id",null=True, blank=True,on_delete=models.SET_NULL)
    depth = models.CharField(verbose_name="评论等级", max_length=32, null=True, blank=True)
    comment_id = models.CharField(verbose_name="根评论id", max_length=32, null=True, blank=True)

    time_TS = models.CharField(verbose_name="时间标志位", max_length=128, null=True, blank=True)
    create_time = models.DateTimeField(verbose_name="发布时间",max_length=128, null=True, blank=True)
    yes_or_no = models.CharField(verbose_name="根新闻stu", max_length=32, null=True, blank=True)
    whether_read = models.CharField(verbose_name="根新闻stu", max_length=32, null=True, blank=True)

class message(models.Model):
    user = models.ForeignKey(verbose_name="用户关联_id",related_name="mess_user",max_length=32, to="UserInfo", to_field="id",null=True, blank=True,on_delete=models.SET_NULL)
    re_user = models.ForeignKey(verbose_name="回复用户关联_id",related_name="mess_reuser",max_length=32, to="UserInfo", to_field="id",null=True, blank=True,on_delete=models.SET_NULL)
    message = models.CharField(verbose_name="消息内容", max_length=128, null=True, blank=True)
    type = models.CharField(verbose_name="类型", max_length=32, null=True, blank=True)
    time_TS = models.CharField(verbose_name="时间标志位", max_length=128, null=True, blank=True)
    create_time = models.DateTimeField(verbose_name="发布时间",max_length=128, null=True, blank=True,default=0)
    room_num = models.CharField(verbose_name="已读回执",max_length=164, null=True, blank=True,default="False")
    read = models.CharField(verbose_name="已读回执",max_length=164, null=True, blank=True,default="False")


class Fans_Blogger(models.Model):
    fans = models.ForeignKey(verbose_name="用户关联_id",related_name="userinfo_fans",max_length=32, to="UserInfo", to_field="id",null=True, blank=True,on_delete=models.SET_NULL)
    Blogger = models.ForeignKey(verbose_name="回复用户关联_id",related_name="userinfo_Blogger",max_length=32, to="UserInfo", to_field="id",null=True, blank=True,on_delete=models.SET_NULL)
class room(models.Model):
    room_num = models.CharField(verbose_name="已读回执",max_length=164, null=True, blank=True,default="False")
    member = models.CharField(verbose_name="已读回执",max_length=164, null=True, blank=True,default="False")
