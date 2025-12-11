"""
Tests for organizations app.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Organization, Team
from apps.users.models import User


class OrganizationModelTest(TestCase):
    """Tests for Organization model."""
    
    def setUp(self):
        """Set up test data."""
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='pass123',
            role='empresa'
        )
        self.organization = Organization.objects.create(
            name='Test Org',
            email='org@example.com',
            phone='+573001234567',
            owner=self.owner,
            size='small'
        )
    
    def test_organization_creation(self):
        """Test organization is created correctly."""
        self.assertEqual(self.organization.name, 'Test Org')
        self.assertEqual(self.organization.owner, self.owner)
        self.assertTrue(self.organization.is_active)
    
    def test_organization_str_method(self):
        """Test __str__ method."""
        self.assertEqual(str(self.organization), 'Test Org')
    
    def test_organization_total_members(self):
        """Test total_members property."""
        self.assertEqual(self.organization.total_members, 0)


class TeamModelTest(TestCase):
    """Tests for Team model."""
    
    def setUp(self):
        """Set up test data."""
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='pass123',
            role='empresa'
        )
        self.organization = Organization.objects.create(
            name='Test Org',
            email='org@example.com',
            phone='+573001234567',
            owner=self.owner
        )
        self.team = Team.objects.create(
            name='Dev Team',
            organization=self.organization,
            department='Engineering'
        )
        self.member = User.objects.create_user(
            username='member',
            email='member@example.com',
            password='pass123'
        )
        self.team.members.add(self.member)
    
    def test_team_creation(self):
        """Test team is created correctly."""
        self.assertEqual(self.team.name, 'Dev Team')
        self.assertEqual(self.team.organization, self.organization)
        self.assertTrue(self.team.is_active)
    
    def test_team_str_method(self):
        """Test __str__ method."""
        expected = 'Dev Team - Test Org'
        self.assertEqual(str(self.team), expected)
    
    def test_team_member_count(self):
        """Test member_count property."""
        self.assertEqual(self.team.member_count, 1)


class OrganizationAPITest(APITestCase):
    """Tests for Organization API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.empresa_user = User.objects.create_user(
            username='empresa',
            email='empresa@example.com',
            password='pass123',
            role='empresa'
        )
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='admin'
        )
        self.organization = Organization.objects.create(
            name='Test Org',
            email='testorg@example.com',
            phone='+573001234567',
            owner=self.empresa_user
        )
    
    def test_create_organization_as_empresa(self):
        """Test empresa user can create organization."""
        self.client.force_authenticate(user=self.empresa_user)
        url = reverse('organization-list')
        data = {
            'name': 'New Org',
            'email': 'neworg@example.com',
            'phone': '+573009876543',
            'size': 'small'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list_organizations(self):
        """Test listing organizations."""
        self.client.force_authenticate(user=self.empresa_user)
        url = reverse('organization-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_organization_members(self):
        """Test /organizations/{id}/members/ endpoint."""
        self.client.force_authenticate(user=self.empresa_user)
        url = reverse('organization-members', kwargs={'pk': self.organization.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('members', response.data)
    
    def test_get_organization_teams(self):
        """Test /organizations/{id}/teams/ endpoint."""
        self.client.force_authenticate(user=self.empresa_user)
        url = reverse('organization-teams', kwargs={'pk': self.organization.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('teams', response.data)
    
    def test_my_organizations(self):
        """Test /organizations/my_organizations/ endpoint."""
        self.client.force_authenticate(user=self.empresa_user)
        url = reverse('organization-my-organizations')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TeamAPITest(APITestCase):
    """Tests for Team API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='pass123',
            role='empresa'
        )
        self.member = User.objects.create_user(
            username='member',
            email='member@example.com',
            password='pass123',
            role='aprendiz'
        )
        self.organization = Organization.objects.create(
            name='Test Org',
            email='org@example.com',
            phone='+573001234567',
            owner=self.owner
        )
        self.team = Team.objects.create(
            name='Dev Team',
            organization=self.organization
        )
        self.team.members.add(self.member)
    
    def test_create_team(self):
        """Test creating a team."""
        self.client.force_authenticate(user=self.owner)
        url = reverse('team-list')
        data = {
            'name': 'QA Team',
            'organization': self.organization.id,
            'department': 'Quality Assurance'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_add_member_to_team(self):
        """Test /teams/{id}/add_member/ endpoint."""
        self.client.force_authenticate(user=self.owner)
        new_member = User.objects.create_user(
            username='newmember',
            email='newmember@example.com',
            password='pass123'
        )
        url = reverse('team-add-member', kwargs={'pk': self.team.id})
        data = {'user_id': new_member.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.team.members.filter(id=new_member.id).exists())
    
    def test_remove_member_from_team(self):
        """Test /teams/{id}/remove_member/ endpoint."""
        self.client.force_authenticate(user=self.owner)
        url = reverse('team-remove-member', kwargs={'pk': self.team.id})
        data = {'user_id': self.member.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.team.members.filter(id=self.member.id).exists())
    
    def test_my_teams(self):
        """Test /teams/my_teams/ endpoint."""
        self.client.force_authenticate(user=self.member)
        url = reverse('team-my-teams')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total'], 1)


class OrganizationPermissionsTest(APITestCase):
    """Tests for organization permissions."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='pass123',
            role='empresa'
        )
        self.other_user = User.objects.create_user(
            username='other',
            email='other@example.com',
            password='pass123',
            role='empresa'
        )
        self.organization = Organization.objects.create(
            name='Test Org',
            email='org@example.com',
            phone='+573001234567',
            owner=self.owner
        )
    
    def test_owner_can_update_organization(self):
        """Test owner can update their organization."""
        self.client.force_authenticate(user=self.owner)
        url = reverse('organization-detail', kwargs={'pk': self.organization.id})
        data = {'name': 'Updated Org'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_non_owner_cannot_update_organization(self):
        """Test non-owner cannot update organization."""
        self.client.force_authenticate(user=self.other_user)
        url = reverse('organization-detail', kwargs={'pk': self.organization.id})
        data = {'name': 'Hacked Org'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)