from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from ..models import UploadedFile

class FileUploadViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_file_upload_view(self):
        """Test the file upload view accepts valid file size"""
        # Create a sample valid txt file to upload (1KB in size)
        valid_file = SimpleUploadedFile("valid_test.txt", b"x" * 1024)  # 1KB file

        # Perform POST request to upload the file
        response = self.client.post(reverse('upload_file'), {'file': valid_file})

        # Check that the response redirects to the file list page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('file_list'))

        # Check that the UploadedFile object was created
        uploaded_file = UploadedFile.objects.first()
        self.assertEqual(uploaded_file.filename, 'valid_test.txt')

    def test_file_upload_below_minimum_size(self):
        """Test the file upload view rejects files smaller than 0.5KB"""
        # Create a sample txt file smaller than 0.5KB (400 bytes)
        small_file = SimpleUploadedFile("small_test.txt", b"x" * 400)

        # Perform POST request to upload the small file
        response = self.client.post(reverse('upload_file'), {'file': small_file})

        # Check that the file was not uploaded (should stay on upload page with an error)
        self.assertEqual(response.status_code, 200)  # No redirect (stays on form)
        self.assertContains(response, "File must be between 0.5KB and 2KB")

        # Check that no file was added to the database
        self.assertEqual(UploadedFile.objects.count(), 0)

    def test_file_upload_above_maximum_size(self):
        """Test the file upload view rejects files larger than 2KB"""
        # Create a sample txt file larger than 2KB (2500 bytes)
        large_file = SimpleUploadedFile("large_test.txt", b"x" * 2500)

        # Perform POST request to upload the large file
        response = self.client.post(reverse('upload_file'), {'file': large_file})

        # Check that the file was not uploaded (should stay on upload page with an error)
        self.assertEqual(response.status_code, 200)  # No redirect (stays on form)
        self.assertContains(response, "File must be between 0.5KB and 2KB")

        # Check that no file was added to the database
        self.assertEqual(UploadedFile.objects.count(), 0)
