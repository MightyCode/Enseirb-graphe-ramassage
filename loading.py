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
        "worldSize" : [100, 100],
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
    size:str = data.split(";")[1].replace(" ", "").replace("(", "").replace(")", "").replace("\n", "")
  
    parts = positions.split(",")

    obstacle["position"] = [int(parts[0]), int(parts[1])]

    parts = size.split(",")

    obstacle["size"] = [int(parts[0]), int(parts[1])]

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
    

def load_map(path: str) -> dict:
    result: dict = return_template_map()

    file = open(path, 'r')
    lines: list = file.readlines()

    for line in lines:
        read_line(line, result)

    return result
