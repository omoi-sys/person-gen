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

# Global list of state names in long form. This list have multiple
# uses including in the GUI list to choose from and in the non-GUI
# generation.
states_long = ['Alaska', 'Arizona', 'California', 'Colorado', 'Hawaii', 
            'Idaho', 'Montana', 'New Mexico', 'Nevada', 'Oregon', 'Utah', 
            'Washington', 'Wyoming']

# Global list of states in their abbreviated form is fow use in
# the non-GUI generation with comparison purposes.
states_short = ['ak', 'az', 'ca', 'co', 'hi', 'id', 'mt', 
                'nm', 'nv', 'or', 'ut', 'wa', 'wy']

# Dictionary of states with key as their long name and the abbreviated form
# as the value. Main use is in generate_addresses() function.
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
# Function: save_lines
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
    while(count < num_to_generate):
        random_line = random.randrange(1, state_data_lengths[state_filename_dict[states_long[state_index]]])
        if random_line not in line_indexes: # skip already existing indexes
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
# Function: generate_content()
# Purpose:  Gets and injects content obtained by another microservice into
#           the GUI.
##############################################################################
def generate_content():
    global content_data # Data that is displayed about the state climate
    global content_textbox

    # make input file for Content Generator
    congen_infile = open('cg_input.csv', 'w')
    congen_infile.write('input_keywords\n')
    congen_infile.write(states_long[state_index] + ';climate')
    congen_infile.close()

    # Start the Content Generator
    os.system("python3 content-generator.py cg_input.csv")
    sleep(2) # wait a bit for the content generator to do its thing
    
    cgen_output = open('output.csv', 'r')
    content_lines = []
    for line in cgen_output:
        content_lines.append(line.split(';'))
    cgen_output.close()

    # format text
    temp_cont = ''
    for i in range(len(content_lines[1][1])):
        if (i % 70 == 0):
            temp_cont += '\n'
        else:
            temp_cont += content_lines[1][1][i]

    content_data.set('Climate in ' + content_lines[1][0] + '\n' + temp_cont)
    # check to see if content displayed is empty before insertng it to GUI
    if content_data.get() != ' ':
        content_textbox.delete('1.0', 'end')
    content_textbox.insert(INSERT, content_data.get())

##############################################################################
# Function: get_addr_list()
# Purpose:  Generate the list of addresses and save them into a global
#           variable display_list that will be pack()'d at the correct place 
#           outside the function. If pack() were called in the function, it
#           would create a new list underneath every time Generate is clicked.
##############################################################################
def get_addr_list():
    global state_index
    global num_to_generate
    global display_list
    global content_data     # Data that is displayed about the state climate
    global content_textbox  # Text box to update

    # get the position of the state selected by user on GUI
    state_index = int(state_listbox.curselection()[0])
    num_to_generate = int(user_num_input.get())

    # Reset values
    display_list.delete(0, 'end')
    generate_addresses()

    # Update addresses
    for i in range(0, num_to_generate):
        display_list.insert(i, address_list[i])

    generate_content()


if __name__ == '__main__':
    # Skip GUI if input file is passed when starting program
    if (len(sys.argv) > 1):
        skip_GUI(sys.argv[1])

    else:
        # Create the GUI window and greet user. I used the following tutorial
        # for learning how to make a GUI with Tkinter: https://coderslegacy.com/python/python-gui/python-tkinter-list-box/
        # and https://realpython.com/python-gui-tkinter/
        window = Tk()
        window.geometry("600x900")
        message = "Welcome to Person Generator\nPlease select which state you would like to generate addresses for.\n" + \
                "Please make sure the state is highlighted otherwise nothing will be generated.\n"
        greeting = Label(text=message)
        greeting.pack(side = 'top')

        # List of states
        state_listbox = Listbox(window, width='70', height='13')
        # List of addresses to be displayed
        display_list = Listbox(window, width='70', height='15')
        # Data from Content Generator
        CFrame = Frame(window)
        content_data = StringVar()
        content_data.set(' ')
        content_textbox = Text(CFrame, width='70', height='15')
        content_textbox.insert(INSERT, content_data.get())

        # Add scrollbar to Content data
        scroll = Scrollbar(CFrame, orient=VERTICAL, command=content_textbox.yview)

        # Insert states from states_long into the first listbox container
        for i in range(0, 13):
            state_listbox.insert(i, states_long[i])

        state_listbox.pack()  # Create list of states
        # Create entry area to enter the number of addresses to generate
        num_input_ask = Label(text='Number of addresses to generate (max 250)')
        num_input_ask.pack() 
        user_num_input = Entry(window, width = 20)
        user_num_input.insert(0, '') # Make sure entry area is empty
        user_num_input.pack(padx = 5, pady = 5)

        # Create button to press that calls get_addr_list() function
        bttn = Button(window, text = "Generate", command = get_addr_list)
        bttn.pack(side = 'top') # Display button at the bottom

        display_list.pack(side = 'top')
        content_textbox.pack(side=LEFT)
        content_textbox.config(yscrollcommand=scroll.set) # scrollbar
        scroll.pack(side=RIGHT)
        CFrame.pack()

        # Make GUI
        window.mainloop()