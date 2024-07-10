#!/usr/bin/env python3
import multiprocessing

from common.utils import load_old_game_state
from common import client_system
from common.server import Server

logo = """

,------.                      ,--.   ,--.,--.,--.,--.,--.              
|  .---',--.,--.,--.--. ,---. |   `.'   |`--'|  ||  |`--' ,---. ,--,--,  
|  `--, |  ||  ||  .--'| .-. ||  |'.'|  |,--.|  ||  |,--.| .-. ||      \ 
|  `---.'  ''  '|  |   ' '-' '|  |   |  ||  ||  ||  ||  |' '-' '|  ||  | 
`------' `----' `--'    `---' `--'   `--'`--'`--'`--'`--' `---' `--''--' 
                                                          Ricardo - 2023 
"""

if __name__ == "__main__":
  print(logo)

  #setup basic properties
  client_amount = 20
  log_file_name = "log"

  try:
    load_old_game_state(log_file_name)

  except FileNotFoundError:
    # else create new game
    manager = multiprocessing.Manager()
    number_shared_lst = manager.list()
    processes = []

    #start by declaring client process
    list_system_process = multiprocessing.Process(target=client_system.create_list,
                                     args=(number_shared_lst,client_amount,log_file_name,))

    processes.append(list_system_process)

    #declare and start server process
    server = Server()

    server_process = multiprocessing.Process(target=server.run,
                                args=(number_shared_lst, log_file_name))
    processes.append(server_process)

    #start client process and wait
    list_system_process.start()
    list_system_process.join()

    #start server process and wait
    server_process.start()
    server_process.join()

    client_system.define_winner(
      number_shared_lst,
      log_file_name,
    )

    #terminate process and free process handle
    for process in processes:
      process.terminate()
      process.close()
