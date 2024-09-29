from django.db import models

class UploadedFile(models.Model):
    filename = models.CharField(max_length=255)
    file_content = models.TextField()
    upload_timestamp = models.DateTimeField(auto_now_add=True)
    s3_file_path = models.CharField(max_length=255)

    def __str__(self):
        return self.filename
