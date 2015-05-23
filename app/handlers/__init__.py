import abc
import os

from boto.exception import S3ResponseError
from boto.s3.connection import Location, S3Connection
from boto.s3.cors import CORSConfiguration
from werkzeug.utils import secure_filename

from app import app


__author__ = 'darryl'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


class Storage(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def store_image(self, image):
        pass

    @abc.abstractmethod
    def get_image(self, image):
        pass

    @abc.abstractmethod
    def delete_image(self, image):
        pass

    @abc.abstractmethod
    def list_images(self):
        pass


class LocalStorage(Storage):
    @property
    def localdir(self):
        directory = app.config["STORAGE_DIRECTORY"]
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    def store_image(self, image):
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(self.localdir, filename))

    def list_images(self):
        return [filename for filename in os.listdir(self.localdir) if allowed_file(filename)]

    def get_image(self, image):
        pass

    def delete_image(self, image):
        os.remove(os.path.join(self.localdir, image))


class S3Storage(Storage):
    @property
    def bucket(self):
        # Initialize S3
        s3 = S3Connection(
            aws_access_key_id=app.config['AWS_ACCESS_KEY'],
            aws_secret_access_key=app.config['AWS_SECRET_KEY']
        )
        app.logger.info('Connection initialized')
        # Check if bucket already exists
        try:
            bucket = s3.get_bucket(app.config['AWS_BUCKET_NAME'])
            app.logger.info('Connected to bucket')
        except S3ResponseError:
            app.logger.error('Bucket does not exist')
            bucket = s3.create_bucket(app.config['AWS_BUCKET_NAME'], location=Location.EU)
            app.logger.info('New bucket created')
            cors_cfg = CORSConfiguration()
            cors_cfg.add_rule(
                'GET',
                ['*'],
                allowed_header=['*'],
                max_age_seconds=3000,
                expose_header=['x-amz-server-side-encryption']
            )
            bucket.set_cors(cors_cfg)
            app.logger.info('Bucket configuration set')
        app.logger.info('Returning bucket')
        return bucket

    def store_image(self, image):
        bucket = self.bucket
        app.logger.info('Using bucket {} for image store'.format(self.bucket))
        app.logger.info('Handling request')
        if allowed_file(image.filename):
            # Create key in bucket
            filename = secure_filename(image.filename)
            key = bucket.new_key(filename)
            app.logger.info('Creating key')
            image.seek(0)
            key.set_contents_from_file(image)
            app.logger.info('Key set')
            key.make_public()
            key.set_metadata(
                'Content-Type', 'image/' + filename.split('.')[-1].lower()
            )
        app.logger.info('{} stored in bucket'.format(image))

    def get_image(self, image):
        bucket = self.bucket
        key = bucket.get_key(image)
        url = key.generate_url(3000, query_auth=False, force_http=True)
        return url

    def delete_image(self, image):
        bucket = self.bucket
        bucket.delete_key(image)

    def list_images(self):
        bucket = self.bucket
        return [k.name for k in bucket.list()]