from sequence import *

MUTATION_RATE = 0.05
alphabet = string.ascii_lowercase
POPULATION_SIZE = 350
NUM_GENERATIONS = 300
REPLICATION = 0.05


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
            dict.append(stripped_line)
    words_encoded = []
    with open('enc.txt', 'r') as f:
        for line in f:
            encoded = line.strip()
            if encoded == "":
                continue
            # go over the encoded message and split it to words.
            wordsline = encoded.split(' ')
            for word in wordsline:
                words_encoded.append(word)

    return words_encoded, dict, letter_freq, couples_freq


def crossover(parent1, parent2, encoded):
    midpoint = random.randint(0, len(parent1.cipher))
    cipher = {}
    for i, (key, value) in enumerate(parent1.cipher.items()):
        if i < midpoint:
            cipher[key] = value
    # Copy key-value pairs from dict2
    for i, (key, value) in enumerate(parent2.cipher.items()):
        if key not in cipher:
            cipher[key] = value
    seq = Sequence(encoded, cipher)
    return seq


def run_genetic(encoded, dict, letter_freq, couples_freq):
    population = []
    for i in range(POPULATION_SIZE):
        # send the encoded message to the constructor and return a random solution with the text decoded.
        seq = Sequence(encoded, None)
        # add solution to the population.
        population.append(seq)

    # run over the generations and try to improve the solution.
    for generation in range(NUM_GENERATIONS):
        # give score to each solution in the population.
        if generation == 15:
            print("15")
        fitness_scores = [seq.fitness(dict, letter_freq, couples_freq) for seq in population]
        offspring = []
        replicate_num = int(REPLICATION * POPULATION_SIZE)
        fitness_scores_replicate = fitness_scores.copy()
        for i in range(replicate_num):
            # find the best solution in the population and add it to the offspring.
            best_index = fitness_scores.index(max(fitness_scores_replicate))
            offspring.append(population[best_index])
            fitness_scores_replicate[best_index] = -1
        for i in range(POPULATION_SIZE - replicate_num):
            parent1 = random.choices(population, weights=fitness_scores)[0]
            parent2 = random.choices(population, weights=fitness_scores)[0]
            while parent1 == parent2:
                parent1 = random.choices(population, weights=fitness_scores)[0]
            # create a new solution by crossing over the parents.
            child = crossover(parent1, parent2, encoded)
            child.mutate(encoded)
            offspring.append(child)
        # Replace population with offspring
        population = offspring



if __name__ == '__main__':
    encoded, dict, letter_freq, couples_freq = open_freq_files()
    run_genetic(encoded, dict, letter_freq, couples_freq)
