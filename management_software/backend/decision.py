def decision(decisionQueue):
    result= 'Available'
    if decisionQueue[0] == 'Free':
        if decisionQueue[1] == 'No Cup':  
            if decisionQueue[2] == 'No Bowl':
                result = 'Available'
        elif decisionQueue[1] == 'Low' or decisionQueue[1] == 'Full':
            if decisionQueue[2] == 'Dirty' or decisionQueue[2] == 'Clean' or decisionQueue[2] == 'No Bowl':
                result = 'Need Cleaning'
    elif decisionQueue[0] == 'Occupied':    
        if decisionQueue[1] == 'Low':
            if decisionQueue[2] == 'Dirty':
                result = 'Need refill and plate is empty'
            else :
                result = 'Need refill'
        elif decisionQueue[1] == 'Full' or decisionQueue[1] == 'No Cup':
            if decisionQueue[2] == 'No Bowl' or decisionQueue[2] == 'Food': 
                result = 'Occupied'
            elif decisionQueue[2] == 'Dirty':
                result = "Collect plate"
    return result