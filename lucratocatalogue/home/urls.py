from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('index', views.index, name='index'),
    path('items', views.items, name='items'),
    path('selected_items', views.selected_items, name='selected_items'),
    path('details/<int:item_id>/', views.details, name='details'),
    path('search', views.search, name='search'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
