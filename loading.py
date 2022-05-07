import pmath

def return_template_robot() -> dict:
    return {
        "position" : [0, 0],
        "angle" : 0
    }


def return_template_waste() -> dict:
    return {
        "position" : [0, 0]
    }

def return_template_obstacle() -> dict:
    return  {
        "position" : [0, 0],
        "size" : [0, 0]
    }

def return_template_map() -> dict:
    return {
        "robot" : return_template_robot(),
        "size" : [0, 0],
        "wastes" : [],
        "obstacles": []
    }
   

def handle_robot(line: str, map: dict):
    data:str = line.split(":")[1].replace(" ", "").replace("(", "").replace(")", "").replace("\n", "")
    parts = data.split(",")
    map["robot"]["position"] = [int(parts[0]), int(parts[1])]

def handle_waste(line: str, map: dict):
    waste: dict = return_template_waste()

    data:str = line.split(":")[1].replace(" ", "").replace("(", "").replace(")", "").replace("\n", "")
    parts = data.split(",")

    waste["position"] = [int(parts[0]), int(parts[1])]
    map["wastes"].append(waste)


def handle_obstacle(line: str, map: dict):
    obstacle: dict = return_template_obstacle()

    data:str = line.split(":")[1]
    
    positions:str = data.split(";")[0].replace(" ", "").replace("(", "").replace(")", "").replace("\n", "")
    positions2:str = data.split(";")[1].replace(" ", "").replace("(", "").replace(")", "").replace("\n", "")
  
    parts = positions.split(",")

    obstacle["position"] = [int(parts[0]), int(parts[1])]

    parts = positions2.split(",")

    obstacle["size"] = [int(parts[0]) - obstacle["position"][0], int(parts[1]) - obstacle["position"][1]]

    map["obstacles"].append(obstacle)

def read_line(line: str, map: dict):
    if ":" not in line:
        return

    key: str = line.split(":")[0].replace(" ", "")

    if key == "R":
        handle_robot(line, map)
    elif key.isdigit():
        handle_waste(line, map)
    elif key == "X":
        handle_obstacle(line, map)
    

def load_map(path: str, map_size=None) -> dict:
    result: dict = return_template_map()

    file = open(path, 'r')
    lines: list = file.readlines()

    for line in lines:
        read_line(line, result)

    # Compute by hand map size
    if type(map_size) == list and len(map_size) == 2:
        result["size"] = map_size
    else:
        max = [0, 0]

        for waste in result["wastes"]:
            for i in range(2):
                if waste["position"][i] > max[i]:
                    max[i] = waste["position"][i]

        for i in range(2):
            if result["robot"]["position"][i] > max[i]:
                max[i] = result["robot"]["position"][i]

        result["size"] = [max[0] + 2, max[1] + 2]

    return result

def line_colline_obstacle(obstacles: list, line: list) -> bool:     
    for obstacle in obstacles:
        if pmath.rectangleCollidesLine(
                    line,
                    [obstacle["position"][0], obstacle["position"][1],
                    obstacle["position"][0] + obstacle["size"][0], obstacle["position"][1] + obstacle["size"][1]]):
            return True
    
    return False

def create_graph(map: dict) -> list:
    result: list = []

    for i in range(len(map["wastes"]) + len(map["obstacles"]) * 4):
        result.append([])

        position1 = pmath.getPosition(map, i)
        for j in range(len(map["wastes"]) + len(map["obstacles"]) * 4):
            if i == j:
                continue

            position2 = pmath.getPosition(map, j)
            
            if line_colline_obstacle(map["obstacles"], [position1[0], position1[1], position2[0], position2[1]]):
                continue

            result[i].append(j)

    return result