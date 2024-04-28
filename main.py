# measure time spend on tasks
import os
from datetime import datetime, timedelta
import files_worker
import time
import time_control

# file names
data_tasks_time = "data_tasks_time.json"
json_data_list_file = "data.json"

# date time variables to use in code
time_kz = datetime.now()
time_now = time_kz.strftime("%m/%d/%Y")
date_time_now = time_kz.strftime("%m/%d/%Y, %H-%M-%S")

# create a essential json files for data base
files_worker.check_create_data_base()
files_worker.check_current_date(data_tasks_time)

# write start date time of work day. check if date already writen so if app would close
# not to write it again.
try:
    start_working_day = files_worker.read_json("work_start_time_stamp", json_data_list_file)
    if start_working_day.split(",")[0] != time_now:
        files_worker.update_task_json("work_start_time_stamp", date_time_now, json_data_list_file)
except IndexError:
    files_worker.update_task_json("work_start_time_stamp", date_time_now, json_data_list_file)

else:
    pass
print("Hello! Lets start new wonderful day at work")
print("Type -help or --h to know what you can do\n")


def main():

    # immediately after start before any task is started
    # the program begin to count idle time

    idle_start = datetime.now()
    idle_time_start = time.time()  # start idle time measure
    files_worker.update_task_json("idle_parameter", "idle", json_data_list_file)

    current_task = files_worker.read_json("current_task", json_data_list_file)
    print(f"Current task: {current_task}")

    user_input = input("What to do: ").capitalize()
    idle_time_stop = time.time()  # stop idle time measure
    idle_result = idle_time_stop - idle_time_start
    files_worker.update_task_json("idle_parameter", "work", json_data_list_file)
    time_spend = timedelta(seconds=idle_result)

    """
    Idle time write block
    """
    # current_task = read_json("current_task", json_data_list_file)
    task_index = files_worker.read_json_tasks_index(time_now, "Idle time", data_tasks_time)
    if task_index is not False:
        files_worker.append_json_tasks(time_now, task_index, "Idle time", idle_result, data_tasks_time)
        files_worker.update_task_json("idle_start_date_stamp", date_time_now, json_data_list_file)
    else:
        files_worker.append_json(time_now, {"Idle time": []}, data_tasks_time)
        files_worker.append_json_tasks(time_now, task_index, "Idle time", idle_result, data_tasks_time)
        files_worker.update_task_json("idle_start_date_stamp", date_time_now, json_data_list_file)

    """
    Idle time write block 
    """

    print("--------------------")
    print(f"Gone idle at {idle_start.strftime('%m/%d/%Y, %H-%M-%S')}")
    print(f"Time idling {time_spend}\n")

    # start new task
    if "begin" in user_input.lower():

        new_task = input("New task: ")
        if len(new_task) > 0:
            files_worker.update_task_json("current_task", new_task, json_data_list_file)
            files_worker.append_json(time_now, {new_task: []}, data_tasks_time)
            time_control.time_control(new_task)
        else:
            print("Enter valid string")

    # return to recently stopped task
    elif "current" in user_input.lower():

        current_task = files_worker.read_json("current_task", json_data_list_file)
        check_task_appearance = files_worker.read_json_tasks_index(time_now, current_task, data_tasks_time)
        if check_task_appearance is not False:
            time_control.time_control(current_task)
        else:
            print("Seems like this task is from yesterday but i will write it for you")
            files_worker.append_json(time_now, {current_task: []}, data_tasks_time)
            time_control.time_control(current_task)

    # return to a not current task but previously stopped at current day.
    elif "return" in user_input.lower():

        list_of_tasks = files_worker.read_json_tasks(data_tasks_time, time_now)
        if not list_of_tasks:
            print("There is no task today yet. Start at least one task to return list of tasks")
            main()
        try:
            back_to_task = int(input("Input task to return to: "))
            tasks = " ".join(list_of_tasks[back_to_task])
            files_worker.update_task_json("current_task", tasks, json_data_list_file)
            time_control.time_control(tasks)
        except ValueError:
            print("Input valid symbols")
            main()

    # read elapsed time on each task at any day or by any task.
    elif "read time" in user_input.lower():
        time_control.read_time(data_tasks_time, user_input.lower())

    # delete a task at current day
    elif "delete task" in user_input.lower():
        try:
            list_of_tasks = files_worker.read_json_tasks(data_tasks_time, time_now)
            if not list_of_tasks:
                print("There is no task today yet")
                main()
            input_task_num = int(input("Input task to delete: "))

            tasks = " ".join(list_of_tasks[input_task_num])
            files_worker.append_json(time_now, tasks, data_tasks_time, remove=True)
            print(f"Task \"{tasks}\" has been deleted")
            main()
        except ValueError:
            print("Input valid symbols")
            main()
        except IndexError:
            print("No task with such index")
            main()

    # manually add time to daily tasks
    elif "enter time" in user_input.lower():
        list_of_tasks = files_worker.read_json_tasks(data_tasks_time, time_now)
        if not list_of_tasks:
            print("There is no task today yet. Begin at least one task to manipulate the records")
            main()
        try:
            task_to_input = int(input("Input task to change time: "))

            task = " ".join(list_of_tasks[task_to_input])
            task_index = files_worker.read_json_tasks_index(time_now, task, data_tasks_time)
            if user_input.lower().split().count("-r") > 0:
                files_worker.append_json_tasks(time_now, task_index, task, 0, data_tasks_time, remove=True)
                print(f"Last time record from \"{task}\" has been removed")
                main()
            elif user_input.lower().split().count("-idle") > 0:
                files_worker.append_json_tasks(time_now, task_index, task, 0, data_tasks_time, remove=True)
            input_time = int(input("Input time in minutes: "))

            converted_min_to_sec = input_time * 60
            files_worker.append_json_tasks(time_now, task_index, task, converted_min_to_sec, data_tasks_time)

        except ValueError:
            print("Input valid symbols")
            main()

    # clear all data from data_tasks_time.json
    elif "erase" in user_input.lower():
        if user_input.lower().split().count("-one") > 0:
            print("logic triggered")
            input_date = input("Input date to delete (MM/DD/YYYY): ")
            date = input_date
            validating = input(f"This action erase all tasks at {date}, press Y to continue or press enter to cancel? ")
            if validating == "Y".lower():
                files_worker.erase_data(position=date, all_days=True)
                print(f"Tasks at {date} has been deleted")
            elif not validating.lower():
                print("Deletion has been canceled")
        else:
            validating = input("This action erase all tasks, press Y to continue or press enter to cancel? ")
            if validating == "Y".lower():
                files_worker.erase_data(all_days=True)
                print("All days has been deleted")
            elif not validating.lower():
                print("Deletion has been canceled")
        main()

    # rename chosen task in dict
    elif "rename" in user_input.lower():
        try:
            list_of_tasks = files_worker.read_json_tasks(data_tasks_time, time_now)
            task_to_rename = int(input("Chose task to rename: "))

            task = " ".join(list_of_tasks[task_to_rename])
            task_index = files_worker.read_json_tasks_index(time_now, task, data_tasks_time)
            input_new_name = input("Input new name: ")
            if input_new_name:
                files_worker.rename_task(time_now, task_index, task, data_tasks_time, input_new_name)
                main()
            else:
                print("Name should consist of at least one symbol")
        except ValueError:
            print("Enter valid symbols")
            main()

    # simply clear the console
    elif "cls" in user_input.lower():
        os.system("cls")
        main()

    # display help
    elif user_input == "-help" or user_input == "--h":
        print("Input \"Begin\" then create and start a new task\n"
              "Input \"Current\" and you will continue last active task\n"
              "Input \"Return\" will take you back to previous tasks\n"
              "Input \"Read time\" show how much time is spend on each task\n"
              "\tadd -n chose a task and return all time for one task\n"
              "\tadd -d chose a date and return all time for all tasks\n"
              "\tpress Enter and return time for current day"
              "Input \"Delete task\" and chose task to remove (in the current day by default)\n"
              "Input \"Erase\" and flush entire json DB\n"
              "\tadd -one and chose one date to flush\n"
              "Input \"Enter time\" and chose task to add time to\n" 
              "\tadd -r and remove last time record\n"
              "Input \"Rename\" chose the task to rename and enter new name"
              "Input \"cls\" to clean the console"
              )
        main()
    else:
        main()
    main()


main()
