# needs further review
def assign_sites(units, allocations):
    
    # Returns two things dict of unit name -> list of site names
    # and list of sites that no unit could take

    room_left = {}
    assignments = {}
    for unit in units:
        if unit["active"]:
            room_left[unit["name"]] = unit["dose_capacity"]
            assignments[unit["name"]] = []

    unassigned = []

    for site in allocations:
        doses = allocations[site]

        # find the unit with the most room left
        best_unit = None
        for name in room_left:
            if best_unit is None:
                best_unit = name
            elif room_left[name] > room_left[best_unit]:
                best_unit = name

      if best_unit is None:
            unassigned.append(site)
        elif room_left[best_unit] < doses:
            unassigned.append(site)
        else:
            assignments[best_unit].append(site)
            room_left[best_unit] = room_left[best_unit] - doses

    return assignments, unassigned
