from tensorflow.keras.models import Model, load_model
from tensorflow.keras import preprocessing
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer, tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
import json

class NerModel:
    def __init__(self, model, preprocess, tokenizer_path):
        self.model = load_model(model)
        self.p = preprocess

        with open(tokenizer_path, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
            self.my_tokenizer = loaded_data  # directly assign the loaded dictionary


        self.labels={
            'PAD': 0, 'B-TI': 1, 'O': 2, 'B-LOCATION': 3, 'B-PRODUCT': 4, 'B-SIZE': 5
        }


    def predict_class(self, query):
        preprocessed = self.p.delete_intent_trash_tags(sentence=query)
        word, _ = self.p.divide_words_tags(preprocessed)
        
        q2v = []
        print(word)
        for w in word:
            if w in self.my_tokenizer:
                q2v.append(self.my_tokenizer[w])
            else:
                q2v.append(1)  # Assuming 1 is the "UNK" token in your tokenizer dictionary

        print([q2v])
        padded_seqs = pad_sequences([q2v], maxlen=95, padding='post')
        print([padded_seqs])
        predict = self.model.predict(padded_seqs)
        predict_class = tf.math.argmax(predict, axis=1).numpy()[0]
        return predict_class
    
    def predict_proba(self, query):
        preprocessed = self.p.delete_intent_trash_tags(sentence=query)
        word, _ = self.p.divide_words_tags(preprocessed)
        
        q2v = []
        for w in word:
            if w in self.my_tokenizer:
                q2v.append(self.my_tokenizer[w])
            else:
                q2v.append(1)  # Assuming 1 is the "UNK" token in your tokenizer dictionary

        padded_seqs = pad_sequences([q2v], maxlen=95, padding='post')

        predict_proba = self.model.predict(padded_seqs)
        return predict_proba
