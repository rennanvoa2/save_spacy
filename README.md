# SaveSpacy
API to save / load Spacy models.


While saving / loading models from GCP make sure to have credential saved into GOOGLE_APPLICATION_CREDENTIALS. If you don't you can download the access.json file from you GCP account and run this piece of code:

```
# Set enviroment variables
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = acess_json_path
```