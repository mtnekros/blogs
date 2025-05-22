
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: 'AWS::Serverless-2016-10-31'
Description: Template for ImageAnalytics lambdas

Resources:
  IAAdhocRunApi:
    Type: AWS::Serverless:Api
    Properties:
      StageName: main
      Name: IAAdhocRunAPI


  IAAdhocRunApiLambda:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: ./Ia_Lambdas
      Handler: adhoc_run_apis.handler
      MemorySize: 512
      Timeout: 300
      Role: !Ref LambdaRole
      VpcConfig:
        SecurityGroupIds:
          - !Ref SecurityGroup
        SubnetIds:
          - !Ref SubnetID1
          - !Ref SubnetID2
      Environment:
        Variables:
          SECRETS_NAME: !Ref SecretName
          REGION_NAME: !Ref RegionName
          ADHOC_RUN_CATEGORY_TRACKING_TABLE: 'developer.image_category_adhoc_run_tracking'
      Layers:
        - !Ref IALayer
      Events:
        GetApiHealthEvent:
          Type: Api
          Properties:
            Path: /health
            Method: get
            RestApiId: !Ref IAAdhocRunApi
        AddAdhocCategoryEvent:
          Type: Api
          Properties:
            Path: /categories
            Method: post
            RestApiId: !Ref IAAdhocRunApi
        GetAdhocCategoryEvent:
          Type: Api
          Properties:
            Path: /categories/{batch_id}
            Method: get
            RestApiId: !Ref IAAdhocRunApi
```
