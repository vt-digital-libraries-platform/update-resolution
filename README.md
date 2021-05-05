# update-resolution-table

Update resolution records in Mint table based on NOID

## Deploy the dlp-access-lambdas application using CloudFormation stack

### Through a Launch stack URL

#### Step 1: Launch CloudFormation stack
[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=updateResolution&templateURL=https://vtdlp-dev-cf.s3.amazonaws.com/32270c4e6515edae09e4bd8acdc81d58.template)

Click **Next** to continue

#### Step 2: Specify stack details

| Name | Description |
|----------|:-------------:|
| Stack name | any valid name |
| Collection_Category | IAWA |
| Collection_Table | DynamoDB collection table name |
| Archive_Table | DynamoDB archive table name |
| Mint_Table | DynamoDB mint table name |
| NOID_NAA | 53696 |
| NOID_Scheme | ark:/ |
| REGION | us-east-1 |
| LONG_URL_Path | https://iawa.lib.vt.edu/ |
| SHORT_URL_Path | http://idn.lib.vt.edu/ |
| API_Key | API Key for mint|
| API_Endpoint | https://xxxx.execute-api.us-east-1.amazonaws.com/Prod/ |

#### Step 3: Configure stack options
Click **Next** to continue

#### Step 4: Review
**Check** all checkboxes under *Capabilities and transforms*

Click **Create stack**

### Through AWS CLI
```
wget https://vtdlp-dev-cf.s3.amazonaws.com/32270c4e6515edae09e4bd8acdc81d58.template -O updateResolutinLambas.template

aws cloudformation deploy --template-file updateResolutinLambas.template --stack-name demo --parameter-overrides 'CollectionCategory=RepoType CollectionTable=CollectionTableName ArchiveTable=ArchiveTableName MintTable=MintTableName NOIDNAA=53696 NOIDScheme=ark:/ Region=us-east-1  LongURLPath=LongURLPath ShortURLPath=ShortURLPath APIKey=APIKey APIEndpoint=APIEndpoint' --capabilities CAPABILITY_IAM --region us-east-1
```


## Deploy the dlp-access-lambdas application using SAM CLI

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build the application for the first time, run the following in your shell:
```bash
sam build --use-container
```
Above command will build the source of the application. The SAM CLI installs dependencies defined in `requirements.txt`, creates a deployment package, and saves it in the `.aws-sam/build` folder.

To package the application, run the following in your shell:
```bash
sam package --output-template-file packaged.yaml --s3-bucket BUCKETNAME
```
Above command will package the application and upload it to the S3 bucket you specified.

Run the following in your shell to deploy the application to AWS:
```bash
sam deploy --template-file packaged.yaml --stack-name STACKNAME --s3-bucket BUCKETNAME --parameter-overrides 'CollectionCategory=RepoType CollectionTable=CollectionTableName ArchiveTable=ArchiveTableName MintTable=MintTableName NOIDNAA=53696 NOIDScheme=ark:/ Region=us-east-1  LongURLPath=LongURLPath ShortURLPath=ShortURLPath APIKey=APIKey APIEndpoint=APIEndpoint' --capabilities CAPABILITY_IAM --region us-east-1
```

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.

## Run the dlp-access-lambdas lamdba function through bash
```bash
aws lambda invoke --function-name LambdaFunctioName out --log-type Tail --query 'LogResult' --output text |  base64 -d
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name StackName
```
