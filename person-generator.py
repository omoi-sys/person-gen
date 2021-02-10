import tkinter
import random

address_lines = []

file = open("addresses/ca.csv")
for i, line in enumerate(file):
    address_lines.append(line)

print(address_lines[134544].split(','))
new_one = address_lines[134544].split(',')

print(new_one[2] + " " + new_one[3] + " " + new_one[4] + ", " + new_one[5] + " " + new_one[8])
print("Done")