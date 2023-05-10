import matplotlib.pyplot as plt

from sequence import *

MUTATION_RATE = 0.05
alphabet = string.ascii_lowercase
POPULATION_SIZE = 100
NUM_GENERATIONS = 200
REPLICATION = 0.15
N = 1


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
    population = init_start([])
    average_scores = []
    max_scores = []
    best_solution = None
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
            if i == 0:
                best_solution = offspring[0].copy()
        for i in range(POPULATION_SIZE - replicate_num):
            tournament_size = 5
            tournament = random.sample(population, tournament_size)
            # Choose the individual with the highest fitness score as the winner
            winner = max(tournament, key=lambda x: x.score)
            tournament = random.sample(population, tournament_size)
            # Choose the individual with the highest fitness score as the winner
            winner2 = max(tournament, key=lambda x: x.score)
            # create a new solution by crossing over the parents.
            child = crossover(winner, winner2, encoded)
            child.mutate(encoded)
            offspring.append(child)
        # Replace population with offspring
        population = offspring
        print(max_scores[generation])
        print(get_counter_fitness())
        if generation >= 100:
            flag = stop_run(fitness_scores, generation, max_scores, offspring)
            if flag:
                break
    # get the last solution that in max score.
    save_solution(best_solution)
    plot_max(max_scores)
    plot_average(average_scores)


def init_start(population):
    for i in range(POPULATION_SIZE):
        # send the encoded message to the constructor and return a random solution with the text decoded.
        seq = Sequence(encoded, None)
        # add solution to the population.
        population.append(seq)
    return population


def try_better(population):
    start_population = []
    new_population = []
    old_population = []
    for z in range(len(population)):
        start_population.append(population[z].copy())
        old_population.append(population[z].copy())
    for k in range(POPULATION_SIZE):
        for j in range(N):
            population[k].mutate(encoded)
            population[k].fitness(dict, letter_freq, couples_freq)
            if j == N - 1:
                if population[k].score > old_population[k].score:
                    new_population.append(population[k])
                else:
                    new_population.append(old_population[k])
            else:
                if population[k].score > old_population[k].score:
                    old_population[k] = population[k]
    return new_population, start_population


def stop_run(fitness_scores, generation, max_scores, offspring):
    best_score = max(fitness_scores)
    count = 0
    flag1 = True
    for i in range(len(offspring)):
        if offspring[i].score != best_score:
            count += 1
            if count == 3:
                flag1 = False
                break
    if generation >= 100:
        flag2 = True
        # check if the best score is the same as the last 100 generations
        if max_scores[generation - 80] != max_scores[generation]:
            flag2 = False
    else:
        flag2 = False
    if flag1 and flag2:
        return True


def drawin_gentic(encoded, dict, letter_freq, couples_freq):
    global Counter_fitness
    population = init_start([])
    # initialize the population
    average_scores = []
    max_scores = []
    best_solution = None
    replicate_num = int(REPLICATION * POPULATION_SIZE)
    for generation in range(NUM_GENERATIONS):
        offspring = []
        # give score to each solution in the population.
        fitness_scores = [seq.fitness(dict, letter_freq, couples_freq) for seq in population]
        # add the generation to the array that will be showned in the plot.
        average_scores.append(sum(fitness_scores) // len(fitness_scores))
        max_scores.append(max(fitness_scores))
        fitness_scores_replicate = fitness_scores.copy()
        for i in range(replicate_num):
            # find the best solution in the population and add it to the offspring.
            best_index = fitness_scores.index(max(fitness_scores_replicate))
            offspring.append(population[best_index].copy())
            fitness_scores_replicate[best_index] = -1
            if i == 0:
                best_solution = offspring[0].copy()
        # try to go better with it can improve the solution.
        new_population, start_population = try_better(population)
        for i in range(POPULATION_SIZE):
            start_population[i].score = new_population[i].score
        fitness_scores = [seq.score for seq in new_population]
        for i in range(POPULATION_SIZE - replicate_num):
            tournament_size = 3
            tournament = random.sample(start_population, tournament_size)
            # Choose the individual with the highest fitness score as the winner
            winner = max(tournament, key=lambda x: x.score)
            tournament = random.sample(start_population, tournament_size)
            # Choose the individual with the highest fitness score as the winner
            winner2 = max(tournament, key=lambda x: x.score)
            while winner == winner2:
                tournament = random.sample(start_population, tournament_size)
                winner2 = max(tournament, key=lambda x: x.score)
            # create a new solution by crossing over the parents.
            child = crossover(winner, winner2, encoded)
            offspring.append(child)
        population = offspring
        if generation >= 100:
            stop_run(fitness_scores, generation, max_scores, offspring)
        print(get_counter_fitness())
        print(max_scores[generation])
    #   save result.
    save_solution(best_solution)
    plot_max(max_scores)
    plot_average(average_scores)

def lamark_genetic(encoded, dict, letter_freq, couples_freq):
    global Counter_fitness
    population = init_start([])
    # initialize the population
    average_scores = []
    max_scores = []
    best_solution = None
    replicate_num = int(REPLICATION * POPULATION_SIZE)
    for generation in range(NUM_GENERATIONS):
        offspring = []
        # give score to each solution in the population.
        fitness_scores = [seq.fitness(dict, letter_freq, couples_freq) for seq in population]
        # add the generation to the array that will be showned in the plot.
        average_scores.append(sum(fitness_scores) // len(fitness_scores))
        max_scores.append(max(fitness_scores))
        fitness_scores_replicate = fitness_scores.copy()
        for i in range(replicate_num):
            # find the best solution in the population and add it to the offspring.
            best_index = fitness_scores.index(max(fitness_scores_replicate))
            offspring.append(population[best_index].copy())
            fitness_scores_replicate[best_index] = -1
            if i == 0:
                best_solution = offspring[0].copy()
        # try to go better with it can improve the solution.
        new_population, start_population = try_better(population)
        fitness_scores = [seq.score for seq in new_population]
        for i in range(POPULATION_SIZE - replicate_num):
            tournament_size = 5
            tournament = random.sample(new_population, tournament_size)
            # Choose the individual with the highest fitness score as the winner
            winner = max(tournament, key=lambda x: x.score)
            tournament = random.sample(new_population, tournament_size)
            # Choose the individual with the highest fitness score as the winner
            winner2 = max(tournament, key=lambda x: x.score)
            # create a new solution by crossing over the parents.
            child = crossover(winner, winner2, encoded)
            offspring.append(child)
        population = offspring
        if generation >= 100:
            stop_run(fitness_scores, generation, max_scores, offspring)
        print(get_counter_fitness())
        print(max_scores[generation])
    #   save result.
    save_solution(best_solution)
    plot_max(max_scores)
    plot_average(average_scores)


if __name__ == '__main__':
    encoded, dict, letter_freq, couples_freq = open_freq_files()
    drawin_gentic(encoded, dict, letter_freq, couples_freq)
