import gym
import numpy as np

env = gym.make("MountainCar-v0")

state_space = (env.observation_space.high - env.observation_space.low) * np.array([10, 100])
state_space = np.round(state_space, 0).astype(int) + 1
q_table = np.random.uniform(low=-2, high=0, size=(state_space[0], state_space[1], env.action_space.n))

learning_rate = 0.1
discount_factor = 0.99
epsilon = 1.0
epsilon_decay = 0.995
min_epsilon = 0.01
num_episodes = 10000


def discretize_state(state):
    discrete_state = (state - env.observation_space.low) * np.array([10, 100])
    return tuple(np.round(discrete_state, 0).astype(int))


for episode in range(num_episodes):
    state = discretize_state(env.reset())
    done = False
    while not done:
        if np.random.random() < epsilon:
            action = np.random.randint(0, env.action_space.n)
        else:
            action = np.argmax(q_table[state])

        next_state, reward, done, _ = env.step(action)
        next_state = discretize_state(next_state)

        if done and next_state[0] >= env.goal_position:
            q_table[state][action] = reward
        else:
            q_table[state][action] = (1 - learning_rate) * q_table[state][action] + \
                                     learning_rate * (reward + discount_factor * np.max(q_table[next_state]))

        state = next_state

    epsilon = max(min_epsilon, epsilon * epsilon_decay)

policy = np.argmax(q_table, axis=2)

state = discretize_state(env.reset())
done = False
while not done:
    action = policy[state]
    state, reward, done, _ = env.step(action)
    env.render()

env.close()
