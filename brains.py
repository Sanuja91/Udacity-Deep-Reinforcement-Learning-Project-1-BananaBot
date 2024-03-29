""" Contains a variety of neural network architectures to use on the problem"""
import torch
import torch.nn as nn
import torch.nn.functional as F


class VanillaDQN(nn.Module):
    """Standard Vanilla DQN Brain"""
    
    def __init__(self, state_size, action_size, seed, fc1_units=64, fc2_units=64):
        """Initialize parameters and build the model
        
        Params
        ===========
            state_size (int): Dimension of each state
            action_size (int): Dimension of each action
            seed (int): Random Seed
            fc1_units (int): Number of nodes in first hidden layer
            fc2_units (int): Number of nodes in second hidden layer
        """
        super(VanillaDQN, self).__init__()
        self.seed = torch.manual_seed(seed)
        self.state_size = state_size
        self.action_size = action_size  
        self.fc1 = nn.Linear(state_size, fc1_units)
        self.fc2 = nn.Linear(fc1_units, fc2_units)
        self.fc3 = nn.Linear(fc2_units, action_size)
        
    def forward(self, state):
        """Build a network that maps state -> action values"""
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))
        return self.fc3(x)
    

class DuelingDQN(nn.Module):
    """Dueling DQN Brain"""

    def __init__(self, state_size, action_size, seed, fc1_units=64, fc2_units=64):
        """Initialize parameters and build the model
                
        Params
        ===========
            state_size (int): Dimension of each state
            action_size (int): Dimension of each action
            seed (int): Random Seed
            fc1_units (int): Number of nodes in first hidden layer
            fc2_units (int): Number of nodes in second hidden layer
        """
        super(DuelingDQN, self).__init__()
        self.seed = torch.manual_seed(seed)
        self.state_size = state_size
        self.action_size = action_size 

        self.fc1 = nn.Linear(state_size, fc1_units)
        
        self.fc2_adv = nn.Linear(fc1_units, fc2_units)
        self.fc2_val = nn.Linear(fc1_units, fc2_units)

        self.fc3_adv = nn.Linear(fc2_units, 1)
        self.fc3_val = nn.Linear(fc2_units, action_size)

    def forward(self, state):
        """Build a network that maps state -> action values"""
        x = F.relu(self.fc1(state))
        
        adv = F.relu(self.fc2_adv(x))
        val = F.relu(self.fc2_val(x))
        
        adv = self.fc3_adv(adv)
        val = self.fc3_val(val)
        
        return val + adv - adv.mean()