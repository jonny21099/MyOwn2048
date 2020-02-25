import random as rnd
import os
import sys

class Grid():
    def __init__(self, row=4, col=4, initial=2):
        self.row = row                              # number of rows in grid
        self.col = col                              # number of columns in grid
        self.initial = initial                      # number of initial cells filled
        self.score = 0

        self._grid = self.createGrid(row, col)    # creates the grid specified above

        self.emptiesSet = list(range(row * col))    # list of empty cells

        for _ in range(self.initial):               # assignation to two random cells
            self.assignRandCell(init=True)
        
        
    def createGrid(self, row, col):
        col_list = []
        for number in range(col):
            col_list.append([0,0,0,0])
        
        return col_list

    
    def setCell(self, cell, val):
        if cell <= 3:
            self._grid[0][cell] = val
        elif cell > 3 and cell <= 7:
            self._grid[1][cell-4] = val            
        elif cell > 7 and cell <= 11:
            self._grid[2][cell-8] = val
        elif cell > 11 and cell <= 15:
            self._grid[3][cell-12] = val
        else:
            print("The cell number you have entered is not in the range")

        

    def getCell(self, cell):
        if cell <= 3:
            cell = self._grid[0][cell]
        elif cell > 3 and cell <= 7:
            cell = self._grid[1][cell-4]
        elif cell > 7 and cell <= 11:
            cell = self._grid[2][cell-8]
        elif cell > 11 and cell <= 15:
            cell = self._grid[3][cell-12]
        else:
            print("The cell number you have entered is not in the range")
        return cell


    def assignRandCell(self, init=False):


        if len(self.emptiesSet):

            cell = rnd.sample(self.emptiesSet, 1)[0]
            if init:
                self.setCell(cell, 2)
            else:
                cdf = rnd.random()
                if cdf > 0.75:
                    self.setCell(cell, 4)
                else:
                    self.setCell(cell, 2)
            self.emptiesSet.remove(cell)
        

    def drawGrid(self):

        for i in range(self.row):
            line = '\t|'
            for j in range(self.col):
                if not self.getCell((i * self.row) + j):
                    line += ' '.center(5) + '|'
                else:
                    line += str(self.getCell((i * self.row) + j)).center(5) + '|'
            print(line)
        print()


    def updateEmptiesSet(self):
        self.emptiesSet = []
        for num in range(16):
            if self.getCell(num) == 0:
                self.emptiesSet.append(num)
          
         
                

    def collapsible(self):

        for num in range(0,16):
            if self.getCell(num) == 0:
                return True

        #this covers both the left and right collapse if the numbers were equal
            for num in range(1,4):
                if self.getCell(num) == self.getCell(num-1):
                    return True
            for num in range(5,8):
                if self.getCell(num) == self.getCell(num-1):
                    return True
            for num in range(9,12):
                if self.getCell(num) == self.getCell(num-1):
                    return True
            for num in range(13,16):
                if self.getCell(num) == self.getCell(num-1):
                    return True

        #testing the top and bot collapse if the numbers were equal
        else:
            for num in range(4,13,4):
                if self.getCell(num) == self.getCell(num-4):
                    return True
            for num in range(5,14,4):
                if self.getCell(num) == self.getCell(num-4):
                    return True
            for num in range(6,15,4):
                if self.getCell(num) == self.getCell(num-4):
                    return True
            for num in range(7,16,4):
                if self.getCell(num) == self.getCell(num-4):
                    return True
    
        return False


    def collapseRow(self, lst):
        collapse = False

        firstlist = []
        collapselist = []
        #used enumerate after a friend Kevin Li found it online, found more information on it in the builtin function python page, I tested it and now i understand its use.
        if lst == [0,0,0,0]:
            collapselist.append(0)
        newlist = list(enumerate(lst,start=1))
        for num in range(4):
            if newlist[num][1] != 0:
                firstlist.append(newlist[num][1])
            
                
        for num in range(len(firstlist)):
            try:
                if firstlist[num] == firstlist[num+1]:
                    sum = firstlist[num] + firstlist[num+1]
                    self.score += sum
                    collapselist.append(sum)
                    firstlist[num] = 0
                    firstlist[num+1] = 0

                elif firstlist[num] != firstlist[num+1] and firstlist[num] != 0:
                    collapselist.append(firstlist[num])
                    
            except IndexError:
                continue
            
            finally:
                enumeratedlist = list(enumerate(firstlist,start=1))
                if enumeratedlist[num][0] == len(firstlist):
                    collapselist.append(firstlist[num])
        
        if len(collapselist) == 1:
            collapselist.append(0)
            collapselist.append(0)
            collapselist.append(0)

        if len(collapselist) == 2:
            collapselist.append(0)
            collapselist.append(0)

        if len(collapselist) == 3:
            collapselist.append(0)

        if collapselist != lst:
            collapse = True
    
        return collapselist,collapse
        
    def collapseLeft(self):
        collapse = False
        for num in range(4):
            self._grid[num] = self.collapseRow(self._grid[num])
            if self._grid[num][1] == True:
                collapse = True
            self._grid[num] = self._grid[num][0]

        return collapse

    def collapseRight(self):
        collapse = False
        oldlist = []
        newlist = []
        for num in range(4):
            oldlist.append(self._grid[num])
            newlist.append(list(reversed(self._grid[num])))
            self._grid[num] = self.collapseRow(newlist[num])
            self._grid[num] = list(reversed(self._grid[num][0]))
        if oldlist != self._grid:
            collapse = True
        return collapse

    def collapseUp(self):
        collapse = False
        collapselist = []
        checklist = [] 
        for num in range(4):
            for a in range(4):
                collapselist.append(self._grid[a][num])
                if len(collapselist) == 4:
                    aftercollapse = self.collapseRow(collapselist)
                    for b in range(4):
                        self._grid[b][num] = aftercollapse[0][b]
                    checklist.append(str(aftercollapse[1]))
                    collapselist = []
        if "True" in checklist:
            collapse = True
        return collapse
        

    def collapseDown(self):
        collapse = False
        oldlist = []
        newlist = []
        checklist = []
        for num in range(4):
            oldlist.append(self._grid[num])
            for a in range(4):
                newlist.append(self._grid[a][num])
                if len(newlist) == 4:
                    collapsereverse = self.collapseRow(list(reversed(newlist)))
                    collapsereverse11 =  list(reversed(collapsereverse[0]))
                    if collapsereverse[1] == True:
                        collapse = True
                    for b in range(4):
                        self._grid[b][num] = collapsereverse11[b]
                    newlist = []

        return collapse


