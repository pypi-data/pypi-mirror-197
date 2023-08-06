# Importing libraries
import boto3
import botocore
import os
import tqdm
from files_handler.folders_handler import folders_handler

class s3_handler:
    """
    Deal with files and connection to S3.
    
    :param bucket: The Bucket.
    :type bucket: string
    :param path_ref: Reference Path to manage the files and folders.
    :type path_ref: string
    """

    def __init__(self, bucket, path_ref, input_path='input', result_path='output'):
        self.access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        self.secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        self.region_name = os.environ.get('AWS_REGION_NAME')
        self.bucket = bucket
        self.path_ref = path_ref
        self.path_to_predict_images = os.path.join(path_ref, input_path)
        self.s3_client = boto3.client('s3')
        self.folders_handler = folders_handler('')

    # Get image from s3 bucket 
    def get_image_from_s3_bucket(self, s3_image_path, progress_bar=True):
        """
        Get an image from S3 passing the image path on s3 and saving on reference path + input
        
        :param s3_image_path: The s3 path of image with the image name.
        :type s3_image_path: string
        :param progress_bar: Enable progress bar for download
        :type progress_bar: boolean
    
        :return: If the image was downloaded or not.
        :rtype: boolean
        """
        try:
            self.folders_handler.verify_and_create_folder(self.path_to_predict_images, 'Creating input directory...')

            image_name = os.path.basename(s3_image_path)
            local_image_path = self.path_to_predict_images+'/'+image_name
            print(f'Downloading file: {image_name} to {self.path_to_predict_images} folder') 
            s3 = boto3.resource('s3', aws_access_key_id=self.access_key_id,  aws_secret_access_key=self.secret_access_key, region_name=self.region_name)
            bucket = s3.Bucket(self.bucket)

            if progress_bar:
                meta_data = self.s3_client.head_object(Bucket=self.bucket, Key=s3_image_path)
                total_length = int(meta_data.get('ContentLength', 0))
                with tqdm.tqdm(total=total_length, unit="B", unit_scale=True, desc=s3_image_path) as pbar:
                    bucket.download_file(s3_image_path, local_image_path, Callback=lambda bytes_transferred: pbar.update(bytes_transferred))

            else:
                bucket.download_file(s3_image_path, local_image_path)


            print(f'File Downloaded')
            return True
        
        except botocore.exceptions.ClientError as e:
            print(e)
            return False

    # Upload resulting image to s3 bucket
    def upload_image_to_s3_bucket(self, local_image_path, s3_output_path, progress_bar=True):
        """
        Upload an image to S3 passing the image path on s3 and the S3 Output Path
        
        :param local_image_path: the path of the image locally with the image name
        :type local_image_path: string
        :param s3_output_path: the path of the image on S3
        :type s3_output_path: string
        :param progress_bar: Enable progress bar for upload
        :type progress_bar: boolean
    
        :return: If the image was uploaded or not.
        :rtype: boolean
        """
        try:
            print(f'Uploading results to {s3_output_path}')
            s3 = boto3.resource('s3', aws_access_key_id=self.access_key_id,  aws_secret_access_key=self.secret_access_key, region_name=self.region_name)
            bucket = s3.Bucket(self.bucket)

            image_name = os.path.basename(local_image_path)
            print(f'Complete path: {s3_output_path}/{image_name}')

            if progress_bar:
                with tqdm.tqdm(total=os.stat(local_image_path).st_size, unit="B", unit_scale=True, desc=image_name) as pbar:
                    bucket.upload_file(local_image_path, s3_output_path+'/'+image_name, Callback=lambda bytes_transferred: pbar.update(bytes_transferred))

            else:
                bucket.upload_file(local_image_path, s3_output_path+'/'+image_name)

            return True

        except botocore.exceptions.ClientError as e:
            print(e)
            return False

    def check_if_file_exists(self, file_name, s3_path):
        """
        Check if file exists in s3 bucket
        
        :param file_name: the name of the file 
        :type file_name: string
        :param s3_path: the path of the file on S3
        :type s3_path: string
    
        :return: If the file exists or not.
        :rtype: boolean
        """
        try:
            s3 = boto3.resource('s3', aws_access_key_id=self.access_key_id,  aws_secret_access_key=self.secret_access_key, region_name=self.region_name)
            try:
                s3.Object(self.bucket, f'{s3_path}/{file_name}').load()
                return True
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    # The object does not exist.
                    return False
                else:
                    # Something else has gone wrong.
                    raise
        except botocore.exceptions.ClientError as e:
            return False
