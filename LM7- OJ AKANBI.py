import os

'''
Name: OJ AKANBI
Course: IST 140
Assignment:LM7 CODING Assignment
'''
student_roster = {}
students_absent = []
students_present = []

total_students_absent = 0
total_students_present = 0
total_students_in_roster = 0
total_number_of_students = 0

student_attendance_unknown = []

counter = 0

# setting the variable for the files that are getting inputted
hold_roster_file_name = "/Users/ojakanbi/Desktop/IST140_Class_Roster.txt"
hold_students_present_file_name = "/Users/ojakanbi/Desktop/meeting_saved_chat.txt"
(os.path.isfile(hold_students_present_file_name))  # finds if the file is on the desktop

# Building the path to the specific files
full_file_path_roster = hold_roster_file_name
full_file_path_students_present = hold_students_present_file_name


# opens a file for reading and writing, placing the pointer at the beginning of the file

def add_to_roster(name, email):
    global counter
    counter += 1

    student_roster["Student" + str(counter)] = {"Name": name.capitalize(), "Email": email}


def import_student_roster():  # opens a file for reading and writing, placing the pointer at the beginning of the file
    global counter
    global total_number_of_students

    with open(full_file_path_roster, "r+") as tmp_roster:
        # for line in tmp_roster:
        # print(line, end='')
        tmp_roster_file = tmp_roster.readlines()

        for student in tmp_roster_file:
            tmp_validate = student.find("|")

            if tmp_validate == -1:
                pass
            split_name = student.split("|")
            student_name = (split_name[0].strip().lower())
            student_email = (split_name[1].strip().lower())
            add_to_roster(student_name, student_email)
            total_number_of_students += 1

            # print(student_name, student_email)


def check_attendance():
    for keys, values in student_roster.items():
        for key, value in values.items():
            if key == "Name":
                print(f"Is {value} present or absent")
                user_attendance = input(f"Select P for present and A for absent: ")
                user_attendance = user_attendance.upper()
                if user_attendance == 'P':
                    students_present.append(value)
                elif user_attendance == 'A':
                    students_absent.append(value)
    if len(students_absent) > 0:
        print("\tABSENT")
        for name in students_absent:
            print(f"{name}")
    if len(students_present) > 0:
        print("\tPRESENT")
        for name in students_present:
            print(f"{name}")


def display_roster():
    for keys, items in student_roster.items():  # external dictionary
        print(keys, "|", end=" ")
        for key, value in items.items():  # internal dict that has name and email as key
            if key == 'Name':
                print(value, "|", end="")

            if key == 'Email':
                print(f" {value}")


def drop_student(student, roster):
    try:
        del roster[student]
    except KeyError:
        print("There is no student to drop")


def import_present_students():
    # load up the students tht are present
    global total_students_present

    with open(full_file_path_students_present, 'r+') as path_students:  # open the file with cureent student oresent
        present_students = path_students.readlines()

        for students in present_students:
            validate_record = students.find("From")

            if validate_record == -1:
                pass
            else:  # splits out the information that you do not want from the file txt
                split_student = students.split("From")
                student = (split_student[1]).strip().lower()
                tmp_display_name = student.split(":")
                display_name = tmp_display_name[0]
                display_name = display_name.strip().lower()

                duplicate_check = students_present.count(
                    display_name)  # gets rid of duplicate name incase someone adds in their name multiple times

                if duplicate_check > 0:
                    pass
                else:
                    students_present.append(display_name)
                    total_students_present += 1


def find_absent_students():
    # loop through the student roster.. check the dict against the students
    # in the present list
    global total_students_absent

    print(students_present)

    for student, details in student_roster.items():

        tmp_student_name = ""
        tmp_student_email = ""

        for key, value in details.items():
            # first check to see if the  name in the roster is in the student_present list

            if key == "Name":
                tmp_student_name = value
                if str(value).lower() in students_present:
                    break  # This means that the student is present in the dict. now break out of the loop


            # if it is not, check to see if the email is in the list
            elif key == "Email":
                tmp_student_email = value
                if str(value).lower() in students_present:
                    break
                else:  # if it isn't, then we assume that the student is absent
                    students_absent.append("Name: " + tmp_student_name + " | " + "Email: " + tmp_student_email)
                    total_students_absent += 1


def bulk_update_roster():
    # reset the counter and also the student roster
    global counter
    global total_students_in_roster

    counter = 0
    student_roster.clear()

    for student in students_present:
        split_student_roster = student.split("|")
        roster_student_name = split_student_roster[0].strip().lower()
        roster_student_email = split_student_roster[1].strip().lower()

        add_to_roster(roster_student_name, roster_student_email)

        total_students_in_roster += 1


def display_count_metrics_validation():
    calculated_absent = total_number_of_students - total_students_present
    total_calculated_students = total_students_present + total_students_absent
    total_students_present_marked_absent = total_students_absent - calculated_absent

    print("\nCount Validation - Only" + str(calculated_absent) + " students should be marked absent!")
    print()
    print("\t * Total Students Present & Marked absent: " + str(total_students_present_marked_absent) + " *")
    print()
    print("\t Total Students Present: " + str(total_students_present))
    print("\t Total Students Absent: " + str(total_students_absent))
    print()
    print("\t Total verified students in course: " + str(total_number_of_students))
    print("\t Calculated students in course (Absent + Present): " + str(total_calculated_students))


def bulk_attendance_load():
    # call the function to update the roster dictionary from our file input read
    bulk_update_roster()

    import_student_roster()

    # pull the present students in and load up the list
    import_present_students()

    # print out the roster
    print("Roster: ")
    display_roster()

    # find and print the absent students
    find_absent_students()
    print("\n Students Absent: " + str(total_students_absent))

    for students in students_absent:
        print("\t" + students)

    # print the present students
    print("\n Students present: " + str(total_students_present))

    for students in students_present:
        print("\t" + students)

    # calculated metrics and display
    display_count_metrics_validation()


def print_menu():  # function to print out my menu options
    menu_option = ['Modify/Add', 'Attendance', 'Drop', 'Display', 'Bulk Attendance', 'Exit']
    print("\nMain Menu:")
    for count, word in enumerate(menu_option, start=1):
        print(f"\t{count} {word}")
    print('')


# for some reason the path for the folder on my desktop wasn't finding the folder


print("Welcome, this is your software to modify your scouts.")

print_menu()  # call menu function to user
try:
    user_menu = int(input("Please enter a menu option number: "))  # ask user for menu choice
    if user_menu < 1:
        raise Exception("You inputted a number that is not in the menu")

except ValueError:
    print("You have to enter an integer")

else:
    while user_menu != 6:  # while the user do not exit
        if user_menu == 1:
            scout_name = input("Enter Student name: ")  # variable for student name
            scout_email = input("Enter Student email: ")  # variable for student email
            add_to_roster(scout_name, scout_email)

        elif user_menu == 2:  # if user wants to check attendance
            check_attendance()

        elif user_menu == 3:  # this drop scouts from the roster
            display_roster()
            drop_student_number = (input("Enter Student number to drop (EX:'1'): "))
            student_drop = "Student" + drop_student_number
            drop_student(student_drop, student_roster)
        elif user_menu == 4:
            display_roster()

        elif user_menu == 5:
            bulk_attendance_load()
        print_menu()
        try:
            user_menu = int(input("Please Enter a menu number or '6' to exit: "))
        except ValueError as ve:
            print(f"{ve} \nYou have to input an integer")
        else:
            pass
