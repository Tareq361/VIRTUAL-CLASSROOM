from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name="class"
urlpatterns = [
    path('',views.home,name='home'),
    path('signup/',views.SignupView,name='signup'),
    path('signin/',views.SigninView,name='signin'),
    path('signout/',views.signoutView,name='signout'),
    path('home/', views.homeView, name="home"),
    path('create_class/',views.create_class,name="create"),
    path('join_class/',views.join_class,name="join"),
    path('inviteStudent/',views.InviteStudent,name="inviteStudent"),
    path('class/<int:cid>',views.classView, name="classview"),
    path('pdf/<int:Mid>', views.pdfview, name="pdfView"),
    path('audio/', views.Audio, name="audio"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)