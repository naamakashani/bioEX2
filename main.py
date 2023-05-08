from sequence import *
import matplotlib.pyplot as plt

MUTATION_RATE = 0.05
alphabet = string.ascii_lowercase
POPULATION_SIZE = 300
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
    organized_cipher_parent1 = {}
    for word in encoded:
        for letter in word:
            if letter not in organized_cipher_parent1.keys() and letter in alphabet:
                organized_cipher_parent1[letter] = parent1.cipher[letter]

    organized_cipher_parent2 = {}
    for word in encoded:
        for letter in word:
            if letter not in organized_cipher_parent2.keys() and letter in alphabet:
                organized_cipher_parent2[letter] = parent2.cipher[letter]

    midpoint = random.randint(0, len(organized_cipher_parent1))
    cipher = {}
    for i, (key, value) in enumerate(organized_cipher_parent1.items()):
        if i < midpoint:
            cipher[key] = value
    # Copy key-value pairs from dict2
    for (key, value) in (organized_cipher_parent2.items()):
        if key not in cipher:
            cipher[key] = value
    char_appearances = {
        "a": 0, "b": 0, "c": 0, "d": 0, "e": 0,
        "f": 0, "g": 0, "h": 0, "i": 0, "j": 0,
        "k": 0, "l": 0, "m": 0, "n": 0, "o": 0,
        "p": 0, "q": 0, "r": 0, "s": 0, "t": 0,
        "u": 0, "v": 0, "w": 0, "x": 0, "y": 0,
        "z": 0
    }
    for i, (key, value) in enumerate(cipher.items()):
        char_appearances[value] += 1
    for i, (key, value) in enumerate(cipher.items()):
        if char_appearances[value] > 1:
            for char in alphabet:
                if char_appearances[char] == 0:
                    cipher[key] = char
                    char_appearances[char] += 1
                    char_appearances[value] -= 1
                    break
    seq = Sequence(encoded, cipher)
    return seq




def save_solution(best_sequence):
    # save the permutation in perm.txt file
    with open("perm.txt", 'w') as f:
        for (key, value) in best_sequence.cipher.items():
            f.write(f"{key} {value}\n")
    # open the plain.txt file and write to it the decoded content based on the permutation
    with open("plain.txt", 'w') as plain:
        with open("enc.txt", 'r') as enc:
            for line in enc:
                encoded = line.strip()
                decoded = ""
                for char in encoded:
                    if char in best_sequence.cipher:
                        decoded += best_sequence.cipher[char]
                    else:
                        decoded += char
                plain.write(f"{decoded}\n")


def plot_max(max_scores):
    # Create a figure and axis object
    fig, ax = plt.subplots()
    # Set the width of each bar
    bar_width = 0.1
    # Create two sets of bars for each iteration: one for max values, one for avg values
    x_ticks = []
    # Set the x-axis ticks to the iteration numbers
    for i in range(1, len(max_scores) + 1):
        x_ticks.append(i * 10)
    # Create a figure and two axis objects for the two plots
    ax.set_xticks(x_ticks)
    ax.bar(x_ticks, max_scores, bar_width, label='Max')
    ax.legend()
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Value')
    # Show the plot
    plt.show()


def plot_average(average_scores):
    # Create a figure and axis object
    bar_width = 0.1
    fig, ax = plt.subplots()
    x_ticks = []
    # Set the x-axis ticks to the iteration numbers
    for i in range(1, len(average_scores) + 1):
        x_ticks.append(i * 10)
    # Create a figure and two axis objects for the two plots
    ax.set_xticks(x_ticks)
    ax.bar(x_ticks, average_scores, bar_width, label='Max')

    ax.legend()
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Value')

    # Show the plot
    plt.show()


