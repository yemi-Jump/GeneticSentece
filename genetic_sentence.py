import string
import random

target = "Hello World"

# evaluates fitness for individual
def eval_fit(dna, obj):
	test = [i for i, j in zip(dna, list(target)) if i == j] # compares target and individual dna
	return len(test)

class Individual:
	def __init__(self, dna, fitness):
		self.dna = dna
		self.fitness = fitness

	# creates random individual dna
	def random_birth():
		chromosome = []

		for i in range(len(target)):
			genes = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase +
                            string.digits + " "))
			chromosome.append(genes)
		return chromosome

	# converts individual dna list into string
	def convert(self, dna):
		# convert list of genes into sentence
		new = ""
		for i in dna:
			new += i

		return new

class Population:
	def __init__(self, size):
		self.population = []
		self.size = size
		self.generation = 1

		# creates an inital population of individuals
		create = [Individual(Individual.random_birth(), 0) for i in range(self.size)]

		for obj in create:
			self.population.append(obj)

		print("Staring Population:")
		for obj in self.population:
			obj.fitness = eval_fit(obj.dna, obj)

		# sort by highest fitness
		self.population.sort(key=lambda obj: obj.fitness, reverse=True)

		for obj in self.population:
			print(obj.convert(obj.dna), obj.fitness)

		while self.population[0].fitness < len(target):
			self.selection()
			individual = self.population[0]
			print("Generation:", self.generation, "Individual:",
                      Individual.convert(self, individual.dna),
                      "Fitness:", individual.fitness)

	def selection(self):
		parent1 = self.population[0]
		parent2 = self.population[1]

		parent1 = list(parent1.dna)
		parent2 = list(parent2.dna)

		mate = [None]*(len(parent1) + len(parent2)) # combines both dna lists
		mate[::2] = parent1
		mate[1::2] = parent2

		tuple_dna = list(zip(mate[::2], mate[1::2]))
		self.population.clear()
		self.crossover(tuple_dna)

	def crossover(self, tuple_dna):
		while len(self.population) < self.size:
			child = []
			# return gene of either parent1 or parent2 or mutate the gene
			for tuple in tuple_dna:
				gene = self.mutation(random.choice(tuple))
				child.append(gene)

			individual = Individual(child, 0)
			individual.fitness = eval_fit(individual.dna, individual)
			self.population.append(individual)

		self.generation += 1
		self.population.sort(key=lambda obj: obj.fitness, reverse=True)
		return self.population

	def mutation(self, gene):
		mutation_rate = .03
		if random.random() < mutation_rate:
			gene = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase +
							string.digits + " "))
		else:
			pass
		return gene

if __name__ == '__main__':
	Population(1000)
