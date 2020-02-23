# Cloud Functions

## Development
There are four cloud functions used by the project:
1. data: Stores fixed interval gas and temperature readings from data Pub/Sub topic to gas and temperature table hosted on cloud SQL.
2. envalert: Stores fixed interval gas and temperature readings from alerts Pub/Sub topic to env_table table hosted on cloud SQL.
3. human_detection: Get image from cloud Storage and perform machine learning on the image extracted using Cloud VisonAI
4. register: Stores device registration details from register Pub/Sub topic to device table in cloud SQL.

When developing, you can deploy a function to Cloud Functions by cd to the directory containing the function you want to deploy and run
```bash
gcloud functions deploy <function name> --runtime=python37 --trigger-topic=<topic> --entry-point=main --env-vars-file=../env.yaml
```