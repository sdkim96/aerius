from konlpy.tag import Komoran
from tensorflow.keras.preprocessing.text import Tokenizer

class Preprocess:
    def __init__(self, userdic=None):

        self.k = Komoran(userdic=userdic)
        self.tokenizer = Tokenizer()
        print(userdic)
        
        self.intent_trash_tags = ['JKS', 'JKC', 'JKG', 'JKO', 'JKB', 'JKQ',
                      'JX', 'JC',
                    #   'SF', 
                      'SP', 'SS', 'SE', 'SQ',
                    #   'EP', 'EF', 'EC', 
                      'ETN','ETM',
                      'XSN', 'XSV', 'XSA']
        
        self.sense_trash_tags = [

        ]


    def delete_intent_trash_tags(self, sentence):
        pos = self.k.pos(sentence)
        preprocessed = []
        
        for p in pos:
            if p[1] in self.intent_trash_tags:
                continue
            else:
                preprocessed.append(p)

        return preprocessed
    

    def delete_sense_trash_tags(self, sentence):
        pos = self.k.pos(sentence)
        preprocessed = []

        for p in pos:
            if p[1] in self.sense_trash_tags:
                continue
            else:
                preprocessed.append(p)

        return preprocessed
                

    def divide_words_tags(self, preprocessed):
        words = []
        tags = []
        
        for s in preprocessed:
            words.append(s[0])
            tags.append(s[1])

        return words, tags
    

    def initialize_tokenizer(self, texts):
        self.tokenizer.fit_on_texts(texts)

    
    def text_to_sequence(self, text):
        return self.tokenizer.texts_to_sequences([text])[0]
