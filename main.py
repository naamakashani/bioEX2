from sequence import *

MUTATION_RATE = 0.05
alphabet = string.ascii_lowercase
POPULATION_SIZE = 2000
NUM_GENERATIONS = 100
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
            if len(stripped_line) > 1:
                dict.append(stripped_line)
    return dict, letter_freq, couples_freq


def crossover(parent1, parent2, encoded):
    midpoint = random.randint(0, len(parent1.cipher))
    cipher = {}
    keys1 = parent1.cipher.keys()
    keys2 = parent2.cipher.keys()
    for i in range(parent1.cipher):
        if i < midpoint:
            cipher[keys1[i]] = parent1.cipher[keys1[i]]
        else:
            cipher[keys2[i]] = parent2.cipher[keys2[i]]
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
        fitness_scores = [seq.fitness(dict, letter_freq, couples_freq) for seq in population]
        offspring = []
        replicate_num = int(REPLICATION * POPULATION_SIZE)
        fitness_scores_replicate = fitness_scores.copy()
        for i in range(replicate_num):
            # find the best solution in the population and add it to the offspring.
            best_index = fitness_scores.index(max(fitness_scores_replicate))
            offspring.append(population[best_index])
            fitness_scores_replicate.remove(best_index)

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
    for seq in population:
        print(seq.decoded_sentence)


if __name__ == '__main__':
    dict, letter_freq, couples_freq = open_freq_files()
    run_genetic("xaac cbz", dict, letter_freq, couples_freq)
