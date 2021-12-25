import csv
from typing import List
import pdb

class FileWrapper:
  @staticmethod
  def read(path: str) -> List[float]:
    with open(path, newline='') as csvfile:
     reader = csv.reader(csvfile, delimiter=',')
     rows = []
     for row in reader:
       row_res = []
       for i in row:
         row_res.append(float(i))
       rows.append(row_res)
     return rows
  
  @staticmethod
  def write(path: str, weights: List[float]) -> None:
    with open(path, 'w', newline='') as csvfile:
      writer = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_NONE)
      writer.writerow(weights)
