from decision import decision


def colours(decisionstatus, tableID):
    colour = 'white'
    if decisionstatus == 'Available':
        colour = 'green'
    elif decisionstatus == 'Need Cleaning':
        colour = 'yellow'
    elif decisionstatus == 'Occupied':
        colour = 'blue'
    elif decisionstatus == 'Need refill and plate is empty':
        colour = 'red'
    elif decisionstatus == 'Need refill':
        colour = 'red'
    elif decisionstatus == 'Collect plate':
        colour = 'red'
    return {'ID': tableID, 'status': decisionstatus , 'colour':colour}