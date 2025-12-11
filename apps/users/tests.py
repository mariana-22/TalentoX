"""
Tests for users app.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import User, Profile


class UserModelTest(TestCase):
    """Tests for User model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            role='aprendiz'
        )
    
    def test_user_creation(self):
        """Test user is created correctly."""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.role, 'aprendiz')
        self.assertTrue(self.user.is_active)
    
    def test_user_full_name(self):
        """Test full_name property."""
        self.assertEqual(self.user.full_name, 'Test User')
    
    def test_user_str_method(self):
        """Test __str__ method."""
        expected = 'testuser (Aprendiz)'
        self.assertEqual(str(self.user), expected)


class ProfileModelTest(TestCase):
    """Tests for Profile model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio='Test bio',
            location='Bogotá',
            years_experience=3
        )
    
    def test_profile_creation(self):
        """Test profile is created correctly."""
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.location, 'Bogotá')
        self.assertEqual(self.profile.years_experience, 3)
    
    def test_profile_str_method(self):
        """Test __str__ method."""
        expected = 'Perfil de testuser'
        self.assertEqual(str(self.profile), expected)


class UserAPITest(APITestCase):
    """Tests for User API endpoints."""
    
    def setUp(self):
        """Set up test data and client."""
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='admin'
        )
        self.regular_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='user123',
            role='aprendiz'
        )
        Profile.objects.create(user=self.regular_user)
    
    def test_user_registration(self):
        """Test user registration endpoint."""
        url = reverse('user-list')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password2': 'newpass123',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'aprendiz'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_user_login(self):
        """Test JWT login endpoint."""
        url = reverse('token_obtain_pair')
        data = {
            'username': 'user',
            'password': 'user123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
    
    def test_get_current_user(self):
        """Test /users/me/ endpoint."""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('user-me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'user')
    
    def test_get_user_skills(self):
        """Test /users/{id}/skills/ endpoint."""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('user-skills', kwargs={'pk': self.regular_user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('skills', response.data)
    
    def test_list_users_requires_admin(self):
        """Test that listing users requires admin role."""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_admin_can_list_users(self):
        """Test that admin can list all users."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserPermissionsTest(APITestCase):
    """Tests for user permissions."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123',
            role='aprendiz'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123',
            role='aprendiz'
        )
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='admin'
        )
    
    def test_user_can_update_own_profile(self):
        """Test user can update their own profile."""
        self.client.force_authenticate(user=self.user1)
        url = reverse('user-detail', kwargs={'pk': self.user1.id})
        data = {'first_name': 'Updated'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_cannot_update_other_profile(self):
        """Test user cannot update another user's profile."""
        self.client.force_authenticate(user=self.user1)
        url = reverse('user-detail', kwargs={'pk': self.user2.id})
        data = {'first_name': 'Updated'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_admin_can_update_any_profile(self):
        """Test admin can update any user's profile."""
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-detail', kwargs={'pk': self.user1.id})
        data = {'first_name': 'Admin Updated'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)