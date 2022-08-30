from save_spacy import SaveSpacy
import spacy

save_spacy = SaveSpacy()

nlp = spacy.load("en_core_web_sm")

save_spacy.save_model_gcp(nlp,"bucket_name","folder_name")