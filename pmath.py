import copy


def isLineCollidesLine(x1, y1, x2, y2, x3, y3, x4, y4) -> bool:
    denominator: float = ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
    numerator1: float = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3))
    numerator2: float = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3))

    # Detect coincident lines (has a problem, read below)
    if (denominator == 0) :
        return False#numerator1 == 0 and numerator2 == 0

    r: float = numerator1 / denominator
    s: float = numerator2 / denominator

    return (0 <= r <= 1) and (0 <= s <= 1)

"""
line : [x1, y1, x2, y2]
rectangle [x1, y1, x2, y2]
"""
def rectangleCollidesLine(line: list, rectangle: list) -> bool:
    if isLineCollidesLine(line[0], line[1], line[2], line[3], 
                        rectangle[0], rectangle[1], rectangle[0], rectangle[3]):
        return True

    if isLineCollidesLine(line[0], line[1], line[2], line[3], 
                            rectangle[2], rectangle[1], rectangle[2], rectangle[3]):
        return True

    if isLineCollidesLine(line[0], line[1], line[2], line[3], 
                            rectangle[0], rectangle[1], rectangle[2], rectangle[1]):
        return True

    if isLineCollidesLine(line[0], line[1], line[2], line[3], 
                            rectangle[0], rectangle[3], rectangle[2], rectangle[3]):
        return True

    return  False

def computeRectangleCorner(obstacle: dict, chosenCorner: int):
    """result: list = copy.copy(obstacle["position"])

    if chosenCorner == 1 or chosenCorner == 2:
        result[0] += obstacle["size"][0]

    if chosenCorner >= 2:
        result[1] += obstacle["size"][1]

    return result"""

    if chosenCorner == 0:
        return [obstacle["position"][0] - 0.001, obstacle["position"][1] - 0.001]

    if chosenCorner == 1:
        return [obstacle["position"][0] + obstacle["size"][0] + 0.001, obstacle["position"][1] - 0.001]

    if chosenCorner == 2:
        return [obstacle["position"][0] + obstacle["size"][0] +  0.001, obstacle["position"][1] + obstacle["size"][1] +  0.001]

    if chosenCorner == 3:
        return [obstacle["position"][0] - 0.001, obstacle["position"][1] + obstacle["size"][1] + 0.001]

def getNumberVertex(map: dict):
    return len(map["wastes"]) + 1 + 4 * len(map["obstacles"])

def getPosition(map: dict, vertex: int) -> list:
    if vertex == 0:
        return map["robot"]["position"]

    vertex -= 1

    if vertex < len(map["wastes"]):
        return copy.copy(map["wastes"][vertex]["position"])
  
    start: int = vertex - len(map["wastes"])

    return computeRectangleCorner(map["obstacles"][start // 4], start % 4)

def path_to_graph(numberPoint, path):
    result: list = []
    for i in range(numberPoint):
        result.append([])

    for i in range(len(path) - 1):
        result[path[i]].append(path[i + 1])
        result[path[i + 1]].append(path[i])

    return result