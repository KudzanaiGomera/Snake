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
            
    def isGameOver(self):
        if (self.snake.snakeCoords[self.snake.HEAD]['x'] == - 1 or self.snake.snakeCoords[self.snake.HEAD]['x'] == Config.CELLWIDTH or
            self.snake.snakeCoords[self.snake.HEAD]['y'] == -1 or self.snake.snakeCoords[self.snake.HEAD]['y'] == Config.CELLHEIGHT):
            return self.resetGame()
        for snakeBody in self.snake.snakeCoords[1:]:
            if snakeBody['x'] == self.snake.snakeCoords[self.snake.HEAD]['x'] and snakeBody['y'] == self.snake.snakeCoords[self.snake.HEAD]['y']:
                return self.resetGame()
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
                    