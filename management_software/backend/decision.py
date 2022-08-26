# def decision(decisionQueue):
#     result= 'Available'
#     if decisionQueue[0] == 'Free':
#         if decisionQueue[1] == 'No Cup':  
#             if decisionQueue[2] == 'No Bowl':
#                 if decisionQueue[3] == 'No Plate':
#                     result = 'Available'
#         elif decisionQueue[1] == 'Low' or decisionQueue[1] == 'Full':
#             if decisionQueue[2] == 'Dirty' or decisionQueue[2] == 'Food' or decisionQueue[2] == 'No Bowl':
#                 if decisionQueue[3] == 'Dirty' or decisionQueue[3] == 'Food' or decisionQueue[3] == 'No Plate':
#                     result = 'Need Cleaning'
#     elif decisionQueue[0] == 'Occupied':    
#         if decisionQueue[1] == 'Low':
#             if decisionQueue[2] == 'Dirty':
#                 if decisionQueue [3] == 'Dirty':
#                     result = 'Need refill and plate/bowl is empty'
#             else :
#                 result = 'Need refill'
#         elif decisionQueue[1] == 'Full' or decisionQueue[1] == 'No Cup':
#             if decisionQueue[2] == 'No Bowl' or decisionQueue[2] == 'Food': 
#                 if decisionQueue[3] == 'No Plate' or decisionQueue[2] == 'Food':
#                     result = 'Occupied'
#             elif decisionQueue[2] == 'Dirty':
#                 if decisionQueue[3] == 'Dirty':
#                     result = "Collect plate"
#     return result

def decision(decisionQueue):
    result= 'Available'
    if decisionQueue[0] == 'Free':
        if decisionQueue[2] == 'clean':  
          result = 'Available'
        elif decisionQueue[2] == 'dirty':
            result = 'Need Cleaning'
    elif decisionQueue[0] or decisionQueue[1] == 'Occupied':    
        result = "Occupied"
    # elif decisionQueue[0] or decision[2]== 'Occupied':    
    # result = "Occupied"
    return result