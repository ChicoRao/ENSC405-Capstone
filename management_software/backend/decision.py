def decision(decisionQueue):
    result= 'Available'
    if decisionQueue[0] == 'Free':
        if decisionQueue[1] == 'No Cup':
            result = 'Available'
        elif decisionQueue[1] == 'Low' or decisionQueue[1] == 'Full':
            result = 'Need Cleaning'
    elif decisionQueue[0] == 'Occupied':    
        if decisionQueue[1] == 'Low':
            result = 'Need Attention'
        elif decisionQueue[1] == 'Full' or decisionQueue[1] == 'No Cup':
            result = 'Occupied'
    return result