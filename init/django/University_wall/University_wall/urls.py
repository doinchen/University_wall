"""University_wall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.static import serve
from django.conf import settings
from app01 import views
from django.urls import re_path as url
from django.conf.urls.static import static # 添加本行
from django.conf import settings # 添加本行
urlpatterns = [



    url(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    #path('admin/', admin.site.urls),
    path('layout/', views.layout),
    path('login/', views.login),
    path('logout/', views.logout),

    path('index/', views.index),

    path('admin/list/', views.admin_list),
    path('admin/add/', views.admin_add),
    path('admin/<int:nid>/edit/', views.admin_edit),
    path('admin/<int:nid>/editpwd/', views.admin_editpwd),
    path('admin/<int:nid>/delete/', views.admin_delete),


    path('user/list/',views.user_list),
    path('user/add/', views.user_add),
    path('user/upload/',views.user_upload),
    path('user/<int:nid>/edit/', views.user_edit),
    path('user/<int:nid>/delete/', views.user_delete),


    path('audit/list/', views.audit_list),
    path('audit/<int:nid>/detail/', views.audit_detail),
    path('audit/<int:nid>/baidu/', views.audit_baidu),
    path('audit/<int:nid>/pass/', views.audit_pass),
    path('audit/<int:nid>/del/', views.audit_del),

    path('manage/list/', views.manage_list),









#APT
    url(r'^api/',include('api.urls')),#路由分发


    #
    #
    # path('add/admin/', views.add_admin),
    # path('delete/', views.delete),

    #path('english/', include('api.urls')),
]

              #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
