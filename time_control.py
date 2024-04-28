import time
from datetime import datetime, timedelta
import files_worker
import json


data_tasks_time = "data_tasks_time.json"
json_data_list_file = "data.json"

time_kz = datetime.now()


def date_get():
    time_now = time_kz.strftime("%m/%d/%Y")
    return time_now


def get_time():
    return time_kz.strftime("%m/%d/%Y %H-%M-%S")


def get_time_read_input(input, parameter):
    if not input:
        input_task = date_get()
        data = files_worker.read_json_tasks_time(data_tasks_time, input_task)
        return data
    if parameter.split().count("-n"):
        data = files_worker.read_json_tasks_time_by_name(data_tasks_time, input)
        return data
    if parameter.split().count("-d"):
        data = files_worker.read_json_tasks_time(data_tasks_time, input)  # <class 'list'>
        return data


def time_control(new_task):
    print("--------------------")
    print(f"Working on \"{new_task}\" ")
    start_time = datetime.now()
    print(f"Started at {start_time.strftime('%m/%d/%Y %H-%M-%S')}")
    print("--------------------\n")
    start = time.time()

    print("Input any key to stop the timer")
    input("Input: ")
    stop_time = datetime.now()
    stop = time.time()
    elapsed_time = stop - start  # time in seconds

    task_index = files_worker.read_json_tasks_index(date_get(), new_task, data_tasks_time)
    files_worker.append_json_tasks(date_get(), task_index, new_task, elapsed_time, data_tasks_time)
    time_spend = timedelta(seconds=elapsed_time)
    print("\n--------------------")
    print(f"Work stopped at {stop_time.strftime('%m/%d/%Y %H-%M-%S')}. Get some rest or start another task")
    print(f"Time spend on task: \"{new_task}\" =  {time_spend}")
    print("--------------------\n")


# show available dates open data_tasks_time.json and read all keys with seconds.
def read_time(file_name, parameter):
    working_day_start = files_worker.read_json("work_start_time_stamp", json_data_list_file)
    files_worker.read_json_date(file_name)
    input_task = input("Input date or task: ")
    data = get_time_read_input(input_task, parameter)

    tasks_time = data[0]

    tasks_name = data[1]
    total_time_float = 0
    idle_time_float = 0
    for item in tasks_time[1:]:

        for seconds in item:
            total_time_float += seconds

    for idle_time in tasks_time[0:1]:
        for idle_seconds in idle_time:
            idle_time_float += idle_seconds

    total_idle_time = timedelta(seconds=idle_time_float)
    total_time_task = timedelta(seconds=total_time_float)

    total_time_seconds = idle_time_float + total_time_float
    total_time = timedelta(seconds=total_time_seconds)

    elapsed_time = []
    for t in tasks_time:
        elapsed_time.append(timedelta(seconds=sum(t)))

    for i in range(len(tasks_name)):
        tasks_names = tasks_name[i]
        elapsed_times = elapsed_time[i]
        print(f"Time spent on {tasks_names} is {elapsed_times}\n")
    print(f"Working day has started at {working_day_start}")
    print(f"Time total spent on tasks {total_time_task}")
    print(f"Time total spent idle {total_idle_time}")
    print(f"Time overall {total_time}")


