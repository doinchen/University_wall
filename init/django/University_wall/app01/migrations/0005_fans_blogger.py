# Generated by Django 4.1.5 on 2023-02-24 02:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_delete_fans_blogger'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fans_Blogger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Blog', models.ForeignKey(blank=True, max_length=32, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userinfo_Blog', to='app01.userinfo', verbose_name='回复用户_id')),
                ('fans', models.ForeignKey(blank=True, max_length=32, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userinfo_fans', to='app01.userinfo', verbose_name='用户关联_id')),
            ],
        ),
    ]