class Game():
    def __init__(self, row=4, col=4, initial=2):

        """
        Creates a game grid and begins the game
        """

        self.game = Grid(row, col, initial)
        self.play()


    def printPrompt(self):

        """
        Prints the instructions and the game grid with a move prompt
        """

        if sys.platform == 'win32':
            os.system("cls")
        else:
            os.system("clear")

        print('Press "w", "a", "s", or "d" to move Up, Left, Down or Right respectively.')
        print('Enter "p" to quit.\n')
        self.game.drawGrid()
        print('\nScore: ' + str(self.game.score))


    def play(self):

        moves = {'w' : 'Up',
                 'a' : 'Left',
                 's' : 'Down',
                 'd' : 'Right'}

        stop = False
        collapsible = True

        while not stop and collapsible:
            self.printPrompt()
            key = input('\nEnter a move: ')

            while not key in list(moves.keys()) + ['p']:
                self.printPrompt()
                key = input('\nEnter a move: ')

            if key == 'p':
                stop = True
            else:
                move = getattr(self.game, 'collapse' + moves[key])
                collapsed = move()

                if collapsed:
                    self.game.updateEmptiesSet()
                    self.game.assignRandCell()

                collapsible = self.game.collapsible()

        if not collapsible:
            if sys.platform == 'win32':
                os.system("cls")
            else:
                os.system("clear")
            print()
            self.game.drawGrid()
            print('\nScore: ' + str(self.game.score))
            print('No more legal moves.')

def main():
    grid = Grid()
    game = Game()

main()


