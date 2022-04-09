def decision(decisionQueue):
    result= 'Available'
    if decisionQueue[0] == 'Free':
        if decisionQueue[1] == 'No Cup':  
            if decisionQueue[2] == 'No Bowl':
                result = 'Available'
        elif decisionQueue[1] == 'Low' or decisionQueue[1] == 'Full':
            if decisionQueue[2] == 'Dirty' or 'Clean':
                result = 'Need Cleaning'
    elif decisionQueue[0] == 'Occupied':    
        if decisionQueue[1] == 'Low':
            result = 'Water is low'
            if decisionQueue[2] == 'Clean':
                result = 'Water is low and plate is empty'
        elif decisionQueue[2] == 'Clean':
            result = 'plate is empty'
        elif decisionQueue[1] == 'Full' or decisionQueue[1] == 'No Cup':
            if decisionQueue[2] == 'No Bowl' or 'Clean' or 'Dirty':
                result = 'Occupied'
    return result