def corrupted_array_to_array(fileName):
    file = open(fileName, "r")
    content = file.read()
    file.close()
    content.split("\n")
    for row in content:
        row.split(",")
    return content