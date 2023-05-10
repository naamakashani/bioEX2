import random
import string

MUTATION_RATE = 0.05
alphabet = string.ascii_lowercase
Counter_fitness = 0


def get_counter_fitness():
    return Counter_fitness


class Sequence:
    def __init__(self, encoded, cipher):
        self.score = 0.0
        if cipher is None:
            # create a random solution
            shuffled_alphabet = random.sample(alphabet, len(alphabet))
            # the cipher is a dictionary that maps each letter to another letter.
            self.cipher = dict(zip(alphabet, shuffled_alphabet))
        else:
            self.cipher = cipher
        # decode the message using the cipher
        self.decoded_words = []
        for word in encoded:
            decoded_word = ""
            for letter in word:
                if letter in self.cipher:
                    decoded_word += self.cipher[letter]
            self.decoded_words.append(decoded_word)

    def copy(self):
        # create a new Sequence object with the same encoded message and cipher
        new_sequence = Sequence(encoded=[], cipher=self.cipher.copy())
        # copy over the decoded words and fitness score
        new_sequence.decoded_words = self.decoded_words.copy()
        new_sequence.score = self.score
        return new_sequence

    def mutate(self, encoded):
        num_of_mutation = int(MUTATION_RATE * len(self.cipher))
        for i in range(num_of_mutation):
            keys = list(self.cipher.keys())
            a, b = random.sample(keys, 2)
            # swap their values in the cipher
            self.cipher[a], self.cipher[b] = self.cipher[b], self.cipher[a]

        self.decoded_words = []
        for word in encoded:
            decoded_word = ""
            for letter in word:
                if letter in self.cipher:
                    decoded_word += self.cipher[letter]
            self.decoded_words.append(decoded_word)

    def fitness(self, dict, letters_freq, couples_freq):
        score = 0.0
        global Counter_fitness
        Counter_fitness += 1
        # Score the frequency of individual letters
        for word in self.decoded_words:
            for letter in word:
                if letter.upper() in letters_freq:
                    score += letters_freq[letter.upper()]

        # Score the frequency of couples of letters
        for word in self.decoded_words:
            for i in range(len(word) - 1):
                pair = word[i:i + 2]
                if pair.upper() in couples_freq:
                    score += couples_freq[pair.upper()]
        dict_copy = dict.copy()
        for word in self.decoded_words:
            if word in dict_copy:
                dict_copy.remove(word)
                score += len(word)
        self.score = score
        return score
