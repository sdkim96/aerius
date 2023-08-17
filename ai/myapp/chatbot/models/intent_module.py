from tensorflow.keras.models import Model, load_model
from tensorflow.keras import preprocessing
import tensorflow as tf
from ai.backend.settings import INTENT_MAX_SEQ_LEN
from tensorflow.keras.preprocessing.text import Tokenizer, tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
import json

class IntentModel:
    def __init__(self, model, preprocess, tokenizer_path):
        self.model = load_model(model)
        self.p = preprocess

        with open(tokenizer_path, 'r', encoding='utf-8') as f:
            loaded_tokenizer_json = f.read()
            self.tokenizer = self._tokenizer_from_json(loaded_tokenizer_json)

        if "labeled_by_9" in model:
            self.labels = {
                '제품_재고': 0, '제품_정보': 1, '제품_추천': 2, '제품_일반': 3,
                '제품_기타': 4, '결제': 5, '매장': 6, '기타': 7, 'AS': 8
            }
        elif "labeled_by_6" in model:
            self.labels = {
                0:"주문", 1:"배송", 2:"매장", 3:"AS", 4:"제품_정보", 5:"제품_재고"
            }
        else:
            self.labels = {0:"확인", 1:"질문", 2:"요청", 3:"비교"}

    def _tokenizer_from_json(self, json_string):
        tokenizer = tokenizer_from_json(json_string)
        return tokenizer

    def predict_class(self, query):
        preprocessed = self.p.delete_intent_trash_tags(sentence=query)
        word, _ = self.p.divide_words_tags(preprocessed)
        sequence = self.tokenizer.texts_to_sequences([' '.join(word)])
        padded_seqs = pad_sequences(sequence, maxlen=INTENT_MAX_SEQ_LEN, padding='post')

        predict = self.model.predict(padded_seqs)
        predict_class = tf.math.argmax(predict, axis=1).numpy()[0]
        return predict_class
    
    def predict_proba(self, query):
        preprocessed = self.p.delete_intent_trash_tags(sentence=query)
        word, _ = self.p.divide_words_tags(preprocessed)
        sequence = self.tokenizer.texts_to_sequences([' '.join(word)])
        padded_seqs = pad_sequences(sequence, maxlen=INTENT_MAX_SEQ_LEN, padding='post')

        predict_proba = self.model.predict(padded_seqs)
        return predict_proba
