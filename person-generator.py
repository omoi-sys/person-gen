'''
Name: Abraham Serrato Meza
Project: Person Generator proof-of-concept
Class: CS361 Winter 2021: Software Engineering I
'''

from tkinter import *
import random
import sys
import os
from time import sleep

num_to_generate = 0     # Number of addresses to generate
state_index = 0            # Position in list for state selected
address_list = []       # List of addresses that are generated
content_lines = []       # data from Content Generator

# Global lists of state names in long  and short form.
states_long = ['Alaska', 'Arizona', 'California', 'Colorado', 'Hawaii', 
            'Idaho', 'Montana', 'New Mexico', 'Nevada', 'Oregon', 'Utah', 
            'Washington', 'Wyoming']

states_short = ['ak', 'az', 'ca', 'co', 'hi', 'id', 'mt', 
                'nm', 'nv', 'or', 'ut', 'wa', 'wy']

# Dictionary of states with key as their long name and the abbreviated form
# as the value. 
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

state_data_lengths = {
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

##############################################################################
# Function: save_lines()
# Purpose:  This function saves the lines that match line indexes.
##############################################################################
def save_lines(line_indexes):
    global address_list
    file = open(state_filename_dict[states_long[state_index]] + '.csv')

    # Match lines to indexes and saved in one of two formats
    # Method for enumerating lines adapted from: https://stackoverflow.com/questions/2081836/reading-specific-lines-only
    for i, line in enumerate(file):
        if i == line_indexes[0]:
            current_addr = line.split(',')
            if current_addr[4] == '': # If UNIT field is empty, don't added it
                # 2: NUMBER, 3: STREET, 5: CITY, 8: POSTCODE
                address_list.append(current_addr[2] + " " + current_addr[3] \
                + " " + current_addr[5] + " " + current_addr[8])
            else:
                # 2: NUMBER, 3: STREET, 4: UNIT, 5: CITY, 8: POSTCODE
                address_list.append(current_addr[2] + " " + current_addr[3] \
                + " " + current_addr[4] + " "+ current_addr[5] + " " + current_addr[8])

            line_indexes.pop(0)

        if len(line_indexes) == 0:
            break

    file.close()
    output = open('pg_output.csv', 'w')
    output.write('input_state, input_number_to_generate, output_content_type, output_content_value\n')
    for i in range(0, len(address_list)):
        output.write(states_long[state_index] + ',' + str(num_to_generate) \
        + ',' + 'street address,' + address_list[i] + '\n')


##############################################################################
# Function: generate_addresses()
# Purpose:  This function generates addresses by generating random numbers
#           in the range of 1 to the number of lines in a csv file and then 
#           saving corresponding lines in a list and output csv file.
##############################################################################
def generate_addresses():
    global address_list
    line_indexes = []
    address_list = [] # reset list
    random.seed()
    count = 0
    file_size = state_data_lengths[state_filename_dict[states_long[state_index]]]
    while(count < num_to_generate):
        random_line = random.randrange(1, file_size)
        if random_line not in line_indexes:
            line_indexes.append(random_line)
            count = count + 1

    line_indexes.sort()
    save_lines(line_indexes)


##############################################################################
# Function: skip_GUI()
# Purpose:  Skips creating a GUI and will simply read the input file and then
#           call generate_addresses() to get the addresses in output.csv.
##############################################################################
def skip_GUI(input_argument):
    global num_to_generate
    global state_index

    infile_lines = []
    input_file = open(input_argument, 'r')
    for i in input_file:
        infile_lines.append(i)

    # Ignore headers
    input_values = infile_lines[1].split(',')
    num_to_generate = int(input_values[1])

    # check for state match
    for index in range(0, 13):
        if states_long[index].lower() == input_values[0].lower() \
        or states_short[index] == input_values[0].lower():
            state_index = index

    generate_addresses()


##############################################################################
# Function: make_content_input():
# Purpose:  Makes the input file to be used by Content Generator.
##############################################################################
def make_content_input():
    # make input file for Content Generator
    congen_infile = open('cg_input.csv', 'w')
    congen_infile.write('input_keywords\n')
    congen_infile.write(states_long[state_index] + ';climate')
    congen_infile.close()


##############################################################################
# Function: get_content_data():
# Purpose:  Gets the content from the output file made by Content Generator.
##############################################################################
def get_content_data():
    cgen_output = open('output.csv', 'r')
    content_lines = []
    for line in cgen_output:
        content_lines.append(line.split(';'))
    cgen_output.close()
    return content_lines


##############################################################################
# Function: format_content(content_lines):
# Purpose:  Format line passed into separate ones to fit the content frame.
##############################################################################
def format_content(content_lines):
    # format text
    temp_cont = ''
    for i in range(len(content_lines[1][1])):
        if (i % 70 == 0):
            temp_cont += '\n'
        else:
            temp_cont += content_lines[1][1][i]
    return temp_cont


##############################################################################
# Function: generate_content()
# Purpose:  Gets and injects content obtained by another microservice into
#           the GUI.
##############################################################################
def generate_content():
    make_content_input()
    # Start the Content Generator
    os.system("python3 content-generator.py cg_input.csv")
    
    content_lines = get_content_data()
    formatted_cont = format_content(content_lines)

    personGUI.content_data.set('Climate in ' + content_lines[1][0] + '\n' + formatted_cont)
    # check to see if content displayed is empty before insertng it to GUI
    if personGUI.content_data.get() != ' ':
        personGUI.content_text.delete('1.0', 'end')
    personGUI.content_text.insert(INSERT, personGUI.content_data.get())


##############################################################################
# Function: get_addr_list()
# Purpose:  Get the addresses and add them to the list of addresses displayed 
#           in the GUI.
##############################################################################
def get_addr_list():
    global state_index
    global num_to_generate

    # get the position of the state selected by user on GUI
    state_index = int(personGUI.state_listbox.curselection()[0])
    num_to_generate = int(personGUI.user_num_input.get())

    # Reset values
    personGUI.display_list.delete(0, 'end')
    generate_addresses()

    # Update addresses
    for i in range(0, num_to_generate):
        personGUI.display_list.insert(i, address_list[i])

    generate_content()


class GUI:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("600x900")
        self.state_listbox = Listbox()
        self.display_list = Listbox()
        self.user_num_input = Entry()
        self.content_frame = Frame()
        self.content_data = StringVar()
        self.content_text = Text()

    # start the GUI message
    def build_GUI(self, message):
        instruction = Label(text = message)
        instruction.pack(side = 'top')

    # make the state list box
    def build_state_list(self, state_list):
        self.state_listbox = Listbox(self.window, width = '70', height = '13')
        # Insert states into the first listbox container
        for index in range(0, 13):
            self.state_listbox.insert(index, state_list[index])
        self.state_listbox.pack()

    # make the address list box
    def build_address_list(self, address_list):
        self.display_list = Listbox(self.window, width = '70', height = '15')
        self.display_list.pack(side = 'top')

    # make the entry box
    def generate_entry(self):
        prompt_warning = 'Number of addresses to generate.\n' +\
                  'The larger the number, the longer it will take.'
        num_input_ask = Label(text = prompt_warning)
        num_input_ask.pack()
        self.user_num_input = Entry(self.window, width = 20)
        self.user_num_input.insert(0, '')
        self.user_num_input.pack(padx = 5, pady = 5)

    # make the generate button
    def build_button(self):
        bttn = Button(self.window, text = 'Generate', command = get_addr_list)
        bttn.pack(side = 'top')

    # make the content box
    def build_content(self):
        self.content_frame = Frame(self.window)
        self.content_data = StringVar()
        self.content_data.set(' ')
        self.content_text = Text(self.content_frame, width = '70', height = '15')
        self.content_text.insert(INSERT, self.content_data.get())
        self.content_text.pack(side = 'right')
        self.content_frame.pack()

    # create the GUI
    def mainloop(self):
        self.window.mainloop()


if __name__ == '__main__':
    # Skip GUI if input file is passed when starting program
    if (len(sys.argv) > 1):
        skip_GUI(sys.argv[1])

    else:
        message = "Welcome to Person Generator\n" + \
                  "Please select which state you would like to generate addresses for.\n" + \
                  "Please make sure the state is highlighted otherwise nothing will be generated.\n"
        # start the GUI and its various components
        personGUI = GUI()
        personGUI.build_GUI(message)
        personGUI.build_state_list(states_long)
        personGUI.generate_entry()
        personGUI.build_button()
        personGUI.build_address_list(address_list)
        personGUI.build_content()
        personGUI.mainloop()
