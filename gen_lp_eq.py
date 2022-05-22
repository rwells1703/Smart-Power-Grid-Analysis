tasks = [
    (17, 19, 2, 3),
    (16, 20, 3, 9)
]

equations = []

for t in tasks:
    ready_time = t[0]
    deadline = t[1]
    max_hourly_energy = t[2]
    energy_demand = t[3]

    hours = range(0, 24+1)
    
    active_hours = range(ready_time, deadline+1)
    inactive_hours = list(filter(lambda h : h not in active_hours, hours))

    # Set the maximum hourly energy limits during hours when energy can be used
    for hour in active_hours:
        equations.append(f"0 <= x1_{hour} <= {max_hourly_energy};")

    # Ensure the total amount of energy provided to the task matches its demand
    active_equation = ""
    for i, hour in enumerate(active_hours):
        active_equation += f"x1_{hour}"
        if i != len(active_hours)-1:
            active_equation += "+"
    active_equation += f"={energy_demand};"
    equations.append(active_equation)

    # Ensure no energy is used outside of the range between ready_time and deadline
    inactive_equation = ""
    for i, hour in enumerate(inactive_hours):
        inactive_equation += f"x1_{hour}"
        if i != len(inactive_hours)-1:
            inactive_equation += ","
    inactive_equation += "=0;"
    equations.append(inactive_equation)

for e in equations:
    print(e)