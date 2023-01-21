# 8.2
import copy
import random


def spillerlist(antal):
    s_lst = []
    for i in range(antal):
        s_lst.append([f"Spiller {i+1}", 0])
    return s_lst


def runde(spillere):
    winner = ""
    high = 0
    high_lst = []
    s_lst = copy.deepcopy(spillere)
    for i in range(len(s_lst)):
        s_lst[i][1] = random.randint(1, 6)
        print(f"{s_lst[i][0]} slog {s_lst[i][1]}")
        if s_lst[i][1] >= high:
            if s_lst[i][1] == high:
                high_lst.append(s_lst[i])
            else:
                high = s_lst[i][1]
                high_lst.clear()
                high_lst.append(s_lst[i])
    if len(high_lst) > 1:
        winner = extra_runde(high_lst)
    else:
        winner = high_lst
    return winner


def extra_runde(high_lst):
    while True:
        print(
            f"---\nOmslag mellem flere spillere da de begge slog det samme højeste tal som var {high_lst[0][1]}\n---")
        new_high_lst = []
        high = 0
        for i in range(len(high_lst)):
            high_lst[i][1] = random.randint(1, 6)
            print(f"{high_lst[i][0]} slog {high_lst[i][1]}")
            if high_lst[i][1] >= high:
                if high_lst[i][1] == high:
                    new_high_lst.append(high_lst[i])
                else:
                    high = high_lst[i][1]
                    new_high_lst.clear()
                    new_high_lst.append(high_lst[i])
        if len(new_high_lst) == 1:
            return new_high_lst


def antal_runder(spillere, antal):
    point = {k[0]: 0 for k in spillere}
    penge = {k[0]: 100 for k in spillere}
    for i in range(antal):
        bet = copy.deepcopy(spillere)
        print("Hvor meget vil i satse? ")
        for j in range(len(spillere)):
            bet[j][1] = int(input(
                f"{spillere[j][0]} du har {penge[spillere[j][0]]},- hvor meget vil du satse? "))
        box(f"RUNDE {i+1}")
        winner = runde(spillere)
        print(
            f"---\nVinder af runden er {winner[0][0]} med et slag på {winner[0][1]}\n---")
        point[winner[0][0]] += 1
        for j in range(len(spillere)):
            if spillere[j][0] == winner[0][0]:
                penge[spillere[j][0]] += nested_sum(bet)
            else:
                penge[spillere[j][0]] -= bet[j][1]

        if i != antal-1:
            input("Tryk ENTER for at starte ny runde\n")
    point_fordeling(point)
    vinder(point)


def nested_sum(lst):
    sum = 0
    for i in range(len(lst)):
        sum += lst[i][1]
    return sum


def point_fordeling(point):
    for k, v in point.items():
        print(f"{k} vandt {v} runder")


def vinder(point):
    maxi = max(point, key=point.get)
    return box(f"Vinderen med flest point er: {maxi}")


def main():
    box("Velkommen Til Terningespillet")
    spillere = spillerlist(
        int(input("Hvor mange er i der ønsker at spille? ")))
    runder = int(input("Hvor mange runder ønsker i at spille? "))
    print("")
    print(
        f"Lad os komme i gange med at spille i er {len(spillere)} og i kommer til at spille {runder} runder!")
    antal_runder(spillere, runder)


def box(strings):
    line = "+"
    for _ in range(len(strings)+2):
        line += "-"
    line += "+"
    return print(f"{line}\n| {strings} |\n{line}")


if __name__ == "__main__":
    main()
