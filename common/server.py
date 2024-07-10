#!/usr/bin/env python3
import threading
from dataclasses import dataclass
from . import utils
import time


@dataclass
class Server:

  def __init__(self):
    self.clients = []
    self.results = []
    self.draw_condition = threading.Condition()
    self.lock = threading.Lock()
    self.results_event = threading.Event()

  def accept_player(self, list):
    with self.lock:
      self.clients.append(list)

  #TO DO: THIS IS THE LAST THING, JUST CHECK THEM PLEASE
  def check_results(self, shared_queue):
    JACKPOT = True
    with self.lock:
      for player_numbers in self.clients:
        #match player number
        #0 = 5 digits
        #1 = 2 stars
        if player_numbers[0] == self.results[0]:
          #check for jackpot by checking stars
          if player_numbers[1] == self.results[1]:
            shared_queue.put([player_numbers, JACKPOT])
            return
          shared_queue.put([player_numbers, not JACKPOT])

  def draw_numbers(self, save_file_path):
    with self.draw_condition:
      if not self.results:
        self.results = utils.get_ticket_structure()
        utils.save_to_file(self.results, save_file_path)
        time.sleep(0.5)
        print(f"\nTICKET WINNER: {self.results}\n")
        self.results_event.set()  # Notify waiting clients

  def run(self, shared_queue, save_file_path):
    threads = []

    while len(shared_queue):
      thread = threading.Thread(target=self.accept_player,
                                args=(shared_queue.pop(), ))
      threads.append(thread)
      thread.start()

    for thread in threads:
      thread.join()

    self.draw_numbers(save_file_path)
    self.results_event.wait()

    self.check_results(shared_queue)
