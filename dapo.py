# -*- coding: utf-8 -*-
"""DAPO.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13zpyj-6RgPgMGn8Cllbwyb5DegfBDQ_C
"""

import numpy as np

# Dummy reward model (R)

def dummy_reward_model(output):
  """A simple reward model for demonstration."""
  if "good" in output.lower():
    return 1.0
  else:
    return 0.0

# Dummy task prompts (D)

task_prompts = [
    "Write a short sentence with the word 'good'.",
    "Generate a sentence without the word 'good'.",
    "Compose a sentence that includes 'good things'."
]

# Hyperparameters

M = 10  # Number of training steps
G = 5   # Number of outputs sampled per question
N = 10  # Buffer size
mu = 3  # Number of policy update iterations
epsilon_low = 0.1
epsilon_high = 0.9

# Initilization policy model (πθ)
# For simplicity, we'll represent the policy as a probability distribution over words
# In a real scenario, this would be a neural network.
vocabulary = ["good", "bad", "things", "are", "the", "weather", "is", "nice"]
vocab_size = len(vocabulary)
policy_theta = np.ones(vocab_size) / vocab_size  # Initial uniform distribution

# Dynamic sampling buffer
dynamic_sampling_buffer = []

# DAPO Algorithm

for step in range(M):
   # 2: Sample a batch Db from D
    batch_size = min(3, len(task_prompts))  # Adjust batch size as needed
    Db = np.random.choice(task_prompts, size=batch_size, replace=False)

    # 3: Update the old policy model πθold <- πθ
    policy_theta_old = policy_theta.copy()

    # 4: Sample G outputs {oi}i=1~G ~ πθold(.|q) for each question q ∈ Db
    sampled_outputs = []
    rewards = []
    for question in Db:
        for _ in range(G):
            output_words = []
            while True:  # Generate a simple sentence
                word_index = np.random.choice(vocab_size, p=policy_theta_old)
                word = vocabulary[word_index]
                output_words.append(word)
                if len(output_words) >= 5: # simple sentence length limit
                    break
            output = " ".join(output_words)
            sampled_outputs.append(output)
            rewards.append(dummy_reward_model(output))

    # 6: Filter out oi and add the remaining to the dynamic sampling buffer (Dynamic Sampling Equation (11))
    for output, reward in zip(sampled_outputs, rewards):
        # Dummy Dynamic Sampling Equation (11) - Replace with your actual logic
        if np.random.rand() > epsilon_low:  # Simple filtering based on random threshold
            dynamic_sampling_buffer.append((output, reward))

    # 7: if buffer size nb < N: continue
    if len(dynamic_sampling_buffer) < N:
        continue

    # Trim the buffer if it exceeds N
    dynamic_sampling_buffer = dynamic_sampling_buffer[-N:]

    # 9: For each oi in the buffer, compute Âi,t for the t-th token of oi (Equation (9))
    advantages = []
    for output, reward in dynamic_sampling_buffer:
        # Dummy Advantage Calculation - Replace with your actual logic
        advantages.append(reward)  # Simple reward as advantage for demonstration

    # 10: for iteration = 1, ..., μ do
    for _ in range(mu):
        # 11: Update the policy model πθ by maximizing the DAPO objective (Equation (8))
        # Dummy Policy Update - Replace with your actual DAPO objective and optimization
        for output, advantage in zip(dynamic_sampling_buffer, advantages):
            if advantage > 0.5: #very simple update logic.
                for word in output[0].split():
                    if word in vocabulary:
                        word_index = vocabulary.index(word)
                        policy_theta[word_index] += 0.01  # Increase probability of "good" words

        # Normalize policy distribution
        policy_theta /= np.sum(policy_theta)

# Output (πθ)
print("Final Policy Model (πθ):", policy_theta)
print("Vocabulary:", vocabulary)