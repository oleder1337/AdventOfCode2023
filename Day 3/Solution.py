from typing import List


def read_input():
    with open("input.txt", "r") as f:
        return f.read().split("\n")


def create_engine(input):
    parts = []
    part_numbers = []
    for index_y, line in enumerate(input):
        num_flag = False
        num_threshold = ""
        num_coordinates = []
        for index_x, character in enumerate(line):
            try:
                character = int(character)

                if num_flag == False:
                    num_flag = True
                num_threshold += str(character)
                num_coordinates.append((index_y, index_x))

            except ValueError:
                if num_flag:
                    part_numbers.append(
                        Part_Number(
                            number=int(num_threshold), coordinates=num_coordinates
                        )
                    )
                    num_flag = False
                    num_threshold = ""
                    num_coordinates = []
            if num_flag and index_x == len(line) - 1 and len(num_threshold) > 0:
                part_numbers.append(
                    Part_Number(number=int(num_threshold), coordinates=num_coordinates)
                )

                continue

            if not num_flag and character != ".":
                if character == "*":
                    parts.append(Gear(part=character, coordinate=(index_y, index_x)))
                else:
                    parts.append(Part(part=character, coordinate=(index_y, index_x)))

    return parts, part_numbers


def check_for_adjacent(coordinate_a: tuple, coordinate_b: tuple):
    if (
        (
            abs(coordinate_a[0] - coordinate_b[0]) == 1
            and abs(coordinate_a[1] - coordinate_b[1]) == 1
        )
        or (
            abs(coordinate_a[0] - coordinate_b[0]) == 0
            and abs(coordinate_a[1] - coordinate_b[1]) == 1
        )
        or (
            abs(coordinate_a[1] - coordinate_b[1]) == 0
            and abs(coordinate_a[0] - coordinate_b[0]) == 1
        )
    ):
        return True
    else:
        return False


class Part_Number:
    def __init__(self, number, coordinates):
        self.number = number
        self.coordinates = coordinates
        self.adjacent = False

    def set_adjacent(self):
        self.adjacent = True


class Part:
    def __init__(self, part, coordinate):
        self.part_number = []
        self.part = part
        self.coordinate = coordinate

    def add_part_number(self, part_number: Part_Number):
        self.part_number.append(part_number)


class Gear(Part):
    def __init__(self, part, coordinate):
        super().__init__(part, coordinate)
        self.verified = False
        self.part_no_threshold = 0
        self.gear_ratio = 1

    def add_part_number(self, part_number):
        self.part_no_threshold += 1
        self.gear_ratio *= part_number
        if self.part_no_threshold == 2:
            self.verified = True
        if self.part_no_threshold > 2:
            self.verified = False

    def __repr__(self):
        return "Gear"


class Engine:
    def __init__(self, inp=read_input()):
        self.parts, self.part_numbers = create_engine(input=inp)
        self.gears = [x for x in self.parts if repr(x) == "Gear"]
        self.map_part_numbers()

    def map_part_numbers(self):
        part_coordinates = [x.coordinate for x in self.parts]
        for number in self.part_numbers:
            if number.adjacent:
                continue

            else:
                found = False
                for coordinate in number.coordinates:
                    for part_coordinate in part_coordinates:
                        if check_for_adjacent(
                            coordinate_a=coordinate, coordinate_b=part_coordinate
                        ):
                            number.set_adjacent()
                            found = True
                            break
                    if found:
                        break

    def map_gears(self):
        for gear in self.gears:
            for part_number in self.part_numbers:
                found = False
                for coordinate in part_number.coordinates:
                    if check_for_adjacent(
                        coordinate_a=gear.coordinate, coordinate_b=coordinate
                    ):
                        gear.add_part_number(part_number.number)
                        found = True
                        break


def solve_question_1(e: Engine):
    solution = sum([x.number for x in e.part_numbers if x.adjacent == True])

    print(f"Solution to Question 1: {solution}")


def solve_question_2(e: Engine):
    e.map_gears()
    solution = sum([x.gear_ratio for x in e.gears if x.verified == True])
    print(f"Solution to Question 2: {solution}")


def main():
    e = Engine()
    solve_question_1(e=e)
    solve_question_2(e=e)


if __name__ == "__main__":
    main()
