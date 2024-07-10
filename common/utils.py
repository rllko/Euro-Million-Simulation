#!/usr/bin/env python3
import random
import pickle
import os.path


# Data Saved during execution -> client array, server result arr, winner array
def save_to_file(data, file_name):
  with open(file_name, "ab+") as f:
    pickle.dump(data, f)


# Data Loaded in order -> client array, server result arr, winner array
def load_old_game_state(file_name):

  if os.path.exists(file_name):
    try:
      with open(file_name, "rb") as f:
        client_array = pickle.load(f)
        server_result = pickle.load(f)
        winner_arr = pickle.load(f)
      display_old_game_data(client_array, server_result, winner_arr)

    except EOFError:
      print("log data corrupted, please delete it")
  else:
    raise FileNotFoundError


def display_old_game_data(client_array, server_result, winners_arr):

  print("Log file found, Loading last game state\n")

  print("The available tickets are:")
  for client in client_array[0]:
    print(f"ID: {client[0]}\nNumber:{client[1]}")
  
  print(
    f"\nThe EuroMillion result was the numbers {server_result[0]} and stars {server_result[1]}\n"
  )

  if winners_arr[0] != -1:
    for winner in winners_arr:
      print(f"{winner[0]} won with the ticket {winner[1]}\n")
  else:
    print("There was no winners!\n")

  print(
    "Please come back on Monday to have a chance to win the EuroMillion!!\n")


def get_ticket_structure():
  #5 numbers, 2 stars
  return random.sample(range(1, 51), 5), random.sample(range(1, 12), 2)
