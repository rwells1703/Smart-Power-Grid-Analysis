def tasks_to_code(user, pricing):
    script = []

    all_hours = list(range(0, 24))

    # Overall list of active hours (for all tasks belonging to this user)
    all_tasks_active_hours = [[] for i in range(24)]

    # Add objective function to minimise
    script.append("min: c;")

    for task in user:
        # Retreive task information
        ready_time = task['info'][0]
        deadline = task['info'][1]
        max_hourly_energy = task['info'][2]
        energy_demand = task['info'][3]
        
        active_hours = list(range(ready_time, deadline+1))
        inactive_hours = list(filter(lambda h : h not in active_hours, all_hours))

        # Add the task name to the hour it can be done at
        for hour in active_hours:
            all_tasks_active_hours[hour].append(f"{task['name']}_{hour}")

        # Set the maximum hourly energy limits during hours when energy can be used
        for hour in active_hours:
            script.append(f"0<={task['name']}_{hour}<={max_hourly_energy};")

        # Ensure the total amount of energy provided to the task matches its demand
        active_equation = ""
        for i, hour in enumerate(active_hours):
            active_equation += f"{task['name']}_{hour}"

            if i != len(active_hours)-1:
                active_equation += "+"
        active_equation += f"={energy_demand};"
        script.append(active_equation)

        # Ensure no energy is used outside of the range between ready_time and deadline
        for hour in inactive_hours:
            script.append(f"{task['name']}_{hour}=0;")

    # Create the objective function by adding up predicted energy prices multplied by possible usage hours
    objective_function = "c="

    # Find out the final hour that can be occupied
    user_deadline = 0
    for hour in all_hours:
        if len(all_tasks_active_hours[hour]) > 0:
            user_deadline = hour

    # Create an objective function for the total cost (to be minimised)
    for hour in all_hours:
        for i, task_name in enumerate(all_tasks_active_hours[hour]):
            # Add the hour price as a multiplier
            objective_function += f"{pricing[hour]} {task_name}"

            # Append a plus, unless we are on the final term
            if hour != user_deadline or i != len(all_tasks_active_hours[hour])-1:
                objective_function += "+"
    objective_function += ";"
    script.append(objective_function)

    # The script is complete
    return script

# Print out LPSolve code to optimise each user's tasks
def print_all_scripts(scripts):
    for script in scripts:
        for statement in script:
            print(statement)
        print("\n")

def main():
    # Define pricing guideline
    pricing = [
        5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28
    ]

    # Define user tasks
    users = [
        [{"name": "x1", "info": (17, 19, 2, 3)},
        {"name": "x2", "info": (16, 20, 3, 9)}],
        [{"name": "x1", "info": (12, 18, 1, 4)},
        {"name": "x2", "info": (20, 23, 3, 6)}]
    ]

    scripts = []
    for user in users:
        scripts.append(tasks_to_code(user, pricing))

    print_all_scripts(scripts)

if __name__ == "__main__":
    main()