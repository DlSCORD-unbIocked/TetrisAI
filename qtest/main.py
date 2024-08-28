import gymnasium as gym
import numpy as np
import pandas as pd

env = gym.make("MountainCar-v0", render_mode="human")

num_states = 40
num_actions = 3
q_table = np.zeros([num_states, num_states, num_actions])

learning_rate = 0.1
discount_factor = 0.99
epsilon = 0.1
num_episodes = 1000


def discretize_state(state):
    pos_bins = pd.cut(
        [env.observation_space.low[0], env.observation_space.high[0]],
        bins=num_states,
        retbins=True,
    )[1][1:-1]
    vel_bins = pd.cut(
        [env.observation_space.low[1], env.observation_space.high[1]],
        bins=num_states,
        retbins=True,
    )[1][1:-1]

    pos_disc = np.digitize(state[0], pos_bins)
    vel_disc = np.digitize(state[1], vel_bins)
    return pos_disc, vel_disc


for episode in range(num_episodes):
    state, _ = env.reset()
    done = False
    total_reward = 0
    steps = 0

    while not done:

        if np.random.random() < epsilon:
            action = env.action_space.sample()
        else:
            disc_state = discretize_state(state)
            action = np.argmax(q_table[disc_state])

        new_state, reward, done, _, _ = env.step(action)

        disc_state = discretize_state(state)
        disc_new_state = discretize_state(new_state)

        best_next_action = np.argmax(q_table[disc_new_state])
        td_target = (
                reward + discount_factor * q_table[disc_new_state + (best_next_action,)]
        )
        td_error = td_target - q_table[disc_state + (action,)]
        q_table[disc_state + (action,)] += learning_rate * td_error

        state = new_state
        total_reward += reward
        steps += 1

    print(
        f"Episode: {episode + 1}, Steps: {steps}, Total Reward: {total_reward:.2f}, Final Position: {state[0]:.2f}"
    )

state, _ = env.reset()
done = False
total_reward = 0
steps = 0

while not done:
    disc_state = discretize_state(state)
    action = np.argmax(q_table[disc_state])
    state, reward, done, _, _ = env.step(action)
    total_reward += reward
    steps += 1

print("\nFinal Evaluation:")
print(
    f"Steps: {steps}, Total Reward: {total_reward:.2f}, Final Position: {state[0]:.2f}"
)

env.close()
