import random
import loading

def generateWastes(map: dict, N: int) -> None:
    positions: list = []

    for x in range(map["size"][0]):
        for y in range(map["size"][1]):
            positions.append([x, y])

    print(map["size"])
    for i in range(N):
        index: int = random.randint(0, len(positions))

        waste = loading.return_template_waste()
        waste["position"] = positions[index]
    
        map["wastes"].append(waste) 

        del positions[index]



def createAndGenerateMap(size: list, N: int) -> dict:
    result: dict = loading.return_template_map()
    result["robot"]["position"] = [size[0] // 2, size[1] // 2]

    result["size"] = size

    generateWastes(result, N)

    return result