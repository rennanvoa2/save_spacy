import pickle
import spacy
import spacy_transformers
from google.cloud import storage
import os


class SaveSpacy:
    def save_model_to_files(self,spacy_model,config_path="cfg.pkl",model_path="bytes_model.pkl"):
        """
        This function saves a Spacy model locally.
        Two files are going to be saved, config file and bytes model file.
        """
        
        config = spacy_model.config
        bytes_data = spacy_model.to_bytes()
        
        with open(config_path, 'wb') as handle:
            pickle.dump(config, handle, protocol=4)
            print("Config file saved at:",config_path)

        with open(model_path, 'wb') as handle:
            pickle.dump(bytes_data, handle, protocol=4)
            print("Bytes file saved at:",model_path)
        
    def load_spacy_model_local(self,config_file_path, bytes_model_path):
        """
        This function loads a Spacy model stored locally.
        """
        
        with open(config_file_path, 'rb') as handle:
            config_file = pickle.load(handle)
            
        with open(bytes_model_path, 'rb') as handle:
            bytes_model = pickle.load(handle)
        
        lang_cls = spacy.util.get_lang_class(config_file["nlp"]["lang"])
        nlp = lang_cls.from_config(config_file)
        nlp.from_bytes(bytes_model)
        
        return nlp
    
    def load_spacy_model_gcp(self,acess_json_path, gcp_folder,bucket="neobrain-skills-extraction"):
        """
        This function loads a Spacy model stored in GCP storage bucket.
        """
        
        print("Loading Spacy model from Google Storage. This process can take several minutes according to the size of the model.")
        
        #Set enviroment variables
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = acess_json_path

        client = storage.Client()

        bucket = client.get_bucket(bucket)

        config_str = bucket.get_blob(gcp_folder+'/cfg.pkl').download_as_string() #Download string (config file)
        config_file = pickle.loads(config_str) #Pickle load as string
        
        bytes_str = bucket.get_blob(gcp_folder+'/bytes_model.pkl').download_as_string() #Download string (model file)
        bytes_model = pickle.loads(bytes_str) #Pickle load as string
        
        #Load spacy model and config file to re-create the model
        lang_cls = spacy.util.get_lang_class(config_file["nlp"]["lang"])
        nlp = lang_cls.from_config(config_file)
        nlp.from_bytes(bytes_model)
        
        return nlp
