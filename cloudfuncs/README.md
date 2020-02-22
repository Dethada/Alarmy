# Cloud Functions

To deploy cloud func, cd to the directory containing the function you want to deploy and run
```bash
gcloud functions deploy <function name> --runtime=python37 --trigger-topic=<topic> --entry-point=main --set-env-vars DB_HOST=<DB Host>,DB_USER=<DB User>,DB_PASS=<DB Password>,DB_NAME=<DB Name>
```