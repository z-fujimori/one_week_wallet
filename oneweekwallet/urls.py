"""
    oneweekwalletプロジェクトのURL設定。

    urlpatterns` リストは URL をビューにルーティングします。詳しくは
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
    例を参照してください：
    機能ビュー
        1. インポートを追加する: from my_app import views
        2. URL を urlpatterns に追加する: path('', views.home, name='home')
    クラスベースのビュー
        1. インポートの追加: from other_app.views import Home
        2. URL を urlpatterns に追加: path('', Home.as_view(), name='home')
    別の URLconf を含める
        1. include() 関数をインポートします: from django.urls import include, path
        2. URL を urlpatterns に追加します: path(『blog/』, include(『blog.urls』))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("expenses.urls")),
    path("account/", include("accounts.urls")),
    path("admin/", admin.site.urls),
]
