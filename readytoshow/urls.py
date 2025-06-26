# readytoshow/urls.py

from django.contrib import admin
from django.urls import path, include

# 아래 3줄의 import 구문이 추가되었는지 확인해주세요.
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from safety import views as safety_views

urlpatterns = [
    path('', safety_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('safety/', include('safety.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='safety/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# 아래 부분은 개발 환경에서 사용자가 업로드한 미디어 파일을 서빙하기 위해 필요합니다.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)