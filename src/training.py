import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
from collections import deque
from environment import Env
from tqdm import trange
from dqn import DQN

# Hyperparameters
GAMMA = 0.99
EPSILON_START = 1.0
EPSILON_END = 0.05
EPSILON_DECAY = 0.995
LR = 1e-4
BATCH_SIZE = 64
TARGET_UPDATE = 10
MEMORY_SIZE = 100_000
NUM_EPISODES = 100
MAX_STEPS = 500

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Environment
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
env = Env(SCREEN_WIDTH, SCREEN_HEIGHT)
state_size = len(env.get_state())
action_size = 1 + 3 * 10  # 1 for launch, 3 per rocket


# Memory
memory = deque(maxlen=MEMORY_SIZE)

# Networks
policy_net = DQN(state_size, action_size).to(device)
target_net = DQN(state_size, action_size).to(device)
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

optimizer = optim.Adam(policy_net.parameters(), lr=LR)

# Utils
def select_action(state, epsilon):
    if random.random() < epsilon:
        return random.randint(0, action_size - 1)
    with torch.no_grad():
        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(device)
        q_values = policy_net(state_tensor)
        return torch.argmax(q_values).item()

def replay():
    if len(memory) < BATCH_SIZE:
        return

    batch = random.sample(memory, BATCH_SIZE)
    states, actions, rewards, next_states, dones = zip(*batch)

    states = torch.FloatTensor(states).to(device)
    actions = torch.LongTensor(actions).unsqueeze(1).to(device)
    rewards = torch.FloatTensor(rewards).unsqueeze(1).to(device)
    next_states = torch.FloatTensor(next_states).to(device)
    dones = torch.FloatTensor(dones).unsqueeze(1).to(device)

    q_values = policy_net(states).gather(1, actions)
    next_q_values = target_net(next_states).max(1)[0].unsqueeze(1)
    target_q = rewards + (GAMMA * next_q_values * (1 - dones))

    loss = nn.MSELoss()(q_values, target_q)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

# Training loop with tqdm
epsilon = EPSILON_START
episode_bar = trange(NUM_EPISODES, desc="Training", unit="ep")

for episode in episode_bar:
    state = env.reset()
    total_reward = 0

    for t in range(MAX_STEPS):
        action = select_action(state, epsilon)
        next_state, reward, done, _ = env.execute_action(action)

        memory.append((state, action, reward, next_state, done))
        state = next_state
        total_reward += reward

        replay()

        if done:
            break

    epsilon = max(EPSILON_END, epsilon * EPSILON_DECAY)

    if episode % TARGET_UPDATE == 0:
        target_net.load_state_dict(policy_net.state_dict())

    episode_bar.set_postfix(reward=total_reward, epsilon=epsilon)

# Save model
torch.save(policy_net.state_dict(), "dqn_defense_model.pth")
