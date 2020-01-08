import random

class RepairBot:
    def __init__(self, input):
        self.position = (0,0)
        self.board = {}
        self.board[self.position] = '.'
        self.move_direction = input

    def get_next_move(self, result):
        if result == 0: # wall
            self.board[self.position] = '#'
            directions = [1,2,3,4]
            print('move direction {}'.format(self.move_direction))
            directions.remove(self.move_direction)
            self.move_direction = random.sample(directions,1)[0]
            # Follow the wall
        elif result == 1: # moved successfully
            self.set_new_position()
            self.board[self.position] = '.'

            # keep going in this direction
        else: # result = 2
            self.board[self.position] = 'X'
    def set_new_position(self):
        if self.move_direction == 1:  # North
            self.position = (self.position[0],      self.position[1] + 1)
        elif self.move_direction == 2: # South
            self.position = (self.position[0],      self.position[1] - 1)
        elif self.move_direction == 3: # West
            self.position = (self.position[0] - 1,  self.position[1])
        else: # 4 East
            self.position = (self.position[0] + 1,  self.position[1])



r = RepairBot(1)
print(r.move_direction)
r.get_next_move(1)
r.get_next_move(1)
r.get_next_move(1)
r.get_next_move(0)

r.get_next_move(1)
r.get_next_move(1)
r.get_next_move(1)
r.get_next_move(0)
print(r.board)
