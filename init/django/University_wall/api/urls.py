from api import views
from django.urls import re_path as url
urlpatterns = [
#


    url(r'^logined/',views.Logined.as_view()),

    url(r'^login/',views.LoginView.as_view()),
    url(r'^UpLoad_avatar/',views.UpLoad_avatar.as_view()),
    url(r'^Change_username/', views.Change_username.as_view()),
    url(r'^Receive/',views.Receive.as_view()),
    url(r'^Upload_Pictures/',views.Upload_Pictures.as_view()),
    url(r'^Upload_Video/',views.Upload_Video.as_view()),
    url(r'^WX_index/',views.WX_index.as_view()),
    url(r'^WX_video_ground/',views.WX_video_ground.as_view()),
    url(r'^WX_detail/',views.WX_detail.as_view()),
    url(r'^SecondComment/',views.SecondComment.as_view()),
    url(r'^Detail_favor/',views.Detail_favor.as_view()),
    url(r'^Comment_fover/', views.Comment_fover.as_view()),
    url(r'^Fans_Blogger/', views.Fans_Blogger.as_view()),
    url(r'^Active/', views.Active.as_view()),
    url(r'^blog_once/', views.blog_once.as_view()),
    url(r'^user_US/', views.user_US.as_view()),
    url(r'^type_click/', views.type_click.as_view()),
    url(r'^room_messsage/', views.room_messsage.as_view()),
    url(r'^searchclick/', views.searchclick.as_view()),
    url(r'^top_search/', views.top_search.as_view()),





















]