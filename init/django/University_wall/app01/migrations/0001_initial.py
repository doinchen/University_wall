# Generated by Django 4.1.5 on 2023-02-24 02:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin_send',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=32, null=True, verbose_name='是否开启AI审核')),
                ('title_type', models.CharField(blank=True, max_length=32, null=True, verbose_name='类型')),
            ],
        ),
        migrations.CreateModel(
            name='Administrtor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_id', models.CharField(max_length=32, verbose_name='账号')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('naminate_privilege', models.IntegerField(blank=True, null=True, verbose_name='任命')),
                ('add_user_privilege', models.BooleanField(blank=True, max_length=32, null=True, verbose_name='添加用户')),
                ('manage_user_privilege', models.BooleanField(blank=True, max_length=32, null=True, verbose_name='管理用户')),
                ('manage_message_privilege', models.BooleanField(blank=True, max_length=32, null=True, verbose_name='管理信息')),
                ('audit_privilege', models.BooleanField(blank=True, max_length=32, null=True, verbose_name='审核')),
            ],
        ),
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='校区')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='院系')),
            ],
        ),
        migrations.CreateModel(
            name='Profession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='专业')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stu_id', models.CharField(max_length=64, null=True, verbose_name='用户ID')),
                ('text', models.CharField(max_length=255, null=True)),
                ('create_time', models.DateTimeField(max_length=128, null=True)),
                ('hide', models.CharField(max_length=255, null=True)),
                ('time_TS', models.CharField(blank=True, max_length=128, null=True, verbose_name='时间标志位')),
            ],
        ),
        migrations.CreateModel(
            name='UserAvatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=64, verbose_name='用户ID')),
                ('name', models.CharField(max_length=64, verbose_name='用户ID')),
                ('username', models.CharField(max_length=64, verbose_name='用户ID')),
                ('avatarurl', models.CharField(max_length=64, verbose_name='用户ID')),
            ],
        ),
        migrations.CreateModel(
            name='UserLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='层次')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='用户ID')),
                ('username', models.CharField(blank=True, max_length=32, null=True, verbose_name='用户名')),
                ('avatarurl', models.ImageField(blank=True, max_length=128, null=True, upload_to='user', verbose_name='头像')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('gender', models.SmallIntegerField(choices=[(1, '男'), (2, '女')], verbose_name='性别')),
                ('age', models.IntegerField(verbose_name='年龄')),
                ('student_number', models.CharField(max_length=32, verbose_name='学号')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('create_time', models.DateField(verbose_name='入学时间')),
                ('campus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app01.campus', verbose_name='校区')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app01.department', verbose_name='院系')),
                ('level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app01.userlevel', verbose_name='层次')),
                ('profession', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app01.profession', verbose_name='专业')),
            ],
        ),
        migrations.CreateModel(
            name='NewsMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_number', models.CharField(blank=True, max_length=32, null=True, verbose_name='学号')),
                ('create_time', models.DateTimeField(verbose_name='发布时间')),
                ('admin_hide', models.CharField(blank=True, max_length=32, null=True, verbose_name='后台')),
                ('user_hide', models.CharField(blank=True, max_length=32, null=True, verbose_name='用户')),
                ('type', models.CharField(blank=True, max_length=32, null=True, verbose_name='类型')),
                ('text', models.CharField(blank=True, max_length=255, null=True, verbose_name='文本内容')),
                ('type_text', models.CharField(blank=True, max_length=255, null=True, verbose_name='多媒体内容')),
                ('favor_count', models.PositiveIntegerField(default=0, verbose_name='赞数')),
                ('viewer_count', models.PositiveIntegerField(default=0, verbose_name='浏览数')),
                ('comment_count', models.PositiveIntegerField(default=0, verbose_name='评论数')),
                ('report_num', models.PositiveIntegerField(default=0, verbose_name='举报数')),
                ('time_TS', models.CharField(blank=True, max_length=128, null=True, verbose_name='时间标志位')),
                ('campus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app01.campus', verbose_name='校区')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app01.department', verbose_name='院系')),
                ('profession', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app01.profession', verbose_name='专业')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app01.userinfo', verbose_name='用户关联_id')),
            ],
        ),
        migrations.CreateModel(
            name='message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(blank=True, max_length=128, null=True, verbose_name='消息内容')),
                ('type', models.CharField(blank=True, max_length=32, null=True, verbose_name='类型')),
                ('time_TS', models.CharField(blank=True, max_length=128, null=True, verbose_name='时间标志位')),
                ('create_time', models.DateTimeField(blank=True, default=0, max_length=128, null=True, verbose_name='发布时间')),
                ('read', models.CharField(blank=True, default='False', max_length=164, null=True, verbose_name='已读回执')),
                ('re_user', models.ForeignKey(blank=True, max_length=32, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mess_reuser', to='app01.userinfo', verbose_name='回复用户关联_id')),
                ('user', models.ForeignKey(blank=True, max_length=32, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mess_user', to='app01.userinfo', verbose_name='用户关联_id')),
            ],
        ),
        migrations.CreateModel(
            name='Fans_Blogger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Blog', models.ForeignKey(blank=True, max_length=32, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userinfo_Blog', to='app01.userinfo', verbose_name='回复用户_id')),
                ('fans', models.ForeignKey(blank=True, max_length=32, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userinfo_fans', to='app01.userinfo', verbose_name='用户关联_id')),
            ],
        ),
        migrations.CreateModel(
            name='Detail_viewer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_TS', models.CharField(blank=True, max_length=32, null=True, verbose_name='根新闻TS')),
                ('news_ustu', models.CharField(blank=True, max_length=32, null=True, verbose_name='根新闻stu')),
                ('create_time', models.DateTimeField(blank=True, max_length=128, null=True, verbose_name='发布时间')),
                ('time_TS', models.CharField(blank=True, max_length=128, null=True, verbose_name='时间标志位')),
                ('user', models.ForeignKey(blank=True, max_length=32, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app01.userinfo', verbose_name='用户关联_id')),
            ],
        ),
        migrations.CreateModel(
            name='Detail_favor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_TS', models.CharField(blank=True, max_length=32, null=True, verbose_name='根新闻TS')),
                ('news_ustu', models.CharField(blank=True, max_length=32, null=True, verbose_name='根新闻stu')),
                ('yes_or_no', models.CharField(blank=True, max_length=32, null=True, verbose_name='根新闻stu')),
                ('create_time', models.DateTimeField(blank=True, max_length=128, null=True, verbose_name='发布时间')),
                ('time_TS', models.CharField(blank=True, max_length=128, null=True, verbose_name='时间标志位')),
                ('whether_read', models.CharField(blank=True, max_length=32, null=True, verbose_name='根新闻stu')),
                ('user', models.ForeignKey(blank=True, max_length=32, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app01.userinfo', verbose_name='用户关联_id')),
            ],
        ),
        migrations.CreateModel(
            name='CommentRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_TS', models.CharField(blank=True, max_length=32, null=True, verbose_name='根新闻TS')),
                ('news_ustu', models.CharField(blank=True, max_length=32, null=True, verbose_name='根新闻stu')),
                ('content_text', models.CharField(blank=True, max_length=32, null=True, verbose_name='评论内容')),
                ('depth', models.CharField(blank=True, max_length=32, null=True, verbose_name='评论等级')),
                ('root_id', models.CharField(blank=True, max_length=32, null=True, verbose_name='根评论id')),
                ('type', models.CharField(blank=True, max_length=32, null=True, verbose_name='类型')),
                ('time_TS', models.CharField(blank=True, max_length=128, null=True, verbose_name='时间标志位')),
                ('create_time', models.DateTimeField(verbose_name='发布时间')),
                ('favor_count', models.PositiveIntegerField(default=0, verbose_name='赞数')),
                ('viewer_count', models.PositiveIntegerField(default=0, verbose_name='浏览数')),
                ('comment_count', models.PositiveIntegerField(default=0, verbose_name='评论数')),
                ('report_num', models.PositiveIntegerField(default=0, verbose_name='举报数')),
                ('re_user', models.ForeignKey(blank=True, max_length=32, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userinfo_reuser', to='app01.userinfo', verbose_name='回复用户关联_id')),
                ('user', models.ForeignKey(blank=True, max_length=32, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userinfo_user', to='app01.userinfo', verbose_name='用户关联_id')),
            ],
        ),
        migrations.CreateModel(
            name='Comment_favor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_TS', models.CharField(blank=True, max_length=32, null=True, verbose_name='根新闻TS')),
                ('news_ustu', models.CharField(blank=True, max_length=32, null=True, verbose_name='根新闻stu')),
                ('depth', models.CharField(blank=True, max_length=32, null=True, verbose_name='评论等级')),
                ('comment_id', models.CharField(blank=True, max_length=32, null=True, verbose_name='根评论id')),
                ('time_TS', models.CharField(blank=True, max_length=128, null=True, verbose_name='时间标志位')),
                ('create_time', models.DateTimeField(blank=True, max_length=128, null=True, verbose_name='发布时间')),
                ('yes_or_no', models.CharField(blank=True, max_length=32, null=True, verbose_name='根新闻stu')),
                ('whether_read', models.CharField(blank=True, max_length=32, null=True, verbose_name='根新闻stu')),
                ('user', models.ForeignKey(blank=True, max_length=32, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app01.userinfo', verbose_name='用户关联_id')),
            ],
        ),
    ]
