def randomCypher():
    "This function generates a cypher and randomize the elements inside it."
    import string, random
    elements = string.ascii_letters + string.digits + string.punctuation + "àèéìòù" + " "
    cypher = {elements[i]: None for i in range(len(elements))}

    already_sorted = []
    element_sorted = None

    for i in cypher.keys():
        while True:
            sort = random.randint(0, len(elements) -1)
            if sort in already_sorted:
                continue
            else:
                break

        already_sorted.append(sort)
        element_sorted = elements[sort]

        cypher[i] = element_sorted

    writeCypher(cypher)
    return cypher


def CaesarCypher():
    "This functions generate the Caesar Cypher with a random sequence, or if enabled by the user in the script, the original one."
    import string, random
    elements = string.ascii_letters + string.digits + string.punctuation + "àèéìòù" + " "
    cypher = {elements[i]: None for i in range(len(elements))}

    # sequence = 3 # use this for the original Caesar Cypher
    sequence = random.randint(0, len(cypher)) # use this for a random Caesar Cypher

    modulo = int(len(cypher))
    for i in cypher.keys():
        index = sequence % modulo
        cypher[i] = elements[index]
        sequence += 1

    writeCypher(cypher)
    return cypher
    
def writeCypher(cypher):
    "This function writes a cypher, from a one executed, into a text file."
    
    import json
    with open("cypher.txt","w") as file:
        json.dump(cypher, file)