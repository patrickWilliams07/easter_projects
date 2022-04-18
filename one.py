def check_person_array(array, person="Chuck"):
    if person in array:
        return array.index(person)
    return None
