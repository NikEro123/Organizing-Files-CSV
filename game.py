import random
import copy

class Game:
    def __init__(self):
        self.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        for _ in range(2):
            self.add_random_tile()

    def display_grid(self):
        for row in self.grid:
            print(' '.join(str(num) for num in row))

    def add_random_tile(self):
        while True:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
            if self.grid[row][col] == 0:
                self.grid[row][col] = random.choice([2, 4])
                break

    def move_left(self):
        for i in range(4):
            self.grid[i] = [num for num in self.grid[i] if num != 0]

            j = 0
            while j < len(self.grid[i]) - 1:
                if self.grid[i][j] == self.grid[i][j + 1]:
                    self.grid[i][j] *= 2
                    self.grid[i][j + 1] = 0
                    j += 2
                else:
                    j += 1

            self.grid[i] = [num for num in self.grid[i] if num != 0]

            self.grid[i] += [0] * (4 - len(self.grid[i]))

    def move_right(self):
        for i in range(4):
            self.grid[i].reverse()

        self.move_left()

        for i in range(4):
            self.grid[i].reverse()

    def transpose(self):
        transposed = []

        for col in range(len(self.grid[0])):
            new_row = []
            for row in range(len(self.grid)):
                new_row.append(self.grid[row][col])
            transposed.append(new_row)

        self.grid = transposed

    def move_up(self):
        self.transpose()
        self.move_left()
        self.transpose()

    def move_down(self):
        self.transpose()
        self.move_right()
        self.transpose()

    def is_game_won(self):
        for row in self.grid:
            if 2048 in row:
                return True
        return False

    def is_game_over(self):
        for row in self.grid:
            if 0 in row:
                return False

        for i in range(4):
            for j in range(3):
                if self.grid[i][j] == self.grid[i][j + 1]:
                    return False

        for j in range(4):
            for i in range(3):
                if self.grid[i][j] == self.grid[i + 1][j]:
                    return False
        return True

    def run(self):
        while True:
            self.display_grid()

            move = input("Enter move (w/a/s/d) or q to quit: ").lower()

            if move == 'q':
                print("Thanks for playing!")
                break

            if move not in ['w', 'a', 's', 'd']:
                print("Invalid input!")
                continue

            print(f"You pressed: {move}")

            old_grid = copy.deepcopy(self.grid)

            if move == 'a':
                self.move_left()
            elif move == 'd':
                self.move_right()
            elif move == 'w':
                self.move_up()
            elif move == 's':
                self.move_down()

            if old_grid != self.grid:
                self.add_random_tile()

            if self.is_game_won():
                print("Congratulations! You've reached 2048")

            if self.is_game_over():
                print("Game over! No moves left")
                break
