from decision import decision


def colours(decisionstatus, tableID):
    colour = 'white'
    if decisionstatus == 'Available':
        colour = 'green'
    elif decisionstatus == 'Need Cleaning':
        colour = 'yellow'
    elif decisionstatus == 'Occupied':
        colour = 'blue'
    return colour