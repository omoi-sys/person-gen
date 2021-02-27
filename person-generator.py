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
input_argument = ""     # Name of input file passed, stays empty if none is
state_id = 0            # Position in list for state selected
address_list = []       # List of addresses that are generated
content_list = []

# Global list of state names in long form. This list have multiple
# uses including in the GUI list to choose from and in the non-GUI
# generation.
state_list = ['Alaska', 'Arizona', 'California', 'Colorado', 'Hawaii', 
            'Idaho', 'Montana', 'New Mexico', 'Nevada', 'Oregon', 'Utah', 
            'Washington', 'Wyoming']

# Global list of states in their abbreviated form is fow use in
# the non-GUI generation with comparison purposes.
states_short = ['ak', 'az', 'ca', 'co', 'hi', 'id', 'mt', 
                'nm', 'nv', 'or', 'ut', 'wa', 'wy']

# Dictionary of states with key as their long name and the abbreviated form
# as the value. Main use is in generate() function.
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

##############################################################################
# Function: generate()
# Purpose:  This function generates addresses by generating random numbers
#           in the range of 1 to the number of lines in a csv file minus 1.
#           Function then opens the csv file selected by the user that contains
#           address data from Kaggle's openaddresses files and saves the lines 
#           whose number matches the generated numbers. These addresses lines
#           are then saved in the global address_list variable list. Before
#           saving them, the list is emptied to make sure old addresses don't
#           take up space.
##############################################################################
def generate():
    global address_list # list of addresses to save the addresses to
    global content_list # list of content from the content generator
    line_nums = []      # line positions which will be used to select lines

    # reset list first after each call to generate()
    address_list = []

    # seed the random generator
    random.seed()

    count = 0 # count the number of lines that have been saved
    # run loop so long as the number of lines saved is less than
    # the one required
    while(count < num_to_generate):
        # generate random number in range 1 to length of [state].csv data_length file
        rand_num = random.randrange(1, data_lengths[state_filename_dict[state_list[state_id]]])
        # if the number generated is already in the list of generated numbers,
        # skip since we don't want duplicate addresses
        if rand_num in line_nums:
            continue
        # else save the number in the list and increase count
        else:
            line_nums.append(rand_num)
            count = count + 1

    # sort the generated numbers in ascening order
    line_nums.sort()

    # list of lines as they will be saved from the file
    address_lines = []

    # open the file
    file = open(state_filename_dict[state_list[state_id]] + '.csv')

    # read and save only the lines that match with the randomly
    # generated numbers in line_nums list. This should help with 
    # running time and memory usage as we won't be saving ALL the 
    # lines in memory using a list, but only the ones we need.
    # Method for enumerating lines adapted from: https://stackoverflow.com/questions/2081836/reading-specific-lines-only
    for i, line in enumerate(file):
        if i == line_nums[0]: # if the generated number matches the line number
            # save the line as is
            address_lines.append(line)
            # pop the front of the list, since we no longer need it; 
            # this will save us check time by not having to go through whole
            # number list with every line check
            line_nums.pop(0)
        # if the list of numbers is now empty, we are done and can exit
        # the loop without checking the rest of the file. This will
        # help with memory usage and running time. Especially with CA.
        if len(line_nums) == 0:
            break

    # close the file since we no longer need it
    file.close()

    # Save the addresses in the correct format without the LON, LAT,
    # DISTRICT, REGION, ID, HASH into the global address_list variable list
    for i in range(0, len(address_lines)):
        # current line split as a list
        current_addr = address_lines[i].split(',')
        if current_addr[4] == '': # If UNIT field is empty, don't added it
            # 2: NUMBER, 3: STREET, 5: CITY, 8: POSTCODE
            address_list.append(current_addr[2] + " " + current_addr[3] + " " + current_addr[5] + " " + current_addr[8])
        else:
            # 2: NUMBER, 3: STREET, 4: UNIT, 5: CITY, 8: POSTCODE
            address_list.append(current_addr[2] + " " + current_addr[3] + " " + current_addr[4] + " " + current_addr[5] + " " + current_addr[8])

    # create output.csv file and save addresses to it
    output = open('pg_output.csv', 'w')
    # Write the headers into the file first
    output.write('input_state, input_number_to_generate, output_content_type, output_content_value\n')
    # Write the data into output file
    for i in range(0, len(address_list)):
        output.write(state_list[state_id] + ',' + str(num_to_generate) + ',' + 'street address,' + address_list[i] + '\n')

    # make input file for Content Generator
    c_gen_file = open('cg_input.csv', 'w')
    c_gen_file.write('input_keywords\n')
    c_gen_file.write(state_list[state_id] + ';climate')
    c_gen_file.close()

    # Start the Content Generator
    os.system("python3 content-generator.py cg_input.csv")
    sleep(3) # wait a bit for the content generator to do its thing
    
    # read data that Content Generator created into a list
    cgen_output = open('output.csv', 'r')
    for line in cgen_output:
        content_list.append(line.split(';'))
    cgen_output.close()


