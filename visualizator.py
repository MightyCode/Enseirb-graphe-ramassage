import matplotlib.pyplot as plt

def display_map(map: dict) -> None:
    plt.xlim(0, map["size"][0])
    plt.ylim(0, map["size"][1])

    ax = plt.subplot()

    i: int = 1
    for waste in map["wastes"]:
        plt.plot(waste["position"][0], waste["position"][1], marker="o", markersize=3, markeredgecolor="black", markerfacecolor="green")
        ax.annotate(str(i), (waste["position"][0], waste["position"][1]))

        i += 1

    
    plt.plot(map["robot"]["position"][0], map["robot"]["position"][1], marker="o", markersize=5, markeredgecolor="black", markerfacecolor="red")

    plt.grid()
    plt.show()