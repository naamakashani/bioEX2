import random
import string
MUTATION_RATE = 0.05
alphabet = string.ascii_lowercase

class Sequence:

    def __init__(self, encoded):
        shuffled_alphabet = random.sample(alphabet, len(alphabet))
        self.cipher = dict(zip(alphabet, shuffled_alphabet))

        self.decoded_sentence = ""
        for character in encoded:
            if character in self.cipher:
                self.decoded_sentence += self.cipher[character]
            else:
                self.decoded_sentence += character



    def mutate(self,encoded):
        num_of_mutation= int(MUTATION_RATE * len(self.decoded_sentence))
        for i in range(num_of_mutation):
            keys = list(self.cipher.keys())
            a, b = random.sample(keys, 2)
            # swap their values in the cipher
            self.cipher[a], self.cipher[b] = self.cipher[b], self.cipher[a]
        self.decoded_sentence = ""
        for character in encoded:
            if character in self.cipher:
                self.decoded_sentence += self.cipher[character]
            else:
                self.decoded_sentence += character





    def fitness(self, dict, letters_freq, couples_freq):
        score = 0.0
        message = self.decoded_sentence.upper()

        # Score the frequency of individual letters
        for letter in message:
            if letter in letters_freq:
                score += letters_freq[letter]

        # Score the frequency of couples of letters
        for i in range(len(message) - 1):
            pair = message[i:i + 2]
            if pair in couples_freq:
                score += couples_freq[pair]
        message.lower()
        words = message.split()
        for word in words:
            if word in dict:
                score += 5
        return score

    def check_bijection(self):
        # check that the cipher is still a bijection
        values = set()
        for value in self.cipher.values():
            if value in values:
                return False
            values.add(value)
        return True


    # def fitness(self, dict, letter_freq, pair_freq):
    #     words_in_sentence = self.decoded_sentence.split()
    #     word_score = sum(1 for word in words_in_sentence if word in dict)
    #     #letter_score = sum(letter_freq.get(letter.upper(), 0) for letter in self.decoded_sentence if letter.isalpha())
    #     #pair_score = sum(pair_freq.get(self.decoded_sentence[i:i + 2].upper(), 0) for i in range(len(self.decoded_sentence) - 1) if
    #                      #self.decoded_sentence[i:i + 2].isalpha())
    #     return word_score
