from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'stream',views.StreamPlatformVS,basename="streamplatform")

urlpatterns = [
    path('list',views.WatchListAV.as_view(),name= "watchlist"),
    path('list/<int:pk>',views.WatchDetailAV.as_view(),name= "watchlist_detail"),
    path('', include(router.urls)),
    # path('platforms',views.StreamPlatformListAV.as_view(),name= "stream_platform_list"),
    # path('platforms/<int:pk>',views.StreamPlatformListAV.as_view(),name= "movie_detail"),
    # path('reviews',views.ReviewListAV.as_view(),name= "reviews"),
    # path('reviews/<int:pk>',views.ReviewDetailAV.as_view(),name= "review_detail"),
    path('list/<int:pk>/review-create',views.ReviewCreateAV.as_view(),name= "review_create"),
    path('list/<int:pk>/review',views.ReviewListAV.as_view(),name= "review"),
    path('list/review/<int:pk>',views.ReviewDetailAV.as_view(),name= "review_detail"),
    
]

# urlpatterns += router.urls
