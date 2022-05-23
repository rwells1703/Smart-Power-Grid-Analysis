import data_load
import os

# Convert every task belonding to a user into a single set of linear equations to be solved
def tasks_to_code(user, pricing):
    script = []

    all_hours = list(range(0, 24))

    # Overall list of active hours (for all tasks belonging to this user)
    all_tasks_active_hours = [[] for i in range(24)]

    # Add objective function to minimise
    script.append("min: c;")

    for task in user:
        # Retreive task information
        ready_time = task['ready_time']
        deadline = task['deadline']
        max_hourly_energy = task['max_hourly_energy']
        energy_demand = task['energy_demand']
        
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

# Save LPSolve code to script files
def save_all_scripts(scripts, sub_folder):
    for i, script in enumerate(scripts):
        filepath = f"lp_scripts\\{sub_folder}\\user{i+1}.lp"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath,"w") as f:
            for statement in script:
                f.write(f"{statement}\n")

def schedule_real_tasks():
    # Define pricing guideline
    pricing_data = data_load.read_data("data\\TestingData.txt", "f*")
    for pricing_index, pricing in enumerate(pricing_data):
        # Define user tasks
        users = []
        users_data = data_load.read_data("data\\UserTaskData.csv", "siiii")

        previous_user_name = ""
        for current_user in users_data:
            task_name = current_user[0]
            ready_time = current_user[1]
            deadline = current_user[2]
            max_hourly_energy = current_user[3]
            energy_demand = current_user[4]

            current_user_name = task_name.split("_")[0]
            if current_user_name != previous_user_name:
                users.append([])
            previous_user_name = current_user_name

            users[-1].append({"name":task_name, "ready_time":ready_time, "deadline":deadline, "max_hourly_energy":max_hourly_energy, "energy_demand":energy_demand})

        scripts = []
        for user in users:
            scripts.append(tasks_to_code(user, pricing))

        save_all_scripts(scripts, pricing_index)

def main():
    schedule_real_tasks()

if __name__ == "__main__":
    main()