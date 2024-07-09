import numpy as np
import random as rm
import itertools
import math

class FirstOrderMarkovModel(object):

    def __init__(self, states, initial_state, steps, weight="random", simulate=True, n_sim=1000):
        self.states = states
        self.initial_state = initial_state
        self.steps = steps
        self.state_size = len(states)

        state_product = list(itertools.product(self.states, repeat=2))
        state_product = [s[1] for s in state_product]
        state_transition_matrix = [state_product[i*self.state_size:(i+1)*self.state_size] for i in range(self.state_size)]

        self.transition_matrix = {}
        for i in range(self.state_size):
            if weight == "equal":
                p = {state:1 / self.state_size for state in states}
            elif weight=="random":
                try:
                    p = self.random_weight(self.state_size)
                except ValueError:
                    #if the probabilities sum to one before last val, we
                    #error out and try again
                    p = self.random_weight(self.state_size)
            else:
                e = "Specify either equal or random weights"
                raise AttributeError(e)
            self.transition_matrix[states[i]] = p

        self.probs = self.initialize_probability()

        if simulate:
            self.simulation = []
            for i in range(n_sim):
                self.simulation.append(self.find_trajectory())

    def random_weight(self, n):
        p = {}
        prob_sum = 0
        for j in range(n):
            if j == self.state_size - 1:
                prob = 100 - prob_sum
            else:
                prob = rm.randrange(1, 100 - prob_sum)
            prob_sum += prob
            p[self.states[j]] = (prob/100)
        return p

    def transition_probability(self, t, probs):
        probs[t] = {state:0 for state in self.states}
        for prior_state, possible in self.transition_matrix.items():
            for current_state, p in possible.items():
                probs[t][current_state] += probs[t-1][prior_state] * p
        return probs

    def initialize_probability(self):
        probs = {0:{state:0 for state in self.states}}
        probs[0][self.initial_state] = 1
        t = 1
        while t <= self.steps:
            probs = self.transition_probability(t, probs)
            t += 1
        return probs

    def find_trajectory(self):
        trajectory = []
        for i in range(self.steps):
            cpt = self.probs[i]
            trajectory.append(np.random.choice(list(cpt.keys()), replace=True, p=list(cpt.values())))
        return trajectory
