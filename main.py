import math
from sequence import *

MUTATION_RATE = 0.05
alphabet = string.ascii_lowercase
POPULATION_SIZE = 5000
NUM_GENERATIONS = 100


def open_freq_files():
    letter_freq = {}
    couples_freq = {}
    dict = []
    with open('Letter_Freq.txt', 'r') as f:
        for line in f.readlines():
            freq, letter = line.strip().split('\t')
            letter_freq[letter] = float(freq)

    with open('Letter2_Freq.txt', 'r') as f:
        for line in f.readlines():
            stripped_line = line.strip()
            if stripped_line == "":
                break
            else:
                freq, couple = stripped_line.split('\t')
                couples_freq[couple] = float(freq)

    with open('dict.txt', 'r') as f:
        for line in f:
            stripped_line = line.strip()
            if len(stripped_line) > 1:
                dict.append(stripped_line)
    return dict, letter_freq, couples_freq


def crossover(parent1, parent2):
    midpoint = random.randint(0, len(parent1.decoded_sentence))
    s1_left, s2_right = parent1.decoded_sentence[:midpoint], parent2.decoded_sentence[midpoint:]
    child = s1_left + s2_right
    cipher = {}
    for char in s1_left:
        for k, v in parent1.cipher.items():
            if v == char:
                cipher[k] = v

    for char in s2_right:
        for k, v in parent2.cipher.items():
            if v == char:
                cipher[k] = v
    seq = Sequence("")
    seq.decoded_sentence = child
    seq.cipher=cipher
    return seq


def run_genetic(encoded, dict, letter_freq, couples_freq):
    population = []
    for i in range(POPULATION_SIZE):
        seq = Sequence(encoded)
        population.append(seq)

    for generation in range(NUM_GENERATIONS):
        fitness_scores = [seq.fitness(dict, letter_freq, couples_freq) for seq in population]
        offspring = []
        for i in range(POPULATION_SIZE):
            parent1 = None
            parent2 = None
            while parent1 == parent2:
                parent1 = random.choices(population, weights=fitness_scores)[0]
                parent2 = random.choices(population, weights=fitness_scores)[0]
            child = crossover(parent1, parent2)
            while not child.check_bijection():
                child = crossover(parent1, parent2)
            child.mutate(encoded)
            offspring.append(child)

        # Replace population with offspring
        population = offspring
    for seq in population:
        print(seq.decoded_sentence)


if __name__ == '__main__':
    dict, letter_freq, couples_freq = open_freq_files()
    run_genetic("xaac cbz", dict, letter_freq, couples_freq)
