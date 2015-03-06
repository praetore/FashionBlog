from boto.exception import S3ResponseError
from boto.s3.connection import Location, S3Connection
from boto.s3.cors import CORSConfiguration
from app import app

__author__ = 'darryl'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def store_image(file):
    bucket = retrieve_bucket()
    app.logger.info('Handling request')
    if allowed_file(file.filename):
        # Create key in bucket
        key = bucket.new_key(file.filename)
        app.logger.info('Creating key')
        file.seek(0)
        key.set_contents_from_file(file)
        app.logger.info('Key set')
        key.make_public()
        key.set_metadata(
            'Content-Type', 'image/' + file.filename.split('.')[-1].lower()
        )


def get_image(filename):
    bucket = retrieve_bucket()
    key = bucket.get_key(filename)
    url = key.generate_url(3000, query_auth=False, force_http=True)
    return url


def delete_image(filename):
    bucket = retrieve_bucket()
    bucket.delete_key(filename)


def retrieve_bucket():
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


def list_images():
    bucket = retrieve_bucket()
    return [k.name for k in bucket.list()]