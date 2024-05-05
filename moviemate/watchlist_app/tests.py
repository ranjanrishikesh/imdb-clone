from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app import models

class StreamPlatformTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(
            name="Netflix", 
            about="number 1 platform",
            website="https://www.netflix.com"
            )
        
    def test_streamplatform_create(self):
        data = {
            "name": "NetPrime",
            "about": "something something NetPrime",
            "website": "https://www.netprime.tv"
        }
        response = self.client.post(reverse('streamplatform-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_streamplatform_ind(self):
        response = self.client.get(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
class WatchListTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(
            name="Netflix", 
            about="number 1 platform",
            website="https://www.netflix.com"
            )
        
        self.watchlist = models.WatchList.objects.create(
            platform=self.stream,
            title="movie number test",
            storyline="storyline number test",
            active=True
        )
        
    
    def test_watchlist_create(self):
        data = {
            "platform": self.stream,
            "title": "movie number one",
            "storyline": "storyline number one",
            "active": True,
        }
        response = self.client.post(reverse('movie-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_watchlist_ind(self):
        response = self.client.get(reverse('movie-details', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.count(), 1)
        self.assertEqual(models.WatchList.objects.get().title, "movie number test")
        
        
class ReviewTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(
            name="Netflix", 
            about="number 1 platform",
            website="https://www.netflix.com"
            )
        
        self.watchlist = models.WatchList.objects.create(
            platform=self.stream,
            title="movie number test",
            storyline="storyline number test",
            active=True
        )
        
        self.watchlist2 = models.WatchList.objects.create(
            platform=self.stream,
            title="movie number test two",
            storyline="storyline number test",
            active=True
        )
        
        self.review = models.Review.objects.create(
            review_user = self.user,
            watchlist = self.watchlist2,
            rating = 5,
            description = "This is a test",
            active = True            
        )
        
    def test_review_create(self):
        data = {
            "review_user": self.user,
            "watchlist": self.watchlist,
            "rating": 4,
            "description": "mic test 1 2 3",
            "active": False
        }
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 2)
        
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_review_create_unauth(self):
        data = {
            "review_user": self.user,
            "watchlist": self.watchlist,
            "rating": 4,
            "description": "mic test 1 2 3",
            "active": False
        }
        self.client.force_authenticate(user=None)
        
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_review_update(self):
        data = {
            "review_user": self.user,
            "watchlist": self.watchlist,
            "rating": 3,
            "description": "mic test mic test",
            "active": False
        }
        response = self.client.put(reverse('review-detail', args=(self.review.id,)), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_list(self):
        response = self.client.get(reverse('review-list', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_ind(self):
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_user(self):
        response = self.client.get('/watch/reviews/?username=' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)