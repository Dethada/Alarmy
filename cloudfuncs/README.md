# Cloud Functions

To deploy cloud func, cd to the directory containing the function you want to deploy and run
```bash
gcloud functions deploy <function name> --runtime=python37 --trigger-topic=<topic> --entry-point=main --env-vars-file=../env.yaml
```