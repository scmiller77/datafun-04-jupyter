'''Project 3 - pull and manipulate data from web'''

import csv
import pathlib 
from pathlib import Path
import re
import random
import json


# External library imports (requires virtual environment)
import requests  
import pandas as pd

# Local module imports
#import yourname_attr      
from smiller_projsetup import create_folders_from_list
import mass_tort_analytics

#txt file section - fetch/write/process
def fetch_and_write_txt_data(folder_name, filename, url):
    response = requests.get(url)
    if response.status_code == 200:
        content = response.text
        cleaned_content = ''.join(char for char in content if char.isprintable() or char.isspace())
        write_txt_file(folder_name, filename, cleaned_content)
    else:
        print(f"Failed to fetch data: {response.status_code}")

def write_txt_file(folder_name, filename, data):
    file_path = Path(folder_name).joinpath(filename) # use pathlib to join paths
    with file_path.open('w') as file:
        file.write(data)
        print(f"Text data saved to {file_path}")

def process_txt_file(folder_name, filename, file_to):
    ''' Function to process txt document, focused on txt docs of books, giving us the total number of words, 
        number of unique words, the 9001st word, and the word that comes up the most.'''
    
    file_path = Path(folder_name).joinpath(filename)
    with file_path.open('r') as file:
        content = file.read()
        cleaned_content_1 = re.sub(r'<[^>]*>', '', content) #remove everything in angled brackets <>
        cleaned_content_2 = re.sub(r'{[^}]*}', '', cleaned_content_1) #remove everything in brackets {}
        cleaned_content_3 = re.sub(r'#\S+', '', cleaned_content_2) #remove terms that start with #
        cleaned_content_4 = re.sub(r'\b\w*\.(\w*\.)*\w*\b|\.\w+\b', '', \
                                   cleaned_content_3) #remove every word with a period in or before it
        words_list = cleaned_content_4.lower().split()
        words_set = set(words_list)
        
        word_counts = {} #now we make a word counter

        # Count occurrences of each word
        for word in words_list:
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1

        most_repeated_word = max(word_counts, key=word_counts.get) #This gives us the most repeated word

        custom_message = 'The number of words in this book is ' + str(len(words_list)) \
        + '.\n' + 'There are ' + str(len(words_set)) + ' unique words in this book. \n'\
        + 'The 9001st word is "' + words_list[9000] + '".\n' + 'The most repeated word'\
        ' in the book is "' + most_repeated_word + '". Go figure...'

    new_file_path = Path(folder_name).joinpath(file_to)
    with new_file_path.open('w') as file:
        file.write(custom_message)
        print(f"Text data saved to {new_file_path}")

#csv section - Fetch/write/process
        
def fetch_and_write_csv_data(folder_name, filename, url):
    response = requests.get(url)
    if response.status_code == 200:
        write_csv_file(folder_name, filename, response.text)
    else:
        print(f"Failed to fetch data: {response.status_code}")

def write_csv_file(folder_name, filename, data):
    file_path = Path(folder_name).joinpath(filename) # use pathlib to join paths
    with file_path.open('w') as file:
        file.write(data)
        print(f"Text data saved to {file_path}")

def process_csv_file(folder_name, filename, file_to):
    ''' Function to process csv file. It totals the salary of all employees, averages the value,
        and picks a random employee to win a lottery'''

    file_path = Path(folder_name).joinpath(filename)
    try:    #Implement Try/Except
        with file_path.open('r') as csvfile:
            csv_content = csv.reader(csvfile)
            employees = []
            for row in csv_content:
                employees.append(row)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    
    salary_column_index = 7

    # Extract salaries and calculate the sum
    salaries = [int(row[salary_column_index]) for row in employees[1:]]  # Skip the header row
    
    #employee lottery
    random_number = random.randint(1, 50)

    lotto_winner_first_name = employees[random_number][1] #pull winner's first name
    lotto_winner_last_name = employees[random_number][2]  #pull winner's last name

    #make custom message. Using an f string this time, to test that as well
    custom_message = f'''This csv file shows data for {len(salaries)} employees.
    \nThe employees are paid a total of ${sum(salaries)} each month, averaging to ${sum(salaries)/len(salaries)} per person.
    \n\nThe winner of the random lottery amongst the employees is {lotto_winner_first_name} {lotto_winner_last_name}!\
    \nVisit HR to collect your prize!
    '''

    new_file_path = Path(folder_name).joinpath(file_to)
    with new_file_path.open('w') as file:
        file.write(custom_message)
        print(f"Text data saved to {new_file_path}")

#Excel section - Fetch/Write/Process 
def fetch_and_write_excel_data(folder_name, filename, url):
    response = requests.get(url)
    if response.status_code == 200:
        write_excel_file(folder_name, filename, response)
    else:
        print(f"Failed to fetch Excel data: {response.status_code}")

