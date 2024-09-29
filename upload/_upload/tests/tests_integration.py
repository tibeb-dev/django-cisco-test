from django.test import TransactionTestCase, Client
from moto import mock_s3
import boto3
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import UploadedFile

class FileUploadIntegrationTest(TransactionTestCase):
    @mock_s3
    def setUp(self):
        self.client = Client()

        # Mock S3 setup
        self.s3 = boto3.client('s3')
        self.s3.create_bucket(Bucket='your-s3-bucket')

    @mock_s3
    def test_valid_file_upload_with_s3(self):
        """Test uploading a valid file (size between 0.5KB and 2KB) to AWS S3 and MySQL RDS"""
        # Create a valid sample file to upload (1KB)
        valid_file = SimpleUploadedFile("valid_test.txt", b"x" * 1024)

        # Perform POST request to upload the file
        response = self.client.post(reverse('upload_file'), {'file': valid_file})

        # Check that the response redirects to the file list page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('file_list'))

        # Check that the file was saved to the database
        uploaded_file = UploadedFile.objects.first()
        self.assertEqual(uploaded_file.filename, 'valid_test.txt')

        # Check that the file was uploaded to the S3 bucket
        s3_objects = self.s3.list_objects(Bucket='your-s3-bucket')
        self.assertIn('Contents', s3_objects)
        self.assertEqual(s3_objects['Contents'][0]['Key'], 'valid_test.txt')

    @mock_s3
    def test_file_too_large(self):
        """Test that a file larger than 2KB is rejected"""
        large_file = SimpleUploadedFile("large_test.txt", b"x" * 3000)  # 3KB file

        # Perform POST request to upload the large file
        response = self.client.post(reverse('upload_file'), {'file': large_file})

        # Check that the file was not uploaded (should stay on the form page)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "File must be between 0.5KB and 2KB")

        # Ensure no file was added to the database or S3
        self.assertEqual(UploadedFile.objects.count(), 0)
        s3_objects = self.s3.list_objects(Bucket='your-s3-bucket')
        self.assertNotIn('Contents', s3_objects)

    @mock_s3
    def test_file_too_small(self):
        """Test that a file smaller than 0.5KB is rejected"""
        small_file = SimpleUploadedFile("small_test.txt", b"x" * 400)  # 400 bytes

        # Perform POST request to upload the small file
        response = self.client.post(reverse('upload_file'), {'file': small_file})

        # Check that the file was not uploaded (should stay on the form page)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "File must be between 0.5KB and 2KB")

        # Ensure no file was added to the database or S3
        self.assertEqual(UploadedFile.objects.count(), 0)
        s3_objects = self.s3.list_objects(Bucket='your-s3-bucket')
        self.assertNotIn('Contents', s3_objects)
