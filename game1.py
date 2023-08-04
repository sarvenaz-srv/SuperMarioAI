import random
from matplotlib import pyplot as plt
import numpy as np

class Game:
    def __init__(self, levels):
        # Get a list of strings as levels
        # Store level length to determine if a sequence of action passes all the steps

        self.levels = levels
        self.current_level_index = -1
        self.current_level_len = 0
    
    def load_next_level(self):
        self.current_level_index += 1
        self.current_level_len = len(self.levels[self.current_level_index])
    
    def initial_population(self):
        initial_actions = []
        for i in range(200):
            sequence = []
            choices = ['0', '0', '0', '1', '2']
            for j in range(self.current_level_len - 1):
                randomAction = random.choice(choices)
                sequence.append(randomAction)
            initial_actions.append(sequence)
        return initial_actions
                
    def get_score(self, actions):
        # Get an action sequence and determine the steps taken/score
        # Return a tuple, the first one indicates if these actions result in victory
        # and the second one shows the steps taken

        current_level = self.levels[self.current_level_index]
        steps = 0
        score = 0
        win = True
        mushroomCount = 0
        maxMushroomCount = 0
        killedGumpa = 0
        maxKilledGumpa = 0
        for i in range(self.current_level_len - 1):
            current_step = current_level[i]
            # count eaten mushrooms
            if(current_step == 'M' and (actions[i-1] == '2' or actions[i-1] == '0')):
                mushroomCount += 1
            if (current_step == '_'):
                steps += 1
            elif (current_step == 'G' and actions[i - 1] == '1'):
                steps += 1
            elif (current_step == 'G' and actions[i-2] == '1'):
                steps += 1
                killedGumpa += 1
            elif (current_step == 'L' and actions[i - 1] == '2'):
                steps += 1
            else: # lose
                if(steps > score):
                    score = steps
                    maxMushroomCount = mushroomCount
                    maxKilledGumpa = killedGumpa
                mushroomCount = 0
                killedGumpa = 0
                steps = 0
                win = False
        if(steps > score):
            score = steps
            maxMushroomCount = mushroomCount
            maxKilledGumpa = killedGumpa
            score += (2*maxMushroomCount)
            score += (2*maxKilledGumpa)
        
        if (win):
            score += 10
            if(actions[self.current_level_len-2] == '1'):
                score += 1
        
        return score
    
    def map_actions_to_scores(self, actionsList):
        scores = []
        for actions in actionsList:
            scores.append(self.get_score(actions))
        return scores
    
    def sort(self, actionsList, scores):
        for i in range(len(actionsList)):
            for j in range(0, len(actionsList)-i-1):
                if(scores[j] > scores[j+1]):
                    temp = scores[j]
                    scores[j] = scores[j + 1]
                    scores[j+1] = temp
                    temp = actionsList[j]
                    actionsList[j]=actionsList[j+1]
                    actionsList[j+1]=temp
        return actionsList, scores
    def get_choice(self, actionsList, scores):
        r = random.randint(0, sum(scores))
        for j in range(len(actionsList)):
            if(r > scores[j]):
                r -= scores[j]
            else:
                return j
                
                
    def choice(self, actionsList, scores, num):
        choices, choicesScores = self.sort(actionsList,scores)
        return choices[0:100], choicesScores[0:100]
                    
    def combine(self, actionsList, scores, count):
        children = []
        for i in range(count//2):
            parent1 = actionsList[self.get_choice(actionsList, scores)]
            parent2 = actionsList[self.get_choice(actionsList, scores)]
            child1 = parent1[0: len(parent1)//2]
            child1.extend(parent2[len(parent1)//2:len(parent1)])
            
            child2 = parent2[0: len(parent1)//2]
            child2.extend(parent1[len(parent1)//2:len(parent1)])
            
            children.append(child1)
            children.append(child2)
        return children
                 
    def jump(self, children):
        for child in children:
            for i in range(len(child)):
                jump = random.uniform(0,1)
                if jump<0.1:
                    choices = ['0', '1', '2']
                    if child[i] not in choices:
                        print(child[i])
                    choices.remove(child[i])
                    child[i] = random.choice(choices)
                else:
                    break
        return children
            
    def average_score(self, actionsList):
        avg = 0
        for actionList in actionsList:
            avg += self.get_score(actionList)
        avg /= len(actionsList)
        return avg
        
            
    def genetic_algorithm(self):
        initialPopulation = self.initial_population()
        initialScores = self.map_actions_to_scores(initialPopulation)
        
        # sortedPopulation, sortedScores = self.sort(initialPopulation, initialScores)
        parentsList, parentsScores = self.choice(initialPopulation, initialScores, 100)
        count = 0
        avgList = [sum(initialScores) / len(initialScores)]
        minList = [min(initialScores)]
        maxList = [max(initialScores)]
        while True:
            if count == 10:
                break
            # baztarkibi
            children = self.jump(self.combine(parentsList, parentsScores, 100))
            parentsList.extend(children)
            initialPopulation = parentsList
            initialScores = self.map_actions_to_scores(initialPopulation)
            avgList.append(sum(initialScores)/len(initialScores))
            minList.append(min(initialScores))
            maxList.append(max(initialScores))
            parentsList, parentsScores = self.choice(initialPopulation, initialScores, 100)
            count += 1
            # jahesh 
        self.plot(avgList, minList, maxList)
        
    def plot(self, avgScores, minScores, maxScores):
        mean_scores = np.array(avgScores)
        max_scores = np.array(maxScores)
        min_scores = np.array(minScores)
        plt.title('level ' + str(self.current_level_index + 1))
        plt.plot(mean_scores)
        plt.plot(max_scores)
        plt.plot(min_scores)
        plt.show()
        return
        
        
        
        
    

g = Game(["__M_____", "____G_____", "__G___L_", "__G__G_L___", # 1, 2, 3, 4
          "____G_ML__G_", "____G_MLGL_G_", "_M_M_GM___LL__G__L__G_M__", # 5, 6, 7
          "____G_G_MMM___L__L_G_____G___M_L__G__L_GM____L____", # 8
          "___M____MGM________M_M______M____L___G____M____L__G__GM__L____ML__G___G___L___G__G___M__L___G____M__", # 9
          "_G___M_____LL_____G__G______L_____G____MM___G_G____LML____G___L____LMG___G___GML______G____L___MG___" # 10
          ])
for i in range(len(g.levels)):
    g.load_next_level()
    g.genetic_algorithm()   
