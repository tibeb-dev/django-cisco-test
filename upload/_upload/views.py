import os
from django.shortcuts import render, redirect
from .models import UploadedFile
import boto3
import hashlib
import base64

MIN_FILE_SIZE = 512  # 0.5KB
MAX_FILE_SIZE = 2048  # 2KB

def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']

        if uploaded_file.size < MIN_FILE_SIZE or uploaded_file.size > MAX_FILE_SIZE:
            error_message = f"File must be between 0.5KB and 2KB. Your file is {uploaded_file.size / 1024:.2f}KB."
            return render(request, 'upload/upload.html', {'error': error_message})
        
        if uploaded_file.content_type != 'text/plain':
            error_message = "File must be a text file."
            return render(request, 'upload/upload.html', {'error': error_message})
        
        file_content = uploaded_file.read().decode('utf-8')

        # Calculate MD5 checksum
        md5_hash = hashlib.md5(file_content.encode('utf-8')).digest()
        md5_base64 = base64.b64encode(md5_hash).decode('utf-8')

        # Upload to AWS S3
        s3 = boto3.client('s3')
        try:
            s3.put_object(
                Bucket=os.getenv('AWS_BUCKET_NAME'),
                Key=uploaded_file.name,
                Body=file_content,
                ContentMD5=md5_base64
            )

             # Get the full file link
            file_url = f"https://{os.getenv('AWS_BUCKET_NAME')}.s3.amazonaws.com/{uploaded_file.name}"

            # Save to UploadedFile model
            uploaded_file_record = UploadedFile(
                filename=uploaded_file.name,
                file_content=file_content,
                s3_file_path=file_url
            )
            uploaded_file_record.save()

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            print(error_message)
            return render(request, 'upload/upload.html', {'error': error_message})

        # return render(request, 'upload/upload.html', {'success': 'File uploaded successfully.'})
        return redirect('file_list')
    
    return render(request, 'upload/upload.html')

def file_list(request):
    files = UploadedFile.objects.all()
    return render(request, 'upload/file_list.html', {'files': files})
