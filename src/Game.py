from random import randint
from fpstimer import FPSTimer
from time import sleep
import sys
import os
import msvcrt

_CLEAR = 'cls' if os.name == 'nt' else 'clear'
_GREEN = '\033[32;1m'
_RED = '\033[31;1m'
_WHITE = '\033[0m'
_BLOCK = '\U00002588'

debug = False
if '-dbg' in sys.argv:
    debug = True
    _TOTAL_HEIGHT = 15
else:
    _TOTAL_HEIGHT = 2

# Comprueba que este en src
if os.getcwd()[-3:] != 'src':
    os.chdir('src')

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
        self._fruitCount = 0

    def startGame(self):
        '''Función que inicia el juego'''
        self.spawnSnake()
        self.spawnFruit()

        self.update()
        self.show()

        self.loop()

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

        while True:
            if self._gameboard[self._fruity][self._fruitx] != ' ':
                self._fruitx = randint(0, self._width-1)
                self._fruity = randint(0, self._height-1)
                continue
            break

    def spawnSnake(self):
        '''Coloca la serpiente en el mapa al iniciar el juego'''
        self._snakeX = self._width//2
        self._snakeY = self._height//2

        self._snakeDir.append([0, 1])
        self._snake.append([self._snakeY, self._snakeX])

        for i in range(self._snake_len-1):
            self._snakeDir.append(self._snakeDir[i-1])

        for i in range(self._snake_len-1):
            self._snake.append([self._snakeY, self._snakeX-i-1])

    def show(self):
        '''Muestra el estado del juego'''
        for fila in self._gameboard:
            for columna in fila:
                sys.stdout.write(f'{columna}')
            sys.stdout.write('\n')
        sys.stdout.write(f'Score: {self._score}  |  Fruta comida: {self._fruitCount}'.center(
            self._width, ' ') + '\n')
        if debug:
            sys.stdout.write(f'{self._snake}\n')
            sys.stdout.write(f'{self._snakeDir}')

    def update(self):
        '''Actualiza los eventos del juego'''
        # Coloca la fruta en el tablero
        self._gameboard[self._fruity][self._fruitx] = f'{_RED}{_BLOCK}{_WHITE}'

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

        for i in range(self._snake_len-1, 0, -1):
            self._snakeDir[i] = self._snakeDir[i-1]

        # Dibuja la serpiente
        for i in range(self._snake_len):
            self._gameboard[self._snake[i-1][0]
                            ][self._snake[i-1][1]] = f'{_GREEN}{_BLOCK}{_WHITE}'
        self._gameboard[self._snakeY][self._snakeX] = f'{_GREEN}{_BLOCK}{_WHITE}'

    def eatFruit(self):
        '''Verifica si la serpiente comio una fruta y la regenera'''
        if self._snakeX == self._fruitx and self._snakeY == self._fruity:
            self._score += 100
            self._fruitCount += 1
            self._snake_len += 1

            tempDir = [self._snakeDir[-1][0], self._snakeDir[-1][1]]
            tempCoord = [self._snake[-1][0], self._snake[-1][1]]

            tempCoord[0] -= tempDir[0]
            tempCoord[1] -= tempDir[1]

            self._snakeDir.append(tempDir)
            self._snake.append(tempCoord)
            self.spawnFruit()

    def isDeath(self):
        '''Comprueba si el juego se termino'''
        if self._snakeX == 0 or self._snakeX == self._width-1:
            self._death = True
        if self._snakeY == 0 or self._snakeY == self._height-1:
            self._death == True
        for i in range(1, self._snake_len):
            if self._snake[i] == [self._snakeY, self._snakeX]:
                self._death = True

    def gameOverScreen(self):
        GameOverText = []
        try:
            with open('./Game_Over_text.txt', 'r', encoding='utf8') as text:
                for line in text:
                    GameOverText.append(line[:-2])
                
                posX = (self._width//2)-(len(GameOverText[0])//2)
                posY = (self._height//2)-(len(GameOverText)//2)

                for i in range(len(GameOverText)):
                    for j in range(len(GameOverText[i])):
                        self._gameboard[posY+i][posX+j] = GameOverText[i][j]
                os.system(_CLEAR)
                self.show()
        except Exception as e:
            # print(f'Error al abrir el archivo: {e}')
            print('Game Over')


    def loop(self):
        '''Loop del juego'''
        timer = FPSTimer(15)
        sys.stdout.flush()
        os.system(_CLEAR)
        while(True):
            sys.stdout.flush()
            print("\033[F"*(self._height+_TOTAL_HEIGHT))
            # print(chr(27) + "[2J")
            if msvcrt.kbhit():
                ch = ord(msvcrt.getch().lower())

                if ch == ord('w'):
                    if self._snakeDir[0] != [1, 0]:
                        self._snakeDir[0] = [-1, 0]
                elif ch == ord('d'):
                    if self._snakeDir[0] != [0, -1]:
                        self._snakeDir[0] = [0, 1]
                elif ch == ord('s'):
                    if self._snakeDir[0] != [-1, 0]:
                        self._snakeDir[0] = [1, 0]
                elif ch == ord('a'):
                    if self._snakeDir[0] != [0, 1]:
                        self._snakeDir[0] = [0, -1]
                else:
                    pass

            self.update()
            self.isDeath()
            self.show()
            if self._death == True:
                self.gameOverScreen()
                input('Presiona enter para continuar...')
                os.system(_CLEAR)
                print(f' Resultados del juego '.center(self._width, '='))
                print(f'Puntuación' + '.'*(self._width - len(str(self._score)) - 10) + f'{self._score}')
                print(f'Fruta comida' + '.'*(self._width - len(str(self._fruitCount)) - 12) + f'{self._fruitCount}')
                while True:
                    print('¿Quieres guardar tu puntaje? (s/n)'.center(self._width, ' '), end='\r')
                    save = ord(msvcrt.getch().lower())
                    print(' '*self._width)
                    if save == ord('s') or save == ord('S'):
                        name = input('Ingresa tu nombre: ')
                        try:
                            with open('./Scores.txt', 'a', encoding='utf8') as scores:
                                scores.write('%' + name + '\n')
                                # scores.write(str(self._fruitCount) + '\n')
                                scores.write(str(self._score) + '\n')
                        except Exception as e:
                            print(f'Hubo un error al guardar el puntaje: {e}')
                            input('Presiona enter para continuar')
                        finally:
                            break
                    elif save == ord('n') or save == ord('N'):
                        break
                os.system(_CLEAR)
                break
            timer.sleep()


if __name__ == '__main__':
    while True:
        os.system(_CLEAR)

        try:
            with open('./Title.txt', 'r', encoding='utf8') as text:
                title = []
                for line in text:
                    title.append(line[:-2])
                print('='*len(title[0]))
                for line in title:
                    print(line)
                print(' Menu \U0001F40D '.center(len(title[0])-1, '='))
        except Exception as e:
            print(f'Ocurrió un error al abrir el archivo: {e}')
            print('Snake \U0001F40D')

        print('''
[1] Iniciar juego
[2] Puntuaciones
[3] Opciones
[4] Salir''')

        op = input('> ')

        if op == '1':
            game = Game()
            game.startGame()
            del game
        elif op == '2':
            print()
            print(' Puntuaciones '.center(40, '='))
            try:
                with open('./Scores.txt', 'r', encoding='utf8') as scores:
                    scoreList = []
                    
                    for line in scores:
                        if line[0] == '%':
                            score = [line[1:-1], scores.readline()[0:-1]]
                            scoreList.append(score)

                    for score in scoreList:
                        print(f'{score[0]}' + '.'*(40 - len(score[0]) - len(score[1])) + score[1])

                    input('\nPresiona enter para salir...')

            except Exception as e:
                print(f'El archivo de puntajes no existe o está dañado: {e}')
        elif op == '3':
            print('Opciones')
            print(f'[1] Eliminar puntuaciones')
            print(f'[2] Regresar')
            opc = input('>')

            if opc == '1':
                print(f'¿Estas seguro? (s/n) ', end='')
                opc = input()
                if opc == 's' or opc == 'S':
                    os.remove(os.path.join('Scores.txt'))
            elif opc == '2':
                pass
            else:
                print('Opcion invalida')
                sleep(1)

        elif op == '4':
            break
        elif op == '5':
            game = Game()
            game.gameOverScreen()
            input()
