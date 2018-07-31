import random

class alexify():
    
    word_list = []
    word_list_len = 0
    
    list_last_randoms = []
    
    __instanceCount = 0
    __silent = True
        
    def __init__(self, silent=True):
        self.__instanceCount += 1
        self.__silent = silent
        self.__pprint("Creating an instance Nr.: " + str(self.__instanceCount) + " of alexify()")
        
    def __pprint(self, str_text):
        if not self.__silent:
            print(str_text)        

    def update_last_randoms(self, int_random_nr = 0, ran_lst_len = 10):
        self.list_last_randoms.append(int_random_nr)
        if len(self.list_last_randoms) > ran_lst_len:
            self.list_last_randoms.pop(0)

    def generate_word_list_index(self):
        curr_rand = random.randint(1,self.word_list_len)
        if curr_rand not in self.list_last_randoms:
            self.update_last_randoms(curr_rand)
            return curr_rand
        else:
            curr_rand = self.generate_word_list_index()
            return curr_rand

    def load_text(self, str_path_to_txt):
        self.__pprint("Loading and splitting text into tokens...")
        with open(str_path_to_txt) as f:
            text = f.read()
        self.word_list = text.split("\n")
        self.word_list_len = len(self.word_list) - 1
        self.__pprint("Max index of word list is: " + str(self.word_list_len))
        return self.word_list_len

    def generate_sentence(self, int_min_sent_length = 2, int_max_sent_length = 20):
        current_sent_length = random.randint(int_min_sent_length, int_max_sent_length)
        output_sentence = ""
        for a in range(0, current_sent_length):
            output_sentence += self.word_list[self.generate_word_list_index()] + " "
        return output_sentence.strip()