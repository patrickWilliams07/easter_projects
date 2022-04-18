def check_people_array(array, people=["Chuck", "Josh", "Bill", "Serge"]):
    indicies  = []
    for person in people:
        if person in array:
            indicies.append(array.index(person))
        else:
            indicies.append(None)
    return indicies
