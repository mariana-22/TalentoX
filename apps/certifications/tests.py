from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Certification

User = get_user_model()


class CertificationModelTest(TestCase):
    """Tests para el modelo Certification"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_create_certification(self):
        """Test crear una certificación"""
        certification = Certification.objects.create(
            user=self.user,
            title='Python Básico',
            total_score=75.0,
            assessments_completed=5
        )
        self.assertEqual(str(certification), f'Python Básico - testuser (Nivel 0)')
        self.assertIsNotNone(certification.certificate_id)
    
    def test_calculate_level(self):
        """Test cálculo automático de nivel"""
        certification = Certification.objects.create(
            user=self.user,
            title='Test Cert',
            total_score=85.0
        )
        certification.calculate_level()
        self.assertEqual(certification.level, 4)  # Avanzado (75-89)
    
    def test_level_expert(self):
        """Test nivel experto"""
        certification = Certification.objects.create(
            user=self.user,
            title='Test Expert',
            total_score=95.0
        )
        certification.calculate_level()
        self.assertEqual(certification.level, 5)  # Experto (90-100)
    
    def test_is_valid_active(self):
        """Test certificación activa es válida"""
        certification = Certification.objects.create(
            user=self.user,
            title='Test Valid',
            status='active'
        )
        self.assertTrue(certification.is_valid())
    
    def test_is_valid_revoked(self):
        """Test certificación revocada no es válida"""
        certification = Certification.objects.create(
            user=self.user,
            title='Test Revoked',
            status='revoked'
        )
        self.assertFalse(certification.is_valid())


class CertificationAPITest(APITestCase):
    """Tests para los endpoints de Certification"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='apiuser',
            password='testpass123'
        )
        self.certification = Certification.objects.create(
            user=self.user,
            title='API Test Cert',
            total_score=70.0,
            assessments_completed=3
        )
    
    def test_list_certifications(self):
        """Test listar certificaciones"""
        response = self.client.get('/certifications/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_certification_detail(self):
        """Test detalle de certificación"""
        response = self.client.get(f'/certifications/{self.certification.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'API Test Cert')
    
    def test_certification_history(self):
        """Test historial de certificaciones de usuario"""
        response = self.client.get(f'/certifications/{self.user.id}/history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_certification_verify(self):
        """Test verificar certificación por UUID"""
        response = self.client.get(f'/certifications/verify/{self.certification.certificate_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_valid'])
