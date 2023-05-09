import matplotlib.pyplot as plt

from sequence import *



MUTATION_RATE = 0.05
alphabet = string.ascii_lowercase
POPULATION_SIZE = 100
NUM_GENERATIONS = 600
REPLICATION = 0.05
N = 5


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
    y_values = []
    x_values = []
    string_value = []
    for i in range(0, len(max_scores), 10):
        y_values.append(max_scores[i])
        x_values.append(i)
        string_value.append(str(i))

    plt.bar(x_values, y_values, color='blue')
    plt.xticks(x_values, string_value)
    plt.xlabel('Iteration')
    plt.xticks(rotation=90)
    plt.ylabel('Value')
    plt.title('Max scores in iterations')
    # Show the plot
    plt.show()


def plot_average(average_scores):
    y_values = []
    x_values = []
    string_value = []
    for i in range(0, len(average_scores), 10):
        y_values.append(average_scores[i])
        x_values.append(i)
        string_value.append(str(i))

    plt.bar(x_values, y_values, color='red')
    plt.xticks(x_values, string_value)
    plt.xticks(rotation=90)
    plt.xlabel('Iteration')
    plt.ylabel('Value')
    plt.title('Average scores in iterations')
    # Show the plot
    plt.show()


def basic_genetic(encoded, dict, letter_freq, couples_freq):
    # initialize the population
    global Counter_fitness
    population = []
    for i in range(POPULATION_SIZE):
        # send the encoded message to the constructor and return a random solution with the text decoded.
        seq = Sequence(encoded, None)
        # add solution to the population.
        population.append(seq)
    average_scores = []
    max_scores = []
    replicate_best = []
    # run over the generations and try to improve the solution.
    for generation in range(NUM_GENERATIONS):
        # give score to each solution in the population.
        fitness_scores = [seq.fitness(dict, letter_freq, couples_freq) for seq in population]
        # add the generation to the array that will be showned in the plot.
        average_scores.append(sum(fitness_scores) // len(fitness_scores))
        max_scores.append(max(fitness_scores))
        offspring = []
        replicate_num = int(REPLICATION * POPULATION_SIZE)
        fitness_scores_replicate = fitness_scores.copy()
        for i in range(replicate_num):
            # find the best solution in the population and add it to the offspring.
            best_index = fitness_scores.index(max(fitness_scores_replicate))
            offspring.append(population[best_index])
            fitness_scores_replicate[best_index] = -1
        replicate_best = offspring.copy()
        # check if in the offspring there is same score
        best_score = max(fitness_scores)
        for i in range(len(offspring)):
            flag1 = True
            if offspring[i].score != best_score:
                flag1 = False
                break
        if generation >= 100:
            flag2 = True
            # check if the best score is the same as the last 100 generations
            if max_scores[generation - 95] != max_scores[generation]:
                flag2 = False
        else:
            flag2 = False
        print(max_scores[generation])
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
        print(get_counter_fitness())
        if flag1 and flag2:
            break
    # get the last solution that in max score.
    print(replicate_best[0].score)
    save_solution(replicate_best[0])
    plot_max(max_scores)
    plot_average(average_scores)


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
    for generation in range(NUM_GENERATIONS):
        # give score to each solution in the population.
        fitness_scores = [seq.fitness(dict, letter_freq, couples_freq) for seq in population]
        # add the generation to the array that will be showned in the plot.
        average_scores.append(sum(fitness_scores) // len(fitness_scores))
        max_scores.append(max(fitness_scores))
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

            # save the child before make mutations
            save_cipher = child.cipher
            save_decode = child.decoded_words
            temp_cipher = save_cipher
            temp_decode = save_decode
            fitness_before = child.fitness(dict, letter_freq, couples_freq)
            for i in range(N):
                # try to improve
                child.mutate(encoded)
                fitness_after = child.fitness(dict, letter_freq, couples_freq)
                # if mutation not improve unmutate
                if (fitness_before >= fitness_after):
                    child.cipher = save_cipher
                    child.decoded_words = save_decode
                else:
                    fitness_before = fitness_after
                    save_cipher = child.cipher
                    save_decode = child.decode
            child.cipher = temp_cipher
            child_decode = save_decode

            offspring.append(child)
        # Replace population with offspring
        population = offspring
        print(get_counter_fitness())
    fitness_scores = [seq.fitness(dict, letter_freq, couples_freq) for seq in population]
    best_index = fitness_scores.index(max(fitness_scores))
    save_solution(population[best_index])
    plot_max(max_scores)
    plot_average(average_scores)


def lamark_genetic(encoded, dict, letter_freq, couples_freq):
    population = []
    for i in range(POPULATION_SIZE):
        # send the encoded message to the constructor and return a random solution with the text decoded.
        seq = Sequence(encoded, None)
        # add solution to the population.
        population.append(seq)
    average_scores = []
    max_scores = []
    # run over the generations and try to improve the solution.
    for generation in range(NUM_GENERATIONS):
        [seq.fitness(dict, letter_freq, couples_freq) for seq in population]
        for seq in population:
            save_cipher = seq.cipher
            save_decode = seq.decoded_words
            fitness_before = seq.score
            for i in range(N):
                # try to improve
                seq.mutate(encoded)
                seq.fitness(dict, letter_freq, couples_freq)
                # if mutation not improve unmutate
                if fitness_before >= seq.score:
                    seq.cipher = save_cipher
                    seq.decoded_words = save_decode
                    seq.score = fitness_before
                else:
                    save_cipher = seq.cipher
                    save_decode = seq.decoded_words
                    fitness_before = seq.score
        fitness_scores = [seq.score for seq in population]
        # add the generation to the array that will be showned in the plot.
        average_scores.append(sum(fitness_scores) // len(fitness_scores))
        max_scores.append(max(fitness_scores))
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
            offspring.append(child)
        # Replace population with offspring
        population = offspring
        print(get_counter_fitness())
    fitness_scores = [seq.fitness(dict, letter_freq, couples_freq) for seq in population]
    best_index = fitness_scores.index(max(fitness_scores))
    save_solution(population[best_index])
    plot_max(max_scores)
    plot_average(average_scores)


if __name__ == '__main__':
    encoded, dict, letter_freq, couples_freq = open_freq_files()
    basic_genetic(encoded, dict, letter_freq, couples_freq)
