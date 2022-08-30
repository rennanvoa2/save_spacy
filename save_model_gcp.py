from save_spacy.save_load import SaveSpacy
import spacy


save_spacy = SaveSpacy()

nlp = spacy.load("en_core_web_sm")

save_spacy.save_model_gcp(nlp,"test_indeed_bucket_neobrain","model")