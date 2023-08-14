from tensorflow.keras.models import Model, load_model
from tensorflow.keras import preprocessing
import tensorflow as tf
from ai.backend.settings import INTENT_MAX_SEQ_LEN

class IntentModel:
    def __init__(self, model, preprocess):
        self.model = load_model(model)
        self.p = preprocess
        if "labeled_by_9" in model:
            self.labels = {
                '제품_재고': 0, '제품_정보': 1, '제품_추천': 2, '제품_일반': 3,
                '제품_기타': 4, '결제': 5, '매장': 6, '기타': 7, 'AS': 8
            }
        else:
            self.labels={0:"확인", 1:"질문", 2:"요청", 3:"비교"}

        

    def predict_class(self, query):
        preprocessed = self.p.delete_intent_trash_tags(sentence=query)
        word, _ = self.p.divide_words_tags(preprocessed)
        sequence=[self.p.text_to_sequence(word)]

        padded_seqs = preprocessing.sequence.pad_sequences(sequence, maxlen=INTENT_MAX_SEQ_LEN, padding='post')

        predict = self.model.predict(padded_seqs)
        predict_class = tf.math.argmax(predict, axis=1).numpy()[0]
        return predict_class
    
    def predict_proba(self, query):
        preprocessed = self.p.delete_intent_trash_tags(sentence=query)
        word, _ = self.p.divide_words_tags(preprocessed)
        sequence = [self.p.text_to_sequence(word)]

        padded_seqs = preprocessing.sequence.pad_sequences(sequence, maxlen=INTENT_MAX_SEQ_LEN, padding='post')

        predict_proba = self.model.predict(padded_seqs)
        return predict_proba

        # # 인덱스를 사용하여 의도의 이름(문자열)을 가져옵니다.
        # intent_name = self.p.tokenizer.index_word.get(predict_class_index)
        # return intent_name
