#!/usr/bin/env python3
from dataclasses import dataclass

@dataclass
class Client:

  def __init__(self, input_data):
    self.ticket_id = id(input_data)
    self.ticket_numbers = input_data[0]
    self.ticket_special_numbers = input_data[1]
    self.ticket_data = [self.ticket_numbers,self.ticket_special_numbers]
    self.data_as_arr = self.ticket_id, self.ticket_data

  def __str__(self):
    return f"Ticket with id {self.ticket_data}, Numbers {self.ticket_numbers} and stars {self.ticket_special_numbers}"
