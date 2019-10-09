import string
import random
import pygame as pg


# evaluates fitness for individual
def eval_fit(target, dna, obj):
	test = [i for i, j in zip(dna, list(target)) if i == j] # compares target and individual dna
	return len(test)

class Individual:
	def __init__(self, dna, fitness):
		self.dna = dna
		self.fitness = fitness

	# creates random individual dna
	def random_birth(target):
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
	def __init__(self, size, target):
		self.target = target
		self.population = []
		self.size = size
		self.generation = 1

		# creates an inital population of individuals
		create = [Individual(Individual.random_birth(self.target), 0) for i in range(self.size)]

		for obj in create:
			self.population.append(obj)

		print("Starting Population:")
		for obj in self.population:
			obj.fitness = eval_fit(self.target, obj.dna, obj)

		# sort by highest fitness
		self.population.sort(key=lambda obj: obj.fitness, reverse=True)

		for obj in self.population:
			print(obj.convert(obj.dna), obj.fitness)

	def next_variation(self):
		if self.population[0].fitness < len(self.target):
			self.selection()
			individual = self.population[0]
			print("Generation:", self.generation, "Individual:",
					  Individual.convert(self, individual.dna),
					  "Fitness:", individual.fitness)
			return individual.convert(individual.dna)

		elif self.population[0].fitness == len(self.target):
			return self.population[0].convert(self.population[0].dna)


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
			individual.fitness = eval_fit(self.target, individual.dna, individual)
			self.population.append(individual)

		self.generation += 1
		self.population.sort(key=lambda obj: obj.fitness, reverse=True)
		#store_fit(self.population[0])
		return self.population

	def mutation(self, gene):
		mutation_rate = .03
		if random.random() < mutation_rate:
			gene = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase +
							string.digits + " "))
		else:
			pass
		return gene


pg.init()

screen = pg.display.set_mode((1080, 720))
font = pg.font.Font(None, 32)
big_font = pg.font.Font(None, 48)
xl_font = pg.font.Font(None, 72)
clock = pg.time.Clock()
input_box = pg.Rect(440, 600, 200, 32)
color_inactive = pg.Color('lightskyblue3')
color_active = pg.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
target = ''
top = ''
done = False

population = Population(1, target)
while not done:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			done = True
		if event.type == pg.MOUSEBUTTONDOWN:
			# If the user clicked on the input_box rect.
			if input_box.collidepoint(event.pos):
				# Toggle the active variable.
				active = not active
			else:
				active = False
			# Change the current color of the input box.
			color = color_active if active else color_inactive
		if event.type == pg.KEYDOWN:
			if active:
				if event.key == pg.K_RETURN:
					print(text)
					target = text
					population = Population(1000, target)
					#population.set_target(target)
					text = ''

				elif event.key == pg.K_BACKSPACE:
					text = text[:-1]
				else:
					text += event.unicode
	top = str(population.next_variation())
	screen.fill((30, 30, 30))
	# Render the current text.
	txt_surface = font.render(text, True, color)
	# Resize the box if the text is too long.
	width = max(200, txt_surface.get_width()+10)
	input_box.w = width
	# Blit the text.
	screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
	title = big_font.render("Genetic Sentence", 1, pg.Color('dodgerblue2'))
	screen.blit(title, (400, 20))
	sentence = font.render(("Target: " + target), 1, pg.Color('gold'))
	screen.blit(sentence, (400, 100))
	top_sentence = font.render(("test: " + top), 1, pg.Color('lightskyblue3'))
	screen.blit(top_sentence, (400, 400))
	# Blit the input_box rect.
	pg.draw.rect(screen, color, input_box, 2)

	pg.display.flip()
	clock.tick(30)