def write_excel_file(folder_name, filename, data):
    file_path = Path(folder_name).joinpath(filename) # use pathlib to join paths
    with open(file_path, 'wb') as file:
        file.write(data.content)
        print(f"Excel data saved to {file_path}")

def process_excel_file(folder_name, filename, file_to):
    ''' Function to process an excel file. It provides the % of people who are married, 
        and the % of people who have purchased a bike. It also gives information about
        their ages.'''

    file_path = Path(folder_name).joinpath(filename)
    excel_data = pd.read_excel(file_path)
    excel_data_list = excel_data.values.tolist()

    entrees = [] #make a list for the data
    for row in excel_data_list:
        entrees.append(row)

    marriage_status_index = 1
    age_index = 11
    bike_purchase_index = 12

    marriage_status = [(row[marriage_status_index]) for row in entrees[:]]
    marriage_counter = 0
    for entry in marriage_status:
        if entry == "M":
            marriage_counter+=1
    
    ages = [int(row[age_index]) for row in entrees[:]]

    bike_purchased = [(row[bike_purchase_index]) for row in entrees[:]]
    
    bike_purchased_counter = 0
    for bike in bike_purchased:
        if bike == "Yes":
            bike_purchased_counter+=1

    custom_message = f'''This Excel file shows data for {len(marriage_status)} individuals.
\nTheir ages range from {min(ages)} to {max(ages)}, with an average age of {round(sum(ages)/len(ages))}.
\nOf these people, {round(marriage_counter/len(marriage_status) *100, 2)}% are married and \
{round(bike_purchased_counter/len(bike_purchased) *100, 2)}% have purchased a bike. 
\nFrom this data, it's more likely to find someone who is married than someone who has purchased a bike!
    '''

    new_file_path = Path(folder_name).joinpath(file_to)
    with new_file_path.open('w') as file:
        file.write(custom_message)
        print(f"Text data saved to {new_file_path}")

#Work with Json files - Fetch/Write/Process
def fetch_and_write_json_data(folder_name, filename, url):
    response = requests.get(url)
    if response.status_code == 200:
        write_json_file(folder_name, filename, response)
    else:
        print(f"Failed to fetch data: {response.status_code}")

def write_json_file(folder_name, filename, data):
    file_path = Path(folder_name).joinpath(filename) # use pathlib to join paths
    with file_path.open('wb') as file:
        file.write(data.content)
        print(f"Text data saved to {file_path}")

def process_json_file(folder_name, filename, file_to):
    ''' Function to process a json file. It tells you the likes and dislikes of pets'''
    file_path = Path(folder_name).joinpath(filename)
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    custom_message = "This json file tells us the following information:\n"

    for obj in data:
        name = obj['name']
        species = obj['species']
        likes = obj['foods']['likes']
        dislikes = obj['foods']['dislikes']

        # Print information for each pet
        info = (f"{name} is a {species} that likes {', '.join(likes)} and dislikes {', '.join(dislikes)}.\n")
        custom_message += info

    new_file_path = Path(folder_name).joinpath(file_to)
    with new_file_path.open('w') as file:
        file.write(custom_message)
        print(f"Text data saved to {new_file_path}")

    
def main():
    ''' Main function to demonstrate module capabilities. '''

    print(f"Byline: {mass_tort_analytics.byline}")

    txt_url = 'https://www.gutenberg.org/cache/epub/69087/pg69087-images.html'
    csv_url = 'https://gist.githubusercontent.com/kevin336/acbb2271e66c10a5b73aacf82ca82784/raw/e38afe62e088394d61ed30884dd50a6826eee0a8/employees.csv'
    excel_url = 'https://github.com/AlexTheAnalyst/Excel-Tutorial/raw/main/Excel%20Project%20Dataset.xlsx'
    json_url = 'https://raw.githubusercontent.com/LearnWebCode/json-example/master/animals-2.json'

    txt_folder_name = 'data-txt'
    csv_folder_name = 'data-csv'
    excel_folder_name = 'data-excel'
    json_folder_name = 'data-json'

    folders = [txt_folder_name, csv_folder_name, 
               excel_folder_name, json_folder_name]
    create_folders_from_list(folders, True, True)


    txt_filename = 'data.txt'
    csv_filename = 'data.csv'
    excel_filename = 'data.xls'
    jason_filename = 'data.json'


    fetch_and_write_txt_data(txt_folder_name, txt_filename, txt_url)
    fetch_and_write_csv_data(csv_folder_name, csv_filename, csv_url)
    fetch_and_write_excel_data(excel_folder_name, excel_filename, excel_url)
    fetch_and_write_json_data(json_folder_name, jason_filename, json_url)

    process_txt_file(txt_folder_name, 'data.txt', 'result_txt.txt')
    process_csv_file(csv_folder_name, 'data.csv', 'result_csv.txt')
    process_excel_file(excel_folder_name, 'data.xls', 'result_xls.txt')
    process_json_file(json_folder_name, 'data.json', 'results_json.txt')


if __name__ == "__main__":
    main()