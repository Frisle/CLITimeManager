import os
import json
from datetime import datetime, timedelta

time_kz = datetime.now()
time_now = time_kz.strftime("%m/%d/%Y")
date_time_now = time_kz.strftime("%m/%d/%Y, %H-%M-%S")

json_data_list_file = os.path.join(os.getcwd(), r"data.json")
data_tasks_time = os.path.join(os.getcwd(), r"data_tasks_time.json")


def erase_data(position=None, all_days=True):
    if all_days:
        clear_json(data_tasks_time)
        check_current_date(data_tasks_time)
    elif not all_days:
        clear_json(data_tasks_time, position)
        check_current_date(data_tasks_time, position)


def clear_json(file_name, position=None):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
    if position:
        file_data[position].clear()
    else:
        file_data.clear()

    with open(file_name, "w") as json_file:
        json.dump(file_data, json_file, ensure_ascii=False, indent=4)


def read_json_tasks(file_name, task_time):
    """
    Return task name with numeric order
    Used to give to the user interface to operate with tasks
    Such as: return to previous tasks or delete them
    :param file_name: file name of tasks json file
    :param task_time: desired task time (current time by default)
    :return:
    """
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        count = 0
        list_tasks = []
        for tasks in file_data[task_time][1:]:
            if tasks:
                count += 1
                list_tasks.append(list(tasks.keys()))
                print(f"{count-1} {list(tasks.keys())}")
            else:
                return []

        return list_tasks


def read_json(position, file_name):

    """
    Simple read and return function.
    Read one particular upper lever position
    :param position: key of the dict
    :param file_name: dict file name
    :return:
    """

    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        data_pull = file_data[position]
        return data_pull[0]


def read_json_tasks_time(file_name, position):
    with open(file_name, "r") as json_file:
        tasks_time = []
        tasks_name = []
        file_data = json.load(json_file)
        data_pull = file_data
        for items in data_pull[position]:
            for key in items:
                tasks_time.append(items.get(key))
                tasks_name.append(key)
        return tasks_time, tasks_name


def read_json_tasks_time_by_name(file_name, name):
    with open(file_name, "r") as json_file:
        tasks_time = []
        tasks_name = []
        time_float = 0
        file_data = json.load(json_file)
        data_pull = file_data
        for date in data_pull:
            for items in data_pull[date]:
                for key in items:
                    if key == name:
                        tasks_time.append(items.get(key))
                        tasks_name.append(key)

        for item in tasks_time:
            for seconds in item:

                time_float += seconds
        spend_time = timedelta(seconds=time_float)

        return tasks_time, tasks_name


def read_json_date(file_name):
    """
    Return list(0:4) of days at work in two formats
    With task count in each day
    """
    with open(file_name, "r") as json_file:

        file_data = json.load(json_file)
        count = 0
        for day in file_data:
            count += 1
            if count > 4:
                break
            if len(file_data[day]) > 0:
                full_day = datetime.strptime(day, "%m/%d/%Y")
                day_slash = full_day.strftime("%m/%d/%Y")
                day_name = full_day.strftime('%a %d')
                month_name = full_day.strftime('%b')
                year = full_day.strftime('\'%y')
                print(f"{day_name} {month_name} {year} {len(file_data[day])} tasks {day_slash}")


def append_json(position, data, file_name, remove=False):

    """
    Append a new artefact to the position key in data_list.json.
    Contain test option remove, for future use.
    :param position: first key in json file
    :param data: any data to insert
    :param file_name: corresponding filename
    :param remove: given the name of the task and the date remove the task from the list
    :return:
    """

    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
    if not remove:
        file_data[position].append(data)
    else:
        for task in file_data[position]:
            if task.get(data):
                index_to_delete = file_data[position].index(task)

                file_data[position].pop(index_to_delete)

    with open(file_name, "w") as json_file:
        json.dump(file_data, json_file, ensure_ascii=False, indent=4)


def append_json_tasks(position, index, task, time, file_name, remove=False):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)

    if remove:
        file_data[position][index][task].pop()
    else:
        file_data[position][index][task].append(time)

    with open(file_name, "w") as json_file:
        json.dump(file_data, json_file, ensure_ascii=False, indent=4)


def update_task_json(position, data, file_name):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)

    file_data[position].clear()
    file_data[position].append(data)

    with open(file_name, "w") as json_file:
        json.dump(file_data, json_file, ensure_ascii=False, indent=4)


def update_json_file(current_time, file_name):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)

    file_data.update({current_time: []})

    with open(file_name, "w") as json_file:
        json.dump(file_data, json_file, ensure_ascii=False, indent=4)


def check_create_data_base():
    try:
        file = open(data_tasks_time, "r")
        file.close()
    except FileNotFoundError:
        create_null_data_tasks_json()

    try:
        with open(json_data_list_file, "r") as file_list:
            file_list.readlines()
    except FileNotFoundError:
        create_null_list_json()


def create_null_data_tasks_json():
    with open(data_tasks_time, "w", encoding="utf-8") as json_file:
        data = {
            time_now: []
        }
        json_object = json.dumps(data, indent=4)
        json_file.write(json_object)


def create_null_list_json():
    with open(json_data_list_file, "w", encoding="utf-8") as json_file:
        data = {
            "idle_parameter": ["idle"],
            "current_task": ["Here your current tasks will appear"],
            "work_start_time_stamp": [],
            "idle_start_date_stamp": []
        }
        json_object = json.dumps(data, indent=4)
        json_file.write(json_object)


def check_current_date(file_name):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        data_stamps = []
        try:
            data_stamps.append(file_data[time_now])
        except KeyError:
            update_json_file(time_now, file_name)


def read_json_tasks_index(position, task, file_name):  # <'index'>
    """

    :param position: takes "time_now"
    :param task: takes “name” of the task as a string
    :param file_name: current file name of the json
    :return: “numeric index” of a task or False if not.
    """
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        tasks = []
        try:
            data_pull = file_data[position]
            for data in data_pull:
                tasks.append(list(data))
            return tasks.index([task])
        except ValueError:
            return False
