import copy


def isLineCollidesLine(x1, y1, x2, y2, z1, w1, z2, w2) -> bool:
    return False


"""
line : [x1, y1, x2, y2]
rectangle [x1, y1, width, height]
"""
def rectangleCollidesLine(line: list, rectangle: list) -> bool:
    if isLineCollidesLine(line[0], line[1], line[3], line[4], 
                        rectangle[0], rectangle[1], rectangle[0], rectangle[1] + rectangle[3]):
        return True

    elif isLineCollidesLine(line[0], line[1], line[3], line[4], 
                            rectangle[0] + rectangle[2], rectangle[1], rectangle[0] + rectangle[2], rectangle[1] + rectangle[3]):
        return True

    elif isLineCollidesLine(line[0], line[1], line[3], line[4], 
                            rectangle[0], rectangle[1], rectangle[0] + rectangle[2], rectangle[1]):
        return True

    elif isLineCollidesLine(line[0], line[1], line[3], line[4], 
                            rectangle[0], rectangle[1] + rectangle[3], rectangle[0] + rectangle[2], rectangle[1] + rectangle[3]):
        return True

    return  False

def computeRectangleCorner(obstacle: dict, chosenCorner: int):
    result: list = copy.copy(obstacle["position"][0])

    if chosenCorner == 1 or chosenCorner == 2:
        result[0] += obstacle["size"][0]

    if chosenCorner >= 2:
        result[1] += obstacle["size"][1]

    return result


def getPosition(map: dict, vertex: int) -> list:
  if vertex < len(map["wastes"]):
    return copy.copy(map["wastes"][vertex])
  
  start: int = vertex - len(map["wastes"])

  return computeRectangleCorner(map["obstacles"][start // 4], start % 4)