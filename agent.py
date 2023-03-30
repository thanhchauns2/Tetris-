import random
import time
from nes_py.wrappers import JoypadSpace
import gym_tetris
from gym_tetris.actions import MOVEMENT

temp_board = [[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

temp_line = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
                 

class Agent:

    pieces = { # T, J, Z, O, S, L, I. Role : rotate to the right
        'I' : {
            'v' : [[0, 0, 1, 0],
                 [0, 0, 1, 0],
                 [0, 0, 1, 0],
                 [0, 0, 1, 0]],
            'h' : [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [1, 1, 1, 1],
                 [0, 0, 0, 0]],
        },
        'L' : {
            'r' : [[0, 1, 0, 0],
                 [0, 1, 0, 0],
                 [0, 1, 1, 0],
                 [0, 0, 0, 0]],
            'd' : [[0, 0, 0, 0],
                 [0, 1, 1, 1],
                 [0, 1, 0, 0],
                 [0, 0, 0, 0]],
            'l' : [[0, 0, 0, 0],
                 [0, 1, 1, 0],
                 [0, 0, 1, 0],
                 [0, 0, 1, 0]],
            'u' : [[0, 0, 0, 0],
                 [0, 0, 1, 0],
                 [1, 1, 1, 0],
                 [0, 0, 0, 0]],
        },
        'S' : {
            'h' : [[0, 0, 0, 0],
                 [0, 0, 1, 1],
                 [0, 1, 1, 0],
                 [0, 0, 0, 0]],
            'v' : [[0, 0, 0, 0],
                 [0, 1, 0, 0],
                 [0, 1, 1, 0],
                 [0, 0, 1, 0]],
        },
        'Z' : {
            'h' : [[0, 0, 0, 0],
                 [1, 1, 0, 0],
                 [0, 1, 1, 0],
                 [0, 0, 0, 0]],
            'v' : [[0, 0, 0, 0],
                 [0, 0, 1, 0],
                 [0, 1, 1, 0],
                 [0, 1, 0, 0]],
        },
        'O' : {
            0 : [[0, 0, 0, 0],
                 [0, 1, 1, 0],
                 [0, 1, 1, 0],
                 [0, 0, 0, 0]],
        },
        'J' : {
            'l' : [[0, 0, 1, 0],
                 [0, 0, 1, 0],
                 [0, 1, 1, 0],
                 [0, 0, 0, 0]],
            'u' : [[0, 0, 0, 0],
                 [0, 1, 0, 0],
                 [0, 1, 1, 1],
                 [0, 0, 0, 0]],
            'r' : [[0, 0, 0, 0],
                 [0, 1, 1, 0],
                 [0, 1, 0, 0],
                 [0, 1, 0, 0]],
            'd' : [[0, 0, 0, 0],
                 [1, 1, 1, 0],
                 [0, 0, 1, 0],
                 [0, 0, 0, 0]],
        },
        'T' : {
            'd' : [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 1, 1, 1],
                 [0, 0, 1, 0]],
            'l' : [[0, 0, 0, 0],
                 [0, 0, 1, 0],
                 [0, 1, 1, 0],
                 [0, 0, 1, 0]],
            'u' : [[0, 0, 0, 0],
                 [0, 0, 1, 0],
                 [0, 1, 1, 1],
                 [0, 0, 0, 0]],
            'r' : [[0, 0, 0, 0],
                 [0, 0, 1, 0],
                 [0, 0, 1, 1],
                 [0, 0, 1, 0]],
        }
    }

    board = []
    total_score = 0
    env, state, reward, done, info = None, None, None, None, None

    def __init__(self) -> None:
        self.board = temp_board
        self.env = gym_tetris.make('TetrisA-v0')
        self.env = JoypadSpace(self.env, MOVEMENT)

        self.state = self.env.reset()
        self.state, self.reward, self.done, self.info = self.env.step(0)
        self.env.render()
        x, y = 0, 0

        for i in range(5000):
            print(self.info)
            print(self.pieces['Z']['h'])
            self.calculate(self.info['current_piece'], 0, 0)
            self.env.render()

    def valid(self, piece_bounding, distance, x, y):
        for i in range(4):
            for j in range(4):
                if piece_bounding[i][j] + self.board[x][y + distance] > 1:
                    print(i, j, x, y, distance)
                    return False
        return True

    def go_down(self, piece : str, x, y):
        distance = 0
        piece_bounding = self.get_piece(piece)
        while self.valid(piece_bounding, distance, x, y):
            distance += 1
        
        distance -= 1
        if distance == -1:
            return -1e8
        else:
            return self.evaluate(piece_bounding, distance, x, y)
    
    def evaluate(piece_bounding, distance, x, y): # The algorithm
        return random.uniform(1, 10)

    def get_piece(self, code):
        print(code)
        if (code[0] == 'O'):
            return self.pieces['O'][0]
        else:
            return self.pieces[code[0]][code[1]]
        
    def calculate(self, piece, x, y):

        final_piece = piece
        delta_x = 0
        score = 0

        for delta in range(-5, 6):
            for p in self.pieces[piece[0]].keys():
                # print(self.go_down(piece[0] + p if p != 0 else piece[0], x + delta, y))
                if self.go_down(piece[0] + p if p != 0 else piece[0], x + delta, y) > score:
                    final_piece = p
                    delta_x = delta
        
        time.sleep(100000)

        while piece != final_piece:
            self.rotate()
            piece = self.info['current_piece']
        
        while delta_x < 0:
            self.go_right()
            x += 1
            delta_x -= 1
        
        while delta_x > 0:
            self.go_left()
            x -= 1
            delta_x += 1
        
        self.drop()
        self.update(piece, x, y)

    def go_right(self):
        self.state, self.reward, self.done, self.info = self.env.step(3)
        self.state, self.reward, self.done, self.info = self.env.step(0)
        self.env.render()

    def go_left(self):
        self.state, self.reward, self.done, self.info = self.env.step(6)
        self.state, self.reward, self.done, self.info = self.env.step(0)
        self.env.render()

    def drop(self):
        self.state, self.reward, self.done, self.info = self.env.step(9)
        self.state, self.reward, self.done, self.info = self.env.step(0)
        self.env.render()

    def rotate(self):
        self.state, self.reward, self.done, self.info = self.env.step(1)
        self.state, self.reward, self.done, self.info = self.env.step(0)
        self.env.render()
        
    def update(self, piece, x, y):
        distance = 0
        piece_bounding = self.get_piece(piece)
        while self.valid(piece_bounding, distance, x, y):
            distance += 1
        
        distance -= 1
        if distance == -1:
            self.game_over()
        else:
            for i in range(4):
                for j in range(4):
                    piece_bounding[i][j] += self.board[x][y + distance]
            
            for i in range(20):
                if sum(self.board[i] == 16):
                    self.total_score += self.score
                    board = temp_line + self.board[:i] + self.board[i + 1:]
    
    def game_over(self):
        pass
        # self.state = self.env.reset()
    

agent = Agent()

    