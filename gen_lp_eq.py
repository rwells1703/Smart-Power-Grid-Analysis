tasks = [
    (17, 19, 2, 3),
    (16, 20, 3, 9)
]

equations = []

for t in tasks:
    ready_time = t[0]
    deadline = t[1]
    max_energy = t[2]
    energy_demand = t[3]

    for hour in range(0, 24+1):
        if hour in range(ready_time, deadline+1):
            # Set the maximum energy limits during hours when energy can be used
            equations.append(f"0 <= x1_{hour} <= {max_energy};")
        else:
            # Otherwise ensure no energy is used between ready_time and deadline
            equations.append(f"x1_{hour} = 0;")

for e in equations:
    print(e)