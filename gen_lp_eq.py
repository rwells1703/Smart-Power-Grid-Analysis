from re import L


pricing = [
    5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28
]

users = [
    {"name": "u1", "tasks": [{"name": "t1", "info": (17, 19, 2, 3)},
                             {"name": "t2", "info": (16, 20, 3, 9)}]},
    {"name": "u2", "tasks": [{"name": "t1", "info": (12, 18, 1, 4)},
                             {"name": "t2", "info": (20, 23, 3, 6)}]}
]

equations = []

for u in users:
    all_hours = list(range(0, 24))

    user_active_hours = [[] for i in range(24)]
    user_equation = []

    # Add objective function to minimise
    user_equation.append("min: c;")

    for t in u["tasks"]:
        ready_time = t["info"][0]
        deadline = t["info"][1]
        max_hourly_energy = t["info"][2]
        energy_demand = t["info"][3]
        
        active_hours = list(range(ready_time, deadline+1))
        inactive_hours = list(filter(lambda h : h not in active_hours, all_hours))

        # Add the task name to the hour it can be done at
        for hour in active_hours:
            user_active_hours[hour].append(f"{u['name']}_{t['name']}_{hour}")

        # Set the maximum hourly energy limits during hours when energy can be used
        for hour in active_hours:
            user_equation.append(f"0 <= {u['name']}_{t['name']}_{hour} <= {max_hourly_energy};")

        # Ensure the total amount of energy provided to the task matches its demand
        active_equation = ""
        for i, hour in enumerate(active_hours):
            active_equation += f"{u['name']}_{t['name']}_{hour}"

            if i != len(active_hours)-1:
                active_equation += "+"
        active_equation += f"={energy_demand};"
        user_equation.append(active_equation)

        # Ensure no energy is used outside of the range between ready_time and deadline
        inactive_equation = ""
        for i, hour in enumerate(inactive_hours):
            inactive_equation += f"{u['name']}_{t['name']}_{hour}"

            if i != len(inactive_hours)-1:
                inactive_equation += ","
        inactive_equation += "=0;"
        user_equation.append(inactive_equation)

    # Create the objective function by adding up predicted energy prices multplied by possible usage hours
    objective_function = "c="

    # Find out the final hour that can be occupied
    user_deadline = 0

    for hour in all_hours:
        for tasks in user_active_hours[hour]:
            if len(tasks) > 0:
                user_deadline = hour

    for hour in all_hours:
        for i, task in enumerate(user_active_hours[hour]):
            # Add the hour price as a multiplier
            objective_function += f"{pricing[hour]} {u['name']}_{t['name']}_{hour}"

            # Append a plus, unless we are on the final term
            if hour != user_deadline or i != len(user_active_hours[hour])-1:
                objective_function += "+"
    objective_function += ";"

    user_equation.append(objective_function)

    equations.append(user_equation)

for ue in equations:
    for e in ue:
        print(e)
    print("\n")