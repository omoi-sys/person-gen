from tkinter import *
import random
import sys

num_to_generate = 0
input_argument = ""
state_id = 0

# name of inputfile in case of input csv file passed as an argument when initiating program
if (len(sys.argv) > 1):
    input_argument = sys.argv[1]

state_list = ['Alaska', 'Arizona', 'California', 'Colorado', 'Hawaii', 
            'Idaho', 'Montana', 'New Mexico', 'Nevada', 'Oregon', 'Utah', 
            'Washington', 'Wyoming']

state_filename_dict = {
    'Alaska': 'ak', 
    'Arizona': 'az', 
    'California': 'ca', 
    'Colorado': 'co', 
    'Hawaii': 'hi', 
    'Idaho': 'id', 
    'Montana': 'mt', 
    'New Mexico': 'nm', 
    'Nevada': 'nv', 
    'Oregon': 'or', 
    'Utah': 'ut', 
    'Washington': 'wa', 
    'Wyoming': 'wy'
}

# length of the data in the csv files dependencies - 1 since reading will
# start at "position 0"
data_lengths = {
    "ak": 292362,
    "az": 3512857,
    "ca": 13784521,
    "co": 2190263,
    "hi": 274329,
    "id": 836758,
    "mt": 614699,
    "nm": 888214,
    "nv": 1229069,
    "or": 2338677,
    "ut": 1116698,
    "wa": 4058176,
    "wy": 368400
}

def generate():
    global data_lengths
    line_nums = []

    random.seed()

    i = 0
    while(i < num_to_generate):
        rand_num = random.randrange(1, data_lengths[state_filename_dict[state_list[state_id]]])
        if rand_num in line_nums:
            continue
        else:
            line_nums.append(rand_num)
            i = i + 1

    line_nums.sort()
    print(line_nums)

    address_lines = []

    file = open(state_filename_dict[state_list[state_id]] + '.csv')

    # read lines from file
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

def retrieve():
    global state_id
    global num_to_generate
    state_id = int(listbox.curselection()[0])
    num_to_generate = int(user_num.get())
    generate()

window = Tk()
window.geometry("600x600")
frame = Frame(window)
frame.pack()
greeting = Label(text="Welcome to Person Generator\nPlease select which state you would like to generate addresses for.")
greeting.pack(side = 'top')

listbox = Listbox(window, width='80', height='13')

for i in range(0, 13):
    listbox.insert(i, state_list[i])

listbox.pack()
num_ask = Label(text='Number of addresses to generate (max 250)')
num_ask.pack()
user_num = Entry(window, width = 20)
user_num.insert(0, '')
user_num.pack(padx = 5, pady = 5)

bttn = Button(window, text = "Generate", command = retrieve)
bttn.pack(side = 'bottom')
window.mainloop()