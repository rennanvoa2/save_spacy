from save_spacy import SaveSpacy

save_spacy = SaveSpacy()

nlp = save_spacy.load_model_gcp("bucket_name","folder_name","cfg.pkl","model.pkl")