def basic_genetic(encoded, dict, letter_freq, couples_freq):
    population = []
    for i in range(POPULATION_SIZE):
        # send the encoded message to the constructor and return a random solution with the text decoded.
        seq = Sequence(encoded, None)
        # add solution to the population.
        population.append(seq)
    average_scores = []
    max_scores = []
    counter = 0
    counter_not_changed = 0

    # run over the generations and try to improve the solution.
    for generation in range(1, NUM_GENERATIONS + 1):
        # give score to each solution in the population.
        fitness_scores = [seq.fitness(dict, letter_freq, couples_freq) for seq in population]
        # add the generation to the array that will be showned in the plot.
        if generation % 10 == 0 and generation >= 10:
            average_scores.append(sum(fitness_scores) // len(fitness_scores))
            max_scores.append(max(fitness_scores))
            counter += 1
            if counter > 1:
                # if the score not improve add 1 to counter
                if max_scores[counter - 1] <= max_scores[counter - 2]:
                    counter_not_changed += 1
                if (counter_not_changed > 4):
                    break
                else:
                    counter_not_changed = 0
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
    fitness_scores = [seq.fitness(dict, letter_freq, couples_freq) for seq in population]
    best_index = fitness_scores.index(max(fitness_scores))
    save_solution(population[best_index])
    plot_max(max_scores)
    plot_average(average_scores)
    return generation + 1


def darwin_genetic(encoded, dict, letter_freq, couples_freq):
    population = []
    for i in range(POPULATION_SIZE):
        # send the encoded message to the constructor and return a random solution with the text decoded.
        seq = Sequence(encoded, None)
        # add solution to the population.
        population.append(seq)
    average_scores = []
    max_scores = []
    counter = 0
    counter_not_changed = 0

    # run over the generations and try to improve the solution.
    for generation in range(1, NUM_GENERATIONS + 1):
        # give score to each solution in the population.
        fitness_scores = [seq.fitness(dict, letter_freq, couples_freq) for seq in population]
        # add the generation to the array that will be showned in the plot.
        if generation % 10 == 0 and generation >= 10:
            average_scores.append(sum(fitness_scores) // len(fitness_scores))
            max_scores.append(max(fitness_scores))
            counter += 1
            if counter > 1:
                # if the score not improve add 1 to counter
                if max_scores[counter - 1] <= max_scores[counter - 2]:
                    counter_not_changed += 1
                if (counter_not_changed > 4):
                    break
                else:
                    counter_not_changed = 0
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
    fitness_scores = [seq.fitness(dict, letter_freq, couples_freq) for seq in population]
    best_index = fitness_scores.index(max(fitness_scores))
    save_solution(population[best_index])
    plot_max(max_scores)
    plot_average(average_scores)
    return generation + 1


def lamark_genetic(encoded, dict, letter_freq, couples_freq):
    population = []
    for i in range(POPULATION_SIZE):
        # send the encoded message to the constructor and return a random solution with the text decoded.
        seq = Sequence(encoded, None)
        # add solution to the population.
        population.append(seq)
    average_scores = []
    max_scores = []
    counter = 0
    counter_not_changed = 0

    # run over the generations and try to improve the solution.
    for generation in range(1, NUM_GENERATIONS + 1):
        # give score to each solution in the population.
        fitness_scores = [seq.fitness(dict, letter_freq, couples_freq) for seq in population]
        # add the generation to the array that will be showned in the plot.
        if generation % 10 == 0 and generation >= 10:
            average_scores.append(sum(fitness_scores) // len(fitness_scores))
            max_scores.append(max(fitness_scores))
            counter += 1
            if counter > 1:
                # if the score not improve add 1 to counter
                if max_scores[counter - 1] <= max_scores[counter - 2]:
                    counter_not_changed += 1
                if (counter_not_changed > 4):
                    break
                else:
                    counter_not_changed = 0
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
    fitness_scores = [seq.fitness(dict, letter_freq, couples_freq) for seq in population]
    best_index = fitness_scores.index(max(fitness_scores))
    save_solution(population[best_index])
    plot_max(max_scores)
    plot_average(average_scores)
    return generation + 1


if __name__ == '__main__':
    encoded, dict, letter_freq, couples_freq = open_freq_files()
    number_of_generation = basic_genetic(encoded, dict, letter_freq, couples_freq)
    print(number_of_generation * POPULATION_SIZE)