##############################################################################
# Function: skip_GUI()
# Purpose:  This function is only called when the program is run with an input
#           file passed, such as 'python3 person-generator input.csv'. It will
#           skip creating a GUI and will simply read the input file and then
#           call generate() to get the addresses in output.csv.
##############################################################################
def skip_GUI():
    # Global variables that will be needed in generate()
    # and determined from input file.
    global num_to_generate
    global state_id

    # lines in the input file
    lines = []
    # open the input file
    input_file = open(input_argument, 'r')
    # save lines from input into lines list
    for i in input_file:
        lines.append(i)

    # Skip headers and get the values from the second line while splitting
    # the values based on commas
    vals = lines[1].split(',')

    # Save the number of addresses requested, which should be on second column
    num_to_generate = int(vals[1])
    # Go through the lists of states in full and short forms to compare first
    # column value, then save the where in the list it is in global state_id
    for i in range(0, 13):
        # if the value in lowercase matches the lowercased value in full
        # state name list OR the short form list, save that list position
        if state_list[i].lower() == vals[0].lower() \
        or states_short[i] == vals[0].lower():
            state_id = i

    # Call generate() function to get addresses and save them into output.csv
    generate()

##############################################################################
# Function: get_addr_list()
# Purpose:  Generate the list of addresses and save them into a global
#           variable display_list that will be pack()'d at the correct place 
#           outside the function. If pack() were called in the function, it
#           would create a new list underneath every time Generate is clicked.
##############################################################################
def get_addr_list():
    # Global variables that will be changed in the function
    global state_id
    global num_to_generate
    global display_list
    global content_info # Data that is displayed about the state climate
    global window

    # get the position of the state selected by user on GUI
    state_id = int(listbox.curselection()[0])
    # get the number of addresses the user wants to generate from GUI
    num_to_generate = int(user_num.get())

    # Delete the current list before generating a new one so the old
    # values don't remain.
    display_list.delete(0, 'end')

    # Call function that generates addresses. This function will also
    # save the addresses to output.csv file at the end.
    generate()

    # Insert addresses generated into global display_list to be used
    # by GUI to display to user.
    for i in range(0, num_to_generate):
        display_list.insert(i, address_list[i])

    # Take in data that was read from Content Generator
    temp_cont = ''
    for i in range(len(content_list[1][1])):
        if (i % 78 == 0):
            temp_cont += '\n'
        else:
            temp_cont += content_list[1][1][i]

    content_info.set('Climate in ' + content_list[1][0] + '\n' + temp_cont)


if __name__ == '__main__':
    # If a file was passed at the same time as the user started this program,
    # save the name of that input file and then call skip_GUI to just make
    # and save the addresses without displaying a GUI.
    if (len(sys.argv) > 1):
        input_argument = sys.argv[1]
        skip_GUI()

    # If no arguments are passed, then pop up a GUI from which a user can
    # manually request addresses.
    else:
        # Create the GUI window and greet user. I used the following tutorial
        # for learning how to make a GUI with Tkinter: https://coderslegacy.com/python/python-gui/python-tkinter-list-box/
        # and https://realpython.com/python-gui-tkinter/
        window = Tk()
        window.geometry("600x900")
        message = "Welcome to Person Generator\nPlease select which state you would like to generate addresses for.\n" + \
                "Please make sure the state is highlighted otherwise nothing will be generated.\n"
        greeting = Label(text=message)
        # Place this message at the top
        greeting.pack(side = 'top')

        # List of states
        listbox = Listbox(window, width='70', height='13')
        # List of addresses to be displayed
        display_list = Listbox(window, width='70', height='15')
        # Data from Content Generator
        content_info = StringVar()
        content_info.set('')
        content_data = Label(window, textvariable=content_info, width='70', height='15')

        # Insert states from state_list into the first listbox container
        for i in range(0, 13):
            listbox.insert(i, state_list[i])

        listbox.pack()  # Create list of states
        # Create entry area to enter the number of addresses to generate
        num_ask = Label(text='Number of addresses to generate (max 250)')
        num_ask.pack() 
        user_num = Entry(window, width = 20)
        user_num.insert(0, '') # Make sure entry area is empty
        user_num.pack(padx = 5, pady = 5)
        
        # Create area with list of addresses. This will be empty
        # before get_addr_list() is called by pressing Generate button
        display_list.pack()

        # Create button to press that calls get_addr_list() function
        bttn = Button(window, text = "Generate", command = get_addr_list)
        bttn.pack(side = 'bottom') # Display button at the bottom
        content_data.pack()

        # Make GUI
        window.mainloop()