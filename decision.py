def decision(decisionQueue):
    result= 'Available'
    if decisionQueue[0] == 'Free':
        if decisionQueue[1] == 'No Hands':  
            if decisionQueue[2] > 0.9: #Score > 0.9
                result = 'Available'
            elif decisionQueue[2] < 0.85: #Score < 0.85
                result = 'Dirty'
    else:    #elif decisionQueue[0] == 'Occupied':
        if decisionQueue[1] == 'Hands':
            result = 'Occupied'
    return result