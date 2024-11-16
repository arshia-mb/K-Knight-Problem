import random

#Generates fenotip based on genotip
def generate_fenotip(pop):
    fenotip = ""
    for i in range(size):
        for j in range(size):
            index = i*size+j
            if index in pop:
                fenotip += " K "
            else:
                fenotip += " _ "
        fenotip += "\n"
    return fenotip

#Finding first larger index than what we want
def find_greater(l,t):
    notfound = len(l)
    for i in range(len(l)):
        if l[i] > t:
            return i
    return notfound 

#Calculates the fitness of a genome
def fitness(genome,size):
    conflict = 0
    move_vector = [(1,2),(1,-2),(2,1),(2,-1)] #Only checking one side of the conflict
    for index in genome:
        row = int(index/size)
        col = index%size
        for x,y in move_vector:
            newrow = x + row
            newcol = y + col
            if newrow >= size or newrow < 0 or newcol >= size or newcol < 0:
                continue #invalid movement, check next
            if newrow * size + newcol in genome: #Check if there is a pair conflict
                conflict += 1
    #Calculate fitness based on size and conflict:
    knights = len(genome) #number of knights on the board is the same as genome length
    if conflict == 0:
        fitness = (size*size/2) + knights #We like the situations without conflict, bias?!
    else:
        fitness = knights/conflict #We want more nights that have less conflict 
    return fitness

#Creates a random board with knight_count knights on it
def create_random_gene(size,knight_count):
    genome = []
    for i in range(knight_count):
        #Checking if we already have the desired 
        while(True):
            index = random.randint(0, size*size-1) #create random index
            if not index in genome:
                genome.append(index)
                break
    #Get fitness function for each genome        
    genome.sort() #We sort the answer for ease on future operations
    return genome
    
#Creates the initial population randomly
def initial_population(size,pop_count):
    population = []
    for p in range(pop_count):
        #Creating random population:
        knight_count = random.randint(1, int(size*size/2)) #Number of knights on the board
        genome = create_random_gene(size,knight_count)  
        pop = genome.copy() #Creating a pop based one the genmoe 
        pop.append(fitness(genome, size)) #Add it's fitness 
        population.append(pop) #Add pop to the population pool
    return population

#Reproduction selection - Stochastic universal sampling
def sus(size,population):
    total_fitness = 0 #total fitness of the group
    fitness_scale = [] #A scale that represents our wheel
    for pop in population:
        total_fitness += pop[-1] #Last item in the list is the fitness of a genome
        fitness_scale.append(total_fitness) #Setting our boundries
    selection_pool = []        
    pointer_scale = total_fitness/size #Each step the pointer has to move
    start = random.uniform(0, pointer_scale) #Selects our starting point
    pointers = [] #Pointers for selecting
    for i in range(size):
        pointers.append(start + i*pointer_scale)
    #RWS selection part
    fitness_pointer = 0 #The pointer that we are checking right now
    for pointer in pointers:
        while fitness_scale[fitness_pointer] < pointer: #move in the wheel
            fitness_pointer += 1 #if it's not in this section then we move to the next section
        selection_pool.append(population[fitness_pointer])
    return selection_pool

#Cross Over - using single point crossover on the row
def crossover(p1,p2,size):
    row = random.randint(0, size-2) #Getting the row we want to use as cross point
    cross_point = row*size+size-1 #Square that we want to cut from
    #Index shows what point in the list the cross over must start
    index1 = find_greater(p1, cross_point)
    index2 = find_greater(p2, cross_point)
    child = p1[:index1] #Adding the top half from one parent
    child.extend(p2[index2:]) #Adding the bottom half from the otherone
    if child == []: #Top half of the p1 is empty and bottom half of the p2 is empty!
        child = p2[:index2]
        child.extend(p1[index1:])
    return child

#Mutation algorithm performed after crossover
def mutation(size):
    knight_count = random.randint(1, int(size*size/2)) #Number of knights on the board
    genome = create_random_gene(size,knight_count)  
    pop = genome.copy() #Creating a pop based one the genmoe 
    pop.append(fitness(genome, size)) #Add it's fitness 
    return pop

#Creating new generation
def reproduction(size,parent_pool,mutation_rate):
    new_generation = []
    while(len(parent_pool) > 0):
        #Chose parents and remove them from the pool
        parent1 = random.choice(parent_pool)
        parent_pool.remove(parent1)
        parent2 = random.choice(parent_pool)
        parent_pool.remove(parent2)
        #Checking for mutation
        if random.uniform(0, 1) < mutation_rate: #Mutation must happen
            child = mutation(size)
            new_generation.append(child)
            continue
        #Create child
        child = crossover(parent1[:len(parent1)-1], parent2[:len(parent2)-1], size)
        child.append(fitness(child, size)) #Calculate fitness
        new_generation.append(child)
    return new_generation

#Reverse selection - trying to keep divercity
def reverse_selection(pop_count,pop_dict,population):
    new_generation = []
    #Selecting survivals
    for key in pop_dict:
        pop = pop_dict[key][0] #Example of a key
        new_generation.append(pop)
        population.remove(pop)
    #Adding other elements randomly
    new_generation.extend(random.sample(population, pop_count-len(new_generation)))
    return new_generation

#Tournament - survival selection
def tournament(size,pop_count,population):
    new_pop = []
    for i in range(pop_count):
        tourny = random.sample(population, 4) #Sample K random pop from population 
        #Add the best of tor to the new_pop
        victor = tourny[0]
        for player in tourny:
            if victor[-1] < player[-1]:
                victor = player
        population.remove(victor) #Remove victor from parenting pool
        new_pop.append(victor) #Add the victor to population
    return new_pop        

#Genetic algorithm steps
def genetic_algorithm(size,pop_count,parent_count,mutation_rate,step_count):
    #Calculating best possible answer
    max_knights = int(size*size/2)
    if size%2==1:
        max_knights = max_knights + 1
    #Creating initial population randomly
    population = initial_population(size, pop_count)
    #Starting evelution steps
    for step in range(step_count):
        #Checking end conditions - finding a good solution
        for pop in population:
            if pop[-1] == max_knights*2: #We have max knights
                return population
        parent_pool = sus(parent_count, population) #Chose parent pool
        new_generation = reproduction(size, parent_pool, mutation_rate) #Create new generation
        population.extend(new_generation) #Add generation to population 
        population = tournament(size, pop_count, population) #Select population that survives
        
    return population

#Problem parameters
size = 8 #Size of the board
pop_count = 500 #Number of population pool
parent_count = 26 #Number of parents each selection
step_count = 500 #Number of evelution steps
mutation_rate = 0.3

answers = genetic_algorithm(size,pop_count,parent_count,mutation_rate,step_count)