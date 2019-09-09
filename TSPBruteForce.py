import pygame
import random
import math
import itertools
import time


class TSP_BF:
    def __init__(self):  
        self.visuals = False

        self.cities = [(323, 90), (28, 123), (226, 390), (119, 37), (316, 282), (104, 1), (103, 181), (14, 88), (198, 368), (179, 122)]      
        #self.cities = []
        if not self.cities:
            cities_count = 10
            for i in range(cities_count):
                x = random.randint(0, 399)
                y = random.randint(0, 399)
                self.cities.append((x ,y))
        print(self.cities)
        self.current_best = {"distance": float("inf"), "path":[]}
        self.path_generator = itertools.permutations(self.cities)       


    def start(self):
        stamp = time.time()        
        if self.visuals:
            pygame.init()
            self.screen = pygame.display.set_mode((450, 450))
            size = (400, 400)
            self.surface = pygame.Surface(size)    
            self.main_loop()
        else:
            print(f"Shortest possible path: {self.find_best_path()}")
            print("Search completed in: {:5.2f} seconds".format(time.time()-stamp))

    def find_best_path(self):
        for current_path in self.path_generator:
            dist = self.calculate_distance(current_path)
            if dist < self.current_best["distance"]:
                self.current_best["distance"] = dist
                self.current_best["path"] = self.cities[:]
        return self.current_best["distance"]

    
    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            try:
                current_path = next(self.path_generator)
            except:
                print(f"Shortest possible path: {self.current_best['distance']}")
                break

            dist = self.calculate_distance(current_path)
            if dist < self.current_best["distance"]:
                self.current_best["distance"] = dist
                self.current_best["path"] = self.cities[:]
                print(self.current_best["distance"])

            self.surface.fill((0, 0, 0))
            self.draw_cities()

            self.draw_path(current_path, (255, 255, 255), 1)
            self.draw_path(self.current_best["path"], (255, 0, 255), 3)
            self.screen.blit(self.surface, (25, 25))
            pygame.display.update()
            

    def swap(self, i, j):
        self.cities[j], self.cities[i] = self.cities[i], self.cities[j]


    def draw_cities(self):
        for i in range(len(self.cities)):
            pygame.draw.circle(self.surface, (255, 255, 255), (self.cities[i][0], self.cities[i][1]), 3)

    def draw_path(self, p, colour, width):
        for i in range(len(p)-1):
            pygame.draw.line(self.surface, colour, (p[i][0], p[i][1]), (p[i+1][0], p[i+1][1]), width)
        pygame.draw.line(self.surface, colour, (p[-1][0], p[-1][1]), (p[0][0], p[0][1]), width)

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
    
tsp = TSP_BF()
tsp.start()