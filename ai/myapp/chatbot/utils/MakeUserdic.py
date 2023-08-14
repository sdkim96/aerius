import os

class Userdic:
    def __init__(self, userdic='/home/azureuser/projects/aerius/ai/myapp/chatbot/dict/userdic.txt'):
        self.userdic = userdic
        if not os.path.exists(self.userdic):
            open(self.userdic, 'w').close()

        with open(self.userdic) as f:
            self.lines = [line.strip() for line in f.readlines()]

    

    def _save(self):
        with open(self.userdic, 'w') as f:
            for line in self.lines:
                f.write(line + "\n")


    def create_words(self, word, tag='NNG'):
        if isinstance(word, list):
            for w in word:
                self.lines.append(f'{w}\t{tag}')
        else:
            self.lines.append(f'{word}\t{tag}')
        self._save()


    def update_word(self, from_word, to_word, tag='NNG'):
        for i, line in enumerate(self.lines):
            if line.split("\t")[0] == from_word:
                self.lines[i] = f'{to_word}\t{tag}'
        self._save()


    def delete_word(self, word):
        if isinstance(word, list):
            for w in word:
                self.lines = [line for line in self.lines if not line.split("\t")[0] == w]
        else:
            self.lines = [line for line in self.lines if not line.split("\t")[0] == word]
        self._save()
