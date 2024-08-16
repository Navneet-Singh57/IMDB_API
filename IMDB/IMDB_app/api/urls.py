from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'stream',views.StreamPlatformVS,basename="streamplatform")

urlpatterns = [
    path('list/',views.WatchListAV.as_view(),name= "watchlist"),
    path('list/<int:pk>/',views.WatchDetailAV.as_view(),name= "watchlist_detail"),
    path('', include(router.urls)),
    path('list/<int:pk>/review-create/',views.ReviewCreateAV.as_view(),name= "review_create"),
    path('list/<int:pk>/review/',views.ReviewList.as_view(),name= "review"),
    path('list/review/<int:pk>/',views.ReviewDetail.as_view(),name= "review_detail"),
    
]


