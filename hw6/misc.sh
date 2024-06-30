# Mock AWS service using LocalStack

#install awc cli

# Start LocalStack in detached mode
#docker-compose up -d localstack

# Wait for LocalStack to be ready
#echo "Waiting for LocalStack to be ready..."
#while ! curl -s http://localhost:4566/health | grep "\"s3\": \"running\"" #> /dev/null; do
#  sleep 1
#done

# aws configure
# region us-east-1
# aws_access_key_id abc
# aws_secret_access_key xyz

echo "LocalStack is ready."

# Create an S3 bucket
aws --endpoint-url=http://localhost:4566 s3 mb s3://my-test-bucket

# List S3 buckets to verify
aws --endpoint-url=http://localhost:4566 s3 ls


#export INPUT_FILE_PATTERN="s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
#export OUTPUT_FILE_PATTERN="s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"

#pipenv install s3fs

#aws --endpoint-url=http://localhost:4566 s3 sync s3://my-test-bucket/ ./
