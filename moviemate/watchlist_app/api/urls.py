from django.urls import path, include
#from watchlist_app.api.views import movie_list, movie_details
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import (WatchDetailAV, WatchListAV, StreamPlatformAV, ReviewListAV, ReviewDetailAV, ReviewCreateAV, UserReview, WatchListGV)

router = DefaultRouter()
router.register('stream', StreamPlatformAV, basename='streamplatform')


urlpatterns = [
    path("list/", WatchListAV.as_view(), name="movie-list"),
    path("<int:pk>", WatchDetailAV.as_view(), name="movie-details"),
    path("list2/", WatchListGV.as_view(), name="watch-list"),
    
    path('', include(router.urls)),
    
    # path("stream/", StreamPlatformAV.as_view(), name="stream"),
    # path("stream/<int:pk>", StreamPlatformDetailAV.as_view(), name="streamplatform-detail"),
    
    path("<int:pk>/review/", ReviewListAV.as_view(), name="review-list"),
    path("<int:pk>/review-create/", ReviewCreateAV.as_view(), name="review-create"),
    path("review/<int:pk>/", ReviewDetailAV.as_view(), name="review-detail"),
    path("reviews/", UserReview.as_view(), name="user-review-detail")
    
]