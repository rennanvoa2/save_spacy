import pickle
import spacy
import spacy_transformers
from google.cloud import storage
import os


class SaveSpacy:
    def save_model_local(
        self,
        spacy_model: spacy.language,
        config_path="cfg.pkl",
        model_path="bytes_model.pkl",
    ) -> None:
        """
        This function saves a Spacy model locally.
        Two files are going to be saved, config file and bytes model file.
        """

        config = spacy_model.config
        bytes_data = spacy_model.to_bytes()

        with open(config_path, "wb") as handle:
            pickle.dump(config, handle, protocol=4)
            print("Config file saved at:", config_path)

        with open(model_path, "wb") as handle:
            pickle.dump(bytes_data, handle, protocol=4)
            print("Bytes file saved at:", model_path)

    def load_model_local(
        self, config_file_path: str, bytes_model_path: str
    ) -> spacy.language:
        """
        This function loads a Spacy model stored locally.
        """

        with open(config_file_path, "rb") as handle:
            config_file = pickle.load(handle)

        with open(bytes_model_path, "rb") as handle:
            bytes_model = pickle.load(handle)

        lang_cls = spacy.util.get_lang_class(config_file["nlp"]["lang"])
        nlp = lang_cls.from_config(config_file)
        nlp.from_bytes(bytes_model)

        return nlp

    def load_model_gcp(
        self, gcp_folder: str, bucket: str, cfg_filename: str, bytes_filename: str,
    ) -> spacy.language:
        """
        This function loads a Spacy model stored in GCP storage bucket.
        """

        print(
            "Loading Spacy model from Google Storage. This process can take several minutes according to the size of the model."
        )

        client = storage.Client()

        bucket = client.get_bucket(bucket)

        config_str = bucket.get_blob(
            "{}/{}".format(gcp_folder, cfg_filename)
        ).download_as_string()  # Download string (config file)

        config_file = pickle.loads(config_str)  # Pickle load as string

        bytes_str = bucket.get_blob(
            "{}/{}".format(gcp_folder, bytes_filename)
        ).download_as_string()  # Download string (model file)

        bytes_model = pickle.loads(bytes_str)  # Pickle load as string

        # Load spacy model and config file to re-create the model
        lang_cls = spacy.util.get_lang_class(config_file["nlp"]["lang"])
        nlp = lang_cls.from_config(config_file)
        nlp.from_bytes(bytes_model)

        return nlp

    def save_model_gcp(
        self,
        spacy_model: spacy.language,
        bucket_name: str,
        bucket_folder: str = None,
        config_path: str = "cfg.pkl",
        model_path: str = "bytes_model.pkl",
    ) -> None:
        """
        Uploads a file to the bucket. First it will save the files locally to config and model paths. 
        Then it will upload those saved files to the choosen bucket/blob
        """

        # bucket_name = "your-bucket-name"
        # config_path = The path to your config file to upload
        # model_path = The path to your model file to upload
        # bucket_folder = Folder to save on GCP
        if bucket_folder:
            bucket_folder = bucket_folder + "/"
        else:
            bucket_folder = ""

        try:
            self.save_model_local(spacy_model, config_path, model_path)
        except:
            raise Exception(
                "Failed to save model locally. Check if cfg and model path's exist."
            )

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        try:
            blob_cfg = bucket.blob(bucket_folder+config_path)
            blob_cfg.upload_from_filename(config_path)
        except Exception as e:
            raise Exception(
                "Failed uploading cfg file to GCS. Check your if credentials are in GOOGLE_APPLICATION_CREDENTIALS env variable."
            )

        try:
            blob_model = bucket.blob(bucket_folder+model_path)
            blob_model.upload_from_filename(model_path)
        except Exception as e:
            raise Exception(
                "Failed uploading model file to GCS. Check your if credentials are in GOOGLE_APPLICATION_CREDENTIALS env variable."
            )

        try:
            os.remove(config_path)
            os.remove(model_path)
        except:
            print("Model saved corretly but the program wasn't able to remove the local files at {} and {}.".format(config_path,model_path))

        print(f"Model uploaded to {bucket_folder}.")
