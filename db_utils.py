# I imagine we will have a DB to store the individuals. In this file, we can store all relevant DB helper functions,
# e.g. - when researching an individual, we will want to confirm that they are not already in the DB, and if they are,
# we can defer to the already existing data, rather than performing a new search on that individual.
import csv


def get_output_results():
    # Read in the output.csv file
    names_dict = {}
    with open('output.csv', newline='') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            names_dict[row[1]] = row[5]

    return names_dict


def get_known_results():
    # Read in the known.csv file
    names_dict = {}
    with open('known_guest_data/test.csv', newline='') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            if (row[0] != '' and row[0] != 'NA'):
                names_dict[row[0]] = get_race_translation(row[1])

    return names_dict


def get_race_translation(race_abrv):
    if race_abrv == 'J' or race_abrv == 'J?':
        return 'Jewish'
    elif race_abrv == 'W' or race_abrv == 'W?':
        return 'White'
    elif race_abrv == 'B' or race_abrv == 'B?':
        return 'Black'
    elif race_abrv == 'A' or race_abrv == 'A?' or race_abrv == 'I' or race_abrv == 'I?':
        return 'Asian'
    elif race_abrv == 'H' or race_abrv == 'H?':
        return 'Hispanic'
    elif race_abrv == 'X' or race_abrv == 'X?' or race_abrv == 'M' or race_abrv == 'M?':
        return 'Other'

    return 'Unknown'

# Compare the two dictionaries and return a % accuracy score


def get_accuracy_score():
    total = 0
    correct = 0
    for key in known_res:
        if key in output_res:
            total += 1
            if known_res[key] == output_res[key]:
                correct += 1
            else:
                print('MISTAKE: ' + key + ' is ' +
                      known_res[key] + ' output: ' + output_res[key])

    return correct / total

# known_res = get_known_results()
# output_res = get_output_results()

# print('known_res has ' + str(len(known_res)) + ' entries')
# print('output_res has ' + str(len(output_res)) + ' entries')

# print(get_accuracy_score())


def get_dict_from_csv(csv_file):
    individuals_dict = {}
    # Read in the name, and individual object from the output.csv file
    with open(csv_file, newline='') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            # If row[0] contains a + character, multiple names, need to split
            if '+' in row[0]:
                # Split the names by the + character
                names = row[0].split(' + ')
                ethnicities = row[1].split(' ')
                # For each name, add it to the individuals_dict
                for name in names:
                    individuals_dict[name] = ethnicities.pop(0)
            elif row[0] != '' and row[0] != 'NA':
                individuals_dict[row[0]] = row[1]

    return individuals_dict


def append_dict_to_csv(existing_file_path, new):

    existing_dict = get_dict_from_csv(existing_file_path)

    values_to_append = {}
    for key in new:
        if key not in existing_dict:
            values_to_append[key] = new[key]

    with open(existing_file_path, 'a', newline='') as csvfile:
        datawriter = csv.writer(csvfile)
        for key in values_to_append:
            datawriter.writerow([key, new[key]])


append_dict_to_csv('manually_reviewed.csv', get_dict_from_csv('guest_temp.csv'))
