from config import Config
from snake import Snake
from food import Food
import pygame,  sys

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
        pygame.display.set_caption('Snake')
        self.food = Food()
        self.snake = Snake()
        
    def drawGrid(self):
        for x in range(0, Config.WINDOW_WIDTH, Config.CELLSIZE): #draw vertical lines
            pygame.draw.line(self.screen, Config.DARKGRAY, (x, 0), (x, Config.WINDOW_HEIGHT))
            
        for y in range(0, Config.WINDOW_HEIGHT, Config.CELLSIZE): #draw horizontal lines
            pygame.draw.line(self.screen, Config.DARKGRAY, (0, y), (Config.WINDOW_WIDTH, y))
            
    def drawSnake(self):
        for coord in self.snake.snakeCoords:
            x = coord['x'] * Config.CELLSIZE
            y = coord['y'] * Config.CELLSIZE
            snakeSegmentRect = pygame.Rect(x, y, Config.CELLSIZE, Config.CELLSIZE)
            pygame.draw.rect(self.screen, Config.DARKGREEN, snakeSegmentRect)
            snakeInnnerSegmentRect = pygame.Rect(x + 4, y + 4, Config.CELLSIZE - 8, Config.CELLSIZE - 8)
            pygame.draw.rect(self.screen, Config.GREEN, snakeInnnerSegmentRect)
    def drawFood(self):
        x = self.food.x * Config.CELLSIZE
        y = self.food.x * Config.CELLSIZE
        foodRect = pygame.Rect(x, y, Config.CELLSIZE, Config.CELLSIZE)
        pygame.draw.rect(self.screen, Config.RED, foodRect)
    def drawScore(self, score):
        scoreSurf = self.BASICFONT.render('Score: %s' % (score), True, Config.WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (Config.WINDOW_WIDTH - 120, 10)
        self.screen.blit(scoreSurf, scoreRect)
    
    def draw(self):
        self.screen.fill(Config.BG_COLOR)
        # we'll draw our snake, grid, food, score
        self.drawGrid()
        self.drawSnake()
        self.drawFood()
        self.drawScore(len(self.snake.snakeCoords) - 3)
        pygame.display.update()
        self.clock.tick(Config.FPS)
        
     def checkForKeyPress(self):
      if len(pygame.event.get(pygame.QUIT)) > 0:
          pygame.quit()

      keyUpEvents = pygame.event.get(pygame.KEYUP)

      if len(keyUpEvents) == 0:
          return None

      if keyUpEvents[0].key == pygame.K_ESCAPE:
          pygame.quit()
          quit()

      return keyUpEvents[0].key   
        
    def handleKeyEvents(self, event):
    if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.snake.direction != self.snake.RIGHT:
        self.snake.direction = self.snake.LEFT
    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.snake.direction != self.snake.LEFT:
        self.snake.direction = self.snake.RIGHT
    elif (event.key == pygame.K_UP or event.key == pygame.K_w) and self.snake.direction != self.snake.DOWN:
        self.snake.direction = self.snake.UP
    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.snake.direction != self.snake.UP:
        self.snake.direction = self.snake.DOWN
    elif event.key == pygame.K_ESCAPE:
        pygame.quit()
            
    def resetGame(self):
        del self.snake
        del self.food
        self.snake = Snake()
        self.food = Food()
        
        return True
    
    def drawPressKeyMsg(self):
      pressKeySurf = self.BASICFONT.render(
          'Press a key to play.', True, Config.DARKGRAY)
      pressKeyRect = pressKeySurf.get_rect()
      pressKeyRect.topleft = (Config.WINDOW_WIDTH - 200,
                              Config.WINDOW_HEIGHT - 30)
      self.screen.blit(pressKeySurf, pressKeyRect)
    
            
    def isGameOver(self):
        if (self.snake.snakeCoords[self.snake.HEAD]['x'] == - 1 or self.snake.snakeCoords[self.snake.HEAD]['x'] == Config.CELLWIDTH or
            self.snake.snakeCoords[self.snake.HEAD]['y'] == -1 or self.snake.snakeCoords[self.snake.HEAD]['y'] == Config.CELLHEIGHT):
            return self.resetGame()
        for snakeBody in self.snake.snakeCoords[1:]:
            if snakeBody['x'] == self.snake.snakeCoords[self.snake.HEAD]['x'] and snakeBody['y'] == self.snake.snakeCoords[self.snake.HEAD]['y']:
                return self.resetGame()
     def displayGameOver(self):
      gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
      gameSurf = gameOverFont.render('Game', True, Config.WHITE)
      overSurf = gameOverFont.render('Over', True, Config.WHITE)
      gameRect = gameSurf.get_rect()
      overRect = overSurf.get_rect()
      gameRect.midtop = (Config.WINDOW_WIDTH / 2, 10)
      overRect.midtop = (Config.WINDOW_WIDTH / 2, gameRect.height + 10 + 25)
      self.screen.blit(gameSurf, gameRect)
      self.screen.blit(overSurf, overRect)

      self.drawPressKeyMsg()
      pygame.display.update()
      pygame.time.wait(500)

      self.checkForKeyPress()  # clear out any key presses in the event queue
      while True:
          if self.checkForKeyPress():
              pygame.event.get()  # clear event queue
              return

  def showStartScreen(self):
      titleFont = pygame.font.Font('freesansbold.ttf', 100)
      titleSurf1 = titleFont.render(
          'Wormy!', True, Config.WHITE, Config.DARKGREEN)
      titleSurf2 = titleFont.render('Wormy!', True, Config.GREEN)
      degrees1 = 0
      degrees2 = 0

      while True:
          for event in pygame.event.get():
              if event.type == pygame.KEYDOWN:
                  return
          self.screen.fill(Config.BG_COLOR)
          rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
          rotatedRect1 = rotatedSurf1.get_rect()
          rotatedRect1.center = (Config.WINDOW_WIDTH / 2,
                                  Config.WINDOW_HEIGHT / 2)
          self.screen.blit(rotatedSurf1, rotatedRect1)

          rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
          rotatedRect2 = rotatedSurf2.get_rect()
          rotatedRect2.center = (Config.WINDOW_WIDTH / 2,
                                  Config.WINDOW_HEIGHT / 2)
          self.screen.blit(rotatedSurf2, rotatedRect2)

          self.drawPressKeyMsg()

          pygame.display.update()
          self.clock.tick(Config.MENU_FPS)
          degrees1 += 1  # rotate by 3 degrees each frame
          degrees2 += 2  # rotate by 7 degrees each frame
    
    def run(self):
        while True:
            self.gameLoop()
            self.displayGameOver()
    
    def gameLoop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    self.handlekeyEvents(event)
                    
            self.snake.update(self.food)
            self.draw()
            if self.isGameOver():
                break
                    
