import re

# function to return a list from a file of comma delimited strings
def getListFromFile(filename):
    with open(filename, 'r') as filehandle:
        name_list = re.split(", |\n| \+ ", filehandle.read())
        name_list = [name for name in name_list if name != '']
        return name_list