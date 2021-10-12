from random import randint
from fpstimer import FPSTimer
import sys, os

_GREEN = '\033[32;1m'
_RED = '\033[31;1m'
_WHITE = '\033[0m'

def clear():
    if os.name == 'nt':
        os.system('CLS')
    else:
        os.system('clear')

class Game:
    def __init__(self) -> None:
        self._end = False
        # Mapa del juego
        self._gameboard = []
        self._height = 25
        self._width = 100
        self.createGameboard()
        # Fruta
        self._fruity = 0
        self._fruitx = 0
        # Snake
        self._snake = []
        self._snakeDir = []
        self._snakeX = 0
        self._snakeY = 0
        self._snake_len = 4
        self._death = False
        # Score
        self._score = 0

    def startGame(self):
        '''Función que inicia el juego'''
        self.spawnSnake()
        # self.spawnFruit()

        self._fruitx = (self._width//2) + 1
        self._fruity = (self._height//2) + 8

        self.update()
        self.show()

    def createGameboard(self):
        '''Crea la cuadricula del juego'''
        # Crea la cuadricula
        for i in range(self._height):
            self._gameboard.append([])
            for j in range(self._width):
                self._gameboard[i].append(' ')

        # Bordes laterales
        for i in range(self._height):
            self._gameboard[i][0] = '|'
            self._gameboard[i][-1] = '|'
        # Borde superior
        for i in range(self._width):
            self._gameboard[0][i] = '='
            self._gameboard[-1][i] = '='

        # Titulo de arriba XD
        snake = '\U0001F40D'
        title = f' Python en Python xd '
        mid_title = self._width//2
        mid_text = len(title)//2
        for i in range(len(title)):
            self._gameboard[0][(mid_title+i)-mid_text] = title[i]

    def spawnFruit(self):
        '''Establece una posición a la fruta'''
        self._fruitx = randint(0, self._width-1)
        self._fruity = randint(0, self._height-1)

        # self._fruitx = self._width//2
        # self._fruity = self._height//2

        # self._gameboard[self._fruity][self._fruitx] = '@'

        while True:
            if self._gameboard[self._fruity][self._fruitx] != ' ':
                self._fruitx = randint(0, self._width-1)
                self._fruity = randint(0, self._height-1)
                continue
            break

    def spawnSnake(self):
        self._snakeX = self._width//2
        self._snakeY = self._height//2

        self._snakeDir.append([0, 1])
        self._snake.append([self._snakeY, self._snakeX])

        for i in range(self._snake_len-1):
            self._snakeDir.append(self._snakeDir[i-1])

        for i in range(self._snake_len-1):
            self._snake.append([self._snakeY, self._snakeX-i-1])

    # def updateSnake(self):


    def show(self):
        '''Muestra el juego'''
        for fila in self._gameboard:
            for columna in fila:
                sys.stdout.write(f'{columna}')
            sys.stdout.write('\n')
        # for fila in self._gameboard:
        #     sys.stdout.write(f'{str(fila)}\n')
        sys.stdout.write(f'Score: {self._score}\n')

    def update(self):
        '''Actualiza el juego'''
        # Coloca la fruta en el tablero
        self._gameboard[self._fruity][self._fruitx] = f'{_RED}@{_WHITE}'


        
        # Vacia los caracteres de la serpiente
        self._gameboard[self._snakeY][self._snakeX] = ' '
        for i in range(self._snake_len):
            self._gameboard[self._snake[i][0]][self._snake[i][1]] = ' '

        # Aumenta la direccion de la serpiente
        self._snakeX += self._snakeDir[0][1]
        self._snakeY += self._snakeDir[0][0]
        self._snake[0][0] = self._snakeY
        self._snake[0][1] = self._snakeX
        for i in range(self._snake_len-1):
            self._snake[i+1][0] += self._snakeDir[i+1][0]
            self._snake[i+1][1] += self._snakeDir[i+1][1]

        # Comprueba que no se salga del rango
        # Comprueba si se comio la fruta
        if self._snakeX == self._fruitx and self._snakeY == self._fruity:
            self._gameboard[self._snakeY][self._snakeX] = ' '
            self.eatFruit()
        elif self._gameboard[self._snakeY][self._snakeX] != ' ':
            self._death = True
            return

        # Establece la direccion
        for i in range(self._snake_len-1):
            if self._snakeDir[i+1] != self._snakeDir[i]:
               self._snakeDir[i+1] = self._snakeDir[i]
               break

        # Dibuja la serpiente
        for i in range(self._snake_len):
            self._gameboard[self._snake[i-1][0]][self._snake[i-1][1]] = f'{_GREEN}0{_WHITE}'
        self._gameboard[self._snakeY][self._snakeX] = f'{_GREEN}O{_WHITE}'


    def eatFruit(self):
        if self._snakeX == self._fruitx and self._snakeY == self._fruity:
            self._score += 100
            self._snake_len += 1

            tempDir = [self._snakeDir[-1][0], self._snakeDir[-1][1]]
            tempCoord = [self._snake[-1][0], self._snake[-1][1]]

            tempCoord[0] -= tempDir[0]
            tempCoord[1] -= tempDir[1]

            self._snakeDir.append(tempDir)
            self._snake.append(tempCoord)
            # self._snake[-1][-1] -= self._snakeDir[-1][-1]
            self.spawnFruit()


    def isDeath(self):
        if self._snakeX == 0 or self._snakeX == self._width-1:
            self._death = True
        if self._snakeY == 0 or self._snakeY == self._height-1:
            self._death == True
        
    def loop(self):
        timer = FPSTimer(10)
        # self._snakeDir[0] = [1,0]
        while(True):
            clear()
            self.update()

            self.isDeath()
            self.show()
            if self._death == True:
                print('Game Over')
                break
            timer.sleep()

def main():
    game = Game()
    game.startGame()
    game.loop()


if __name__ == '__main__':
    main()