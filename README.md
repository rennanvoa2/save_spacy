# SaveSpacy
API to save / load Spacy models.

Spacy models are composed of two files. The binary model and a configuration file.

While saving / loading models from GCP make sure to have credential saved into GOOGLE_APPLICATION_CREDENTIALS. If you don't you can download the access.json file from you GCP account and run this piece of code:

```
# Set enviroment variables
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = acess_json_path
```


## Local

### load_model_local

***Load a model from local files***

config_file_path : str = Local path to load the config pickle
bytes_model_path : str = Local path to load the model pickle

### save_model_local

***Save a model to local files***

spacy_model : spacy.language = The Spacy model to save.
config_path : str = Local path to save the config pickle
model_path : str = Local path to save the model pickle


## Google Cloud Storage

### load_model_gcp

***Load a model from GCS bucket***

bucket_name : str = Name of Google Cloud Bucket to save the file.
bucket_folder : str = The folder inside the bucket to save the file. If the folder doesn't exist it will be created.
cfg_filename : str = Name of the configuration file (recommended `cfg.pkl`)
bytes_filename : str = Name of the model file (recommended `model.pkl`)

### save_model_gcp

***Save a model to local GCS bucket.***

This method first saved the model locally, then upload the files to GCS and finally remove the local files.

spacy_model : spacy.language = The spacy model to save.
bucket_name: str =  Name of Google Cloud Bucket to save the file.
bucket_folder: str = The folder inside the bucket to save the file. If the folder doesn't exist it will be created.
config_path: str = local path to save the cfg file
model_path: str = local path to save the model file