import pygame
import random
import math
import itertools
from collections import Counter
import time


class TSP_BF:
    def __init__(self):
        self.visuals = False
        self.mutation_rate = 0.01 
        pop_size = 100

        #Test data
        self.cities = [(323, 90), (28, 123), (226, 390), (119, 37), (316, 282), (104, 1), (103, 181), (14, 88), (198, 368), (179, 122)]
        #Uncomment the following line and comment out the above line to generate a random list of cities
        #self.cities = []
        if not self.cities:
            cities_count = 20
            for i in range(cities_count):
                x = random.randint(0, 399)
                y = random.randint(0, 399)
                self.cities.append((x ,y))

        # Fill population with random permutations
        self.population = [None] * pop_size
        for i in range(len(self.population)):
            random.shuffle(self.cities)
            self.population[i] = self.cities[:]

        self.fitness = [0] * pop_size

        self.current_best = {"path": self.population[0], "length": float('inf')}

        self.gen_count = 0

    def start(self):
        self.stamp = time.time()
        if self.visuals:
            pygame.init()
            pygame.font.init()
            self.font = pygame.font.SysFont('Times New Roman', 30)
            self.screen = pygame.display.set_mode((800, 850))
            size = (400, 800)
            self.surface = pygame.Surface(size)      

            self.main_loop()
        else:
            while True:
                self.gen_count += 1
                self.calculate_fitness()
                self.generate_new_population()

    
    def main_loop(self):
        current_generation_text = self.font.render("Initialising", False, (255, 255, 255))
        alltime_best_text = self.font.render("Initialising", False, (255, 255, 255))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            self.surface.fill((0, 0, 0))
            self.screen.fill((0, 0, 0))

            self.draw_cities()

            self.gen_count += 1
            self.calculate_fitness()
            self.generate_new_population()

            max_idx = self.fitness.index(max(self.fitness))            
            current_gen_best = self.population[max_idx]

            self.draw_path(current_gen_best, (255, 255, 255), 1, 0)
            self.draw_path(self.current_best["path"], (255, 255, 255), 1, 1)
            current_generation_text = self.font.render("Generation {0} best".format(self.gen_count), False, (255, 255, 255))
            alltime_best_text = self.font.render("Current best: {0}".format(math.floor(self.current_best["length"])), False, (255, 255, 255))

            self.screen.blit(self.surface, (10, 10))
            self.screen.blit(current_generation_text, (450, 100))
            self.screen.blit(alltime_best_text, (450, 500))

            pygame.display.update()            



    def generate_new_population(self):
        new_pop = [None] * len(self.population)
        for i in range(len(self.population)):
            parentA, parentB = None, None
            iter_limit = 0
            while parentA == parentB:
                iter_limit += 1
                parentA = self.accept_reject()
                parentB = self.accept_reject()
                if iter_limit > 5000:
                    break
            new_pop[i] = self.crossover(parentA, parentB)
        new_pop = self.mutate(new_pop)

        self.population = new_pop

    def accept_reject(self):
        max_fitness = max(self.fitness)
        #Choose a random element from the population
        idx = random.randint(0, len(self.population)-1)        

        # Generate a random number between 0 and max_fitness
        # If the fitness of the current element is lower than the random number,
        # choose another element and try again. Othewise return the current element
        while self.fitness[idx] < random.uniform(0, max_fitness):
            idx = random.randint(0, len(self.population)-1)
        return self.population[idx]


    def crossover(self, pA, pB):
        #Add an ordered set of points from parentA, then fill the remaining spots with points from parentB in the order that they appear
        rand = random.randint(0, len(pA)-1)
        child = pA[:rand]

        intersect = Counter(child) & Counter(pB)
        pB = list((Counter(pB) - intersect).elements())
        child += pB[:]
        return child        


    def mutate(self, p):
        # Generate a random number. If it is lower than the mutation rate, swap
        # the current element with a random element from the population
        for i in range(len(p)):
            if random.random() < self.mutation_rate:
                idx = random.randint(0, len(self.population)-1)
                p[i], p[idx] = p[idx], p[i]
        return p
        

    def calculate_fitness(self):
        total_fitness = 0
        # Calculate length of path for each route
        # Invert length to give shorter routes a higher fitness
        for i in range(len(self.fitness)):
            self.fitness[i] = self.calculate_distance(self.population[i])
            if (self.fitness[i] < self.current_best["length"]):
                print("New best path found: {0} after {1} generations and {2:5.2f} seconds.".format(self.fitness[i], self.gen_count, time.time()-self.stamp))
                self.current_best["path"] = self.population[i]
                self.current_best["length"] = self.fitness[i]
            self.fitness[i] = 1/self.fitness[i]
            total_fitness += self.fitness[i]


    def calculate_distance(self, p):
        total = 0

        for i in range(len(p)-1):
            x = pow((p[i+1][0]-p[i][0]), 2)
            y = pow((p[i+1][1]-p[i][1]), 2)
            total += math.sqrt(x+y)

        x = pow((p[-1][0]-p[0][0]), 2)
        y = pow((p[-1][1]-p[0][1]), 2)
        total += math.sqrt(x+y)
        return total

    def draw_cities(self):
        for i in range(len(self.cities)):
            pygame.draw.circle(self.surface, (255, 255, 255), (self.cities[i][0], self.cities[i][1]), 3)
            pygame.draw.circle(self.surface, (255, 255, 255), (self.cities[i][0], self.cities[i][1]+400), 3)

    def draw_path(self, p, colour, width, y_multi):
        offset = 400*y_multi
        for i in range(len(p)-1):
            pygame.draw.line(self.surface, colour, (p[i][0], p[i][1]+offset), (p[i+1][0], p[i+1][1]+offset), width)
        pygame.draw.line(self.surface, colour, (p[-1][0], p[-1][1]+offset), (p[0][0], p[0][1]+offset), width)    
    
tsp = TSP_BF()
tsp.start()
