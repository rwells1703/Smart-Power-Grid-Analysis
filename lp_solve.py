from matplotlib import pyplot as plt
import re
import subprocess

# Run each LP script and output the bytestring result
def run_script(script_path):
    command = ["lp_solve", script_path]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate()

    return stdout

# Trim and parse the LP script result
# Outputs a 2d list containing task names at each hour, and scheduled energy for that hour
def parse_task_schedule(stdout):
    decoded = stdout.decode("utf-8")
    removed_whitespace = re.sub("( )+", ",", decoded)
    split_on_newline = removed_whitespace.split("\r\n")
    trimmed_objective = split_on_newline[5:-1]
    split_on_comma = map(lambda s: s.split(","), trimmed_objective)

    return split_on_comma

# Get the scheduled energy for each hour, ingoring task names
def get_hour_values(task_schedule):
    hour_values = []

    for task in task_schedule:
        task_name = task[0]
        task_hour = task_name.split("_")[-1]
        hour_values.append([int(task_hour), int(task[1])])

    hour_values.sort(key=lambda x: x[0])
    return hour_values

# Combined multiple scheduled energy values for each hour to produce
# a single energy value per hour for the entire community
def aggregate_hour_values(hour_values):
    hour_totals = [0]*24
    for hv in hour_values:
        hour_totals[hv[0]] += hv[1]

    return hour_totals

# For each pricing curve specified, get its optimal scheduling
def get_curve_schedules(curve_indexes):
    all_hour_totals = []
    for i in curve_indexes:
        combined_hour_values = []
        for j in range(0,5):
            script_path = f"lp_scripts\\{i}\\user{j+1}.lp"
            stdout = run_script(script_path)
            task_schedule = parse_task_schedule(stdout)
            hour_values = get_hour_values(task_schedule)
            combined_hour_values += hour_values

        hour_totals = aggregate_hour_values(combined_hour_values)
        all_hour_totals.append(hour_totals)
    return all_hour_totals

# Display curve optimal schedulings as text
def display_curve_schedules(curve_indexes, all_hour_totals):
    i = 0
    while i < len(all_hour_totals):
        print(f"curve{curve_indexes[i]}:{all_hour_totals[i]}")
        i += 1

# Display curve optimal schedulings as bar graphs
def graph_curve_schedules(curve_indexes, all_hour_totals):
    i = 0
    while i < len(all_hour_totals):
        plt.title(f"Curve {curve_indexes[i]}")
        plt.bar(list(range(0,24)), all_hour_totals[i])
        plt.savefig(f"schedules\\curve{curve_indexes[i]}.jpg")
        plt.close()
        i += 1