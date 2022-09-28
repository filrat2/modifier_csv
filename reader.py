# -*- coding: utf-8 -*-

# import needed modules
import sys
import os
import csv


# define function to convert strings to list
def string_to_list(string):
    li = list(string.split(","))
    return li


# define function to convert lists to string
def list_to_string(li):
    string = ""
    for element in li:
        string += element + ','
    string = string[:-1]
    return string


# define function for export/save data to *.csv file
def write_csv(data, filepath):
    with open(filepath, 'w', newline='') as csv_file:
        write = csv.writer(csv_file)
        write.writerows(data)


# import data from *.csv file - filepath passed by user in argv[1]
source = sys.argv[1]

if os.path.exists(source) is False:
    print(f"Plik {source} nie istnieje.")
    sys.exit()
elif source[-4:] != ".csv":
    print(f"Podana ścieżka {source} nie jest plikiem formatu .csv.")
    sys.exit()

csv_file = csv.reader(open(source))
lines = list(csv_file)

# define other variables
dst = sys.argv[2]
changes = []
incorrect_changes = []

for change in sys.argv[3:]:
    change = string_to_list(change)
    if len(change) == 3:
        changes.append(change)


# checking locations passed by user
for change in changes:

    try:
        change[0] = int(change[0])
    except ValueError:
        print(f"Atrybut '{change[0]}' z ciągu znaków {change} podany "
              "jako wiersz do zmodyfikowania nie jest liczbą całkowitą "
              "dodatnią.")
        incorrect_changes.append(change)
        continue

    if change[0] > (len(lines) - 1):
        print(f"\nModyfikacja wartości '{change[2]}' z ciągu znaków {change} "
              f"niemożliwa.\nBrak wiersza nr {change[0]} w pliku '{source}', "
              "więc nie można dokonać modyfikacji wartości.\n")
        incorrect_changes.append(change)
        continue
    elif change[0] < 0:
        print(f"\nModyfikacja wartości '{change[2]}' z ciągu znaków {change} "
              f"niemożliwa.\nWskazany wiersz {change[0]} nie jest liczbą "
              "całkowitą dodatnią.\n")
        incorrect_changes.append(change)
        continue

    try:
        change[1] = int(change[1])
    except ValueError:
        print(f"Atrybut '{change[1]}' z ciągu znaków {change} podany "
              "jako kolumna do zmodyfikowania nie jest liczbą całkowitą.")
        incorrect_changes.append(change)
        continue

    if change[1] > (len(change) - 1):
        print(f"\nModyfikacja wartości '{change[2]}' z ciągu znaków {change} "
              f"niemożliwa.\nBrak wartości w wierszu {change[0]} w kolumnie "
              f"{change[1]} w pliku '{source}', więc nie można jej "
              "zastąpić.\n")
        incorrect_changes.append(change)
        continue
    elif change[1] < 0:
        print(f"\nModyfikacja wartości '{change[2]}' z ciągu znaków {change} "
              f"niemożliwa.\nWskazana kolumna {change[1]} nie jest liczbą "
              "całkowitą dodatnią.\n")
        incorrect_changes.append(change)
        continue

# remove changes with incorrect locations
for incorrect_change in incorrect_changes:
    changes.remove(incorrect_change)

# make changes
for change in changes:
    lines[int(change[0])][int(change[1])] = change[2]

# display modified *.csv file
for line in lines:
    line = list_to_string(line)
    print(line)

# save modified content to *.csv file - filepath passed by user in argv[2]
write_csv(lines, dst)
