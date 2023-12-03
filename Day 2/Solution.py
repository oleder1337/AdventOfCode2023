class Game:
    def __init__(self, amount_red=12, amount_green=13, amount_blue=14):
        self.amount_red = amount_red
        self.amount_green = amount_green
        self.amount_blue = amount_blue
        self.valid_game = True

    def draw_ball(self, color, amount: int):
        for i in range(0, amount - 1):
            # print(color)
            match color:
                case "blue":
                    self.amount_blue -= 1

                case "red":
                    self.amount_red -= 1

                case "green":
                    self.amount_green -= 1

                case _:
                    print("not a valid color")

        self.validate_game()

    def validate_game(self):
        if self.amount_blue > 0 and self.amount_green > 0 and self.amount_red > 0:
            # print(f"Amount red: {self.amount_red}")
            # print(f"Amount green: {self.amount_green}")
            # print(f"Amount blue: {self.amount_blue}")
            self.valid_game = True
        else:
            self.valid_game = False


def read_input():
    with open("input.txt", "r") as f:
        cont = f.read()
    return cont.split("\n")


def process_turn(turn):
    g = Game()
    draws = turn.split(",")
    for draw in draws:
        draw = draw[1 : len(draw)]
        draw = draw.split(" ")

        g.draw_ball(color=draw[1], amount=int(draw[0]))
    if g.valid_game:
        return True
    else:
        return False


def solve_question_1(inp=read_input()):
    solution = 0
    for entry in inp:
        game_number = entry.split(":")[0].split(" ")[1]
        entry = entry.split(":")[1]
        turns = entry.split(";")
        valid = True
        for turn in turns:
            if not process_turn(turn=turn):
                valid = False
                break
        if valid:
            solution += int(game_number)
    return solution


def solve_question_2(inp=read_input()):
    solution = 0
    for entry in inp:
        temp_s = {"red": 0, "green": 0, "blue": 0}
        entry = entry.split(":")[1]
        turns = entry.split(";")
        for turn in turns:
            turn = turn.split(",")
            for t in turn:
                t = t[1 : len(t)]
                color = t.split(" ")[1]
                draws = int(t.split(" ")[0])
                if temp_s[color] < draws:
                    temp_s[color] = draws

        solution += temp_s["red"] * temp_s["green"] * temp_s["blue"]

    return solution


def main():
    print(f"Solution to Q1: {solve_question_1()}")
    print(f"Solution to Q2: {solve_question_2()}")


if __name__ == "__main__":
    main()
