from save_spacy import SaveSpacy
import spacy

save_spacy = SaveSpacy()

nlp = spacy.load("en_core_web_sm")

save_spacy.save_model_local(nlp, "config/path/cfg.pkl", "model/path/model.pkl")