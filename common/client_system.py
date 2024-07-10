#!/usr/bin/env python3

import time
from . import utils
from .client import Client
from threading import Thread, Lock as threading_lock

#create backup components
client_database_backup = []

#function to create and store a new client
def create_client(client_shared_queue):
  #create delay for simulation
  with threading_lock():
    #generate new client entry
    numbers = utils.get_ticket_structure()

    curr_client = Client(numbers)
    #append to backup list
    client_database_backup.append(curr_client.data_as_arr)
    client_shared_queue.append(curr_client.ticket_data)
    #notify new client entry
    print(
      f"NEW ENTRY - ID: {str(curr_client.ticket_id)} saved successfully!\n")


#structure list to be sent to the server
def create_list(shared_client_queue, client_amount, save_file_path):
  #create thread list
  threads = []

  #create one thread for each client
  for index in range(client_amount):
    x = Thread(target=create_client,
               args=(shared_client_queue, ),
               name="cl_entry_thread")
    threads.append(x)
    x.start()

  #pause main thread waiting for entries
  for thread in threads:
    thread.join()

  #save to be able to recover the game later
  utils.save_to_file([client_database_backup], save_file_path)


def define_winner(shared_queue, save_file_path):
  time.sleep(0.5)
  print("DRAWING WINNER", end="")
  time.sleep(0.5)

  winners = []
  while len(shared_queue):
    winners.append(shared_queue.pop())

  utils.save_to_file(winners if len(winners) else [-1], save_file_path)

  #if there is any winners
  if len(winners):
    #list the ticket id because numbers match
    for ticket_number_data in winners:
      winner_id = find_client_by_ticket_num(ticket_number_data[0])

      congrats_message = f"\n\nThe client with ticket ID {str(winner_id)} and numbers {ticket_number_data} won the EuroMillion "

      #check for jackpot
      if ticket_number_data[1]:
        print(congrats_message.join(" AND GOT THE JACKPOT!"))
      else:
        print(congrats_message)
  else:
    print("\n\nNo one won the EuroMillion this time, keep gambling!\n")


def find_client_by_ticket_num(ticket_number):

  if not client_database_backup:
    print("Error: Server backup file is empty!\n")

  #search for a valid match
  if ticket_number in client_database_backup:
    index = client_database_backup.index(ticket_number)
    #return [self.ticket_id, self.ticket_data]
    return client_database_backup[index]

  print(f"Couldnt find anyone with ticket number {ticket_number}!\n")
  #else return not valid
  return -1
