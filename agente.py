import torch
import random
import numpy as np
from collections import deque


from juego import Juego
from modelo import LinearNet,Trainer

MAX_MEMORY = 15_000
BATCH_SIZE = 1000
LR = 0.001

class Agente:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY) #Estructura de datos de la memoria 
        
        self.modelo = LinearNet(3,40,3)
        self.trainer = Trainer(self.modelo,LR,self.gamma)
    
    def obtener_estado(self,game):
        x_jug = game.j1.rect.x
        
        x_gom = game.g.rect.x
        y_gom = game.g.rect.y
        
        state = [x_jug,x_gom,y_gom]

        return state
    
    def recordar(self,state,action,reward,next_state,terminal):
        self.memory.append((state,action,reward,next_state,terminal))
    
    def entrenar_solo(self,state,action,reward,next_state,terminal):
        self.trainer.train(state,action,reward,next_state,terminal)

    def entrenar_lote(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory,BATCH_SIZE) 
        else:
            mini_sample = self.memory
        
        states,actions,rewards,next_states,terminales = zip(*mini_sample)
        self.trainer.train(states,actions,rewards,next_states,terminales)
    
    def obtener_action(self,state):
        self.epsilon = 1 - self.n_games/300
        final_move = [0,0,0]
        if random.randrange(0,1) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state_t = torch.tensor(state,dtype=torch.float)
            
            prediction = self.modelo(state_t)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        
        
        return final_move

def train():
    juego = Juego()
    agente = Agente()
    record = 0
    
    while True:
        state = agente.obtener_estado(juego)
        
        action = agente.obtener_action(state)
        reward, score, terminal, end = juego.paso(action)
        
        next_state = agente.obtener_estado(juego)
        
        agente.entrenar_solo(state,action,reward,next_state,terminal)
        
        agente.recordar(state,action,reward,next_state,terminal)
        
        if end:
            agente.n_games += 1
            agente.entrenar_lote()
            
            if score > record:
                record = score
                #model save
            
            print('Game: ',agente.n_games, ' Score: ',score,' Record: ',record)
            juego.score = 0
            
if __name__ == '__main__':
    train()