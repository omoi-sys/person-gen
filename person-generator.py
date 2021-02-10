import tkinter
import random
import sys

num_to_generate = 10
input_argument = ""

# name of inputfile in case of input csv file passed as an argument when initiating program
if (len(sys.argv) > 1):
    input_argument = sys.argv[1]

data_lengths = {
    "ak": 12,
    "az": 12,
    "ca": 1222,
    "co": 12,
    "hi": 12,
    "id": 12,
    "mt": 12,
    "nm": 12,
    "nv": 12,
    "or": 12,
    "ut": 12,
    "wa": 12,
    "wy": 12
}

line_nums = []

random.seed()

for i in range(10):
    line_nums.append(random.randrange(1, data_lengths["ca"]))

line_nums.sort()
print(line_nums)

address_lines = []

file = open("addresses/ca.csv")
for i, line in enumerate(file):
    if i == line_nums[0]:
        address_lines.append(line)
        line_nums.pop(0)
    if len(line_nums) == 0:
        break

file.close()

for i in range(0, len(address_lines)):
    print(address_lines[i].split(','))
    new_one = address_lines[i].split(',')
    print(new_one[2] + " " + new_one[3] + " " + new_one[4] + ", " + new_one[5] + " " + new_one[8])

print("Done")