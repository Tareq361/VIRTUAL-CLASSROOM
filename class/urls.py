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
    path('class/<int:cid>',views.classView, name="classview"),
    path('pdf/<int:Mid>', views.pdfview, name="pdfView"),
    path('material/<int:Mid>', views.materialview, name="materialView"),
    path('send/',views.sendanmail,name="sendmail"),
    path('invite/',views.invite,name="invite"),
    path('review/<int:mid>',views.review,name="review"),
    path('reviewStudent/<int:rid>',views.reviewstudent,name="reviewstudent"),
    path('api/', views.apiView, name="api"),
    path('api/student/<str:pk>', views.studentlist, name="studentlist"),

    path('api/material-list/', views.materiallist, name="material-list"),
    path('api/material-post/', views.materialpost, name="material-post"),
    path('api/signIn/', views.signinInfo, name="sign-info"),
    path('api/register/', views.register, name="register"),
    path('api/join/', views.joinClass, name="Join"),
    path('api/createClass/', views.createClass, name="createclass"),
    path('api/classList/', views.Classlist, name="classList"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)