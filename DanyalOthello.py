# Name of Program: Final Project - Othello
# Date: 6/22/2021
# Author: Danyal Siddiqui
# Desc: The board game Othello (aka Reversi)

""" *Features*
- "AI" that finds all possible moves and spotlights them with a blue dot
- info displayed on left side such time played (with a lifelike timer), who is winning, moves made, number of pieces of each player, whose turn it is, etc.
- wooden background and nice colours
- sound effect when placing piece
- music to relax to
- music can be toggled on and off with 'p' key
- variety of settings to spice up the game such as board colour, music settings, and board dimensions
"""
# sound effect from https://www.youtube.com/watch?v=7skwR49UhqA
# image/icon from 

# import necessary modules
import pygame, random, math

# initialize pygame
pygame.init()

# make surface to draw on
screenSize = (1200,900)
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Danyal's Othello")  # puts a caption on window
# set the window icon
icon = pygame.image.load('pieces1.png')
pygame.display.set_icon(icon)
# initiate pygame sound effects and music
pygame.mixer.init()
pygame.mixer.music.load('music.mp3')
moveSound = pygame.mixer.Sound('sfx.mp3')

# set the clock
clock = pygame.time.Clock()
# set FPS
FPS = 60

# get screen dimensions
screenWidth = screen.get_width()
screenHeight = screen.get_height()
centerX = screenWidth/2
centerY = screenHeight/2
centerScreen = (centerX, centerY)
if screenWidth <= screenHeight:
	smaller = screenWidth
else:
	smaller = screenHeight
 
# declare colours
BLACK = (0, 0, 0)
WHITE = (255,255,255)
GREEN = (23,93,52)
DARKGREEN = (13, 43, 18)
BLUE = (13, 39, 186)
RED = (168, 30, 30)
BROWN = (51,25,0)
colourList = [GREEN, DARKGREEN, BLUE, RED]

# create the fonts that will be used
fontTitleBold = pygame.font.SysFont("Arial Black", 70, bold=True)
fontTitle = pygame.font.SysFont("Crimson Pro", 60)
fontInfo = pygame.font.SysFont("Crimson Pro", 40)
fontInfoSmall = pygame.font.SysFont("Crimson Pro", 30)

# game variables
running = True
intro = True
game = False
final = False
settings = False
saving = False
rows, columns = 8, 8
if rows <= columns:
	less = rows
else:
	less = columns
buffer = 100
gridSize = (smaller-buffer)/less
radius = gridSize/2 - 5
boardColours = [DARKGREEN, GREEN]
introBackground = pygame.image.load('felt.jpg')
introBackground = pygame.transform.scale(introBackground, (screenWidth, screenHeight))
background = pygame.image.load('wood.jpg')
background = pygame.transform.scale(background, (screenWidth, screenHeight))
pieces1 = pygame.image.load('pieces1.png')
pieces2 = pygame.image.load('pieces2.png')
playerColour = BLACK
lastTurn = True
numBlack = 2
numWhite = 2
numMoves = 0
minutes = 0
seconds = 0
# settings page selections
musicOnSelect = True
musicOffSelect = False
coloursBWSelect = True
coloursRBSelect = False
boardX4Select = False
boardY4Select = False
boardX5Select = False
boardY5Select = False
boardX6Select = False
boardY6Select = False
boardX7Select = False
boardY7Select = False
boardX8Select = True
boardY8Select = True
if musicOnSelect:
	pygame.mixer.music.play(-1)
	music = True

def captureCheck(square, latestStatus):
	# check for any captures
	global captured
	captured = []
	testing = []
	try:
		# check down direction
		for i in range(1,8):
			name = int(square) + i
			rect, colour, status = grid[str(name)]
			if status == None:
				break
			elif status == latestStatus:
				for item in testing:
					captured.append(item)
			else:
				testing.append(str(name))
	except KeyError:
		pass
	try:
		testing = []
		# check up direction
		for i in range(1,8):
			name = int(square) - i
			rect, colour, status = grid[str(name)]
			if status == None:
				break
			elif status == latestStatus:
				for item in testing:
					captured.append(item)
			else:
				testing.append(str(name))
	except KeyError:
		pass
	try:
		testing = []
		# check right direction
		for i in range(1,8):
			name = int(square) + (i*10)
			rect, colour, status = grid[str(name)]
			if status == None:
				break
			elif status == latestStatus:
				for item in testing:
					captured.append(item)
			else:
				testing.append(str(name))
	except KeyError:
		pass
	try:
		testing = []
		# check left direction
		for i in range(1,8):
			name = int(square) - (i*10)
			rect, colour, status = grid[str(name)]
			if status == None:
				break
			elif status == latestStatus:
				for item in testing:
					captured.append(item)
			else:
				testing.append(str(name))
	except KeyError:
		pass
	try:
		testing = []
		# check down-left direction
		for i in range(1,8):
			name = int(square) - (i*10) + i
			rect, colour, status = grid[str(name)]
			if status == None:
				break
			elif status == latestStatus:
				for item in testing:
					captured.append(item)
			else:
				testing.append(str(name))
	except KeyError:
		pass
	try:
		testing = []
		# check down-right direction
		for i in range(1,8):
			name = int(square) + (i*10) + i
			rect, colour, status = grid[str(name)]
			if status == None:
				break
			elif status == latestStatus:
				for item in testing:
					captured.append(item)
			else:
				testing.append(str(name))
	except KeyError:
		pass
	try:
		testing = []
		# check up-left direction
		for i in range(1,8):
			name = int(square) - (i*10) - i
			rect, colour, status = grid[str(name)]
			if status == None:
				break
			elif status == latestStatus:
				for item in testing:
					captured.append(item)
			else:
				testing.append(str(name))
	except KeyError:
		pass
	try:
		testing = []
		# check up-right direction
		for i in range(1,8):
			name = int(square) + (i*10) - i
			rect, colour, status = grid[str(name)]
			if status == None:
				break
			elif status == latestStatus:
				for item in testing:
					captured.append(item)
			else:
				testing.append(str(name))
	except KeyError:
		pass
	return captured

def moveCheck(square, latestStatus):
	# check if move is legal (it captures at least one piece)
	captured = []
	testing = []
	try:
		# check down direction
		for i in range(1,8):
			name = int(square) + i
			rect, colour, status = grid[str(name)]
			if status == None or status == BLUE:
				break
			elif status == latestStatus:
				for item in testing:
					captured.append(item)
				break
			else:
				testing.append(str(name))
	except KeyError:
		pass
	try:
		testing = []
		# check up direction
		for i in range(1,8):
			name = int(square) - i
			rect, colour, status = grid[str(name)]
			if status == None or status == BLUE:
				break
			elif status == latestStatus:
				for item in testing:
					captured.append(item)
				break
			else:
				testing.append(str(name))
	except KeyError:
		pass
	try:
		testing = []
		# check right direction
		for i in range(1,8):
			name = int(square) + (i*10)
			rect, colour, status = grid[str(name)]
			if status == None or status == BLUE:
				break
			elif status == latestStatus:
				for item in testing:
					captured.append(item)
				break
			else:
				testing.append(str(name))
	except KeyError:
		pass
	try:
		testing = []
		# check left direction
		for i in range(1,8):
			name = int(square) - (i*10)
			rect, colour, status = grid[str(name)]
			if status == None or status == BLUE:
				break
			elif status == latestStatus:
				for item in testing:
					captured.append(item)
				break
			else:
				testing.append(str(name))
	except KeyError:
		pass
	try:
		testing = []
		# check down-left direction
		for i in range(1,8):
			name = int(square) - (i*10) + i
			rect, colour, status = grid[str(name)]
			if status == None or status == BLUE:
				break
			elif status == latestStatus:
				for item in testing:
					captured.append(item)
				break
			else:
				testing.append(str(name))
	except KeyError:
		pass
	try:
		testing = []
		# check down-right direction
		for i in range(1,8):
			name = int(square) + (i*10) + i
			rect, colour, status = grid[str(name)]
			if status == None or status == BLUE:
				break
			elif status == latestStatus:
				for item in testing:
					captured.append(item)
				break
			else:
				testing.append(str(name))
	except KeyError:
		pass
	try:
		testing = []
		# check up-left direction
		for i in range(1,8):
			name = int(square) - (i*10) - i
			rect, colour, status = grid[str(name)]
			if status == None or status == BLUE:
				break
			elif status == latestStatus:
				for item in testing:
					captured.append(item)
				break
			else:
				testing.append(str(name))
	except KeyError:
		pass
	try:
		testing = []
		# check up-right direction
		for i in range(1,8):
			name = int(square) + (i*10) - i
			rect, colour, status = grid[str(name)]
			if status == None or status == BLUE:
				break
			elif status == latestStatus:
				for item in testing:
					captured.append(item)
				break
			else:
				testing.append(str(name))
	except KeyError:
		pass
	if captured:
		return True
	else:
		return False

print('Game has initialized')
# program loop
while running:
	lastTurn = True
	numBlack = 2
	numWhite = 2
	numMoves = 0
	minutes = 0
	seconds = 0
	grid = {}
	lastColour = boardColours[0]
	# use for loop to create playing board grid
	for row in range(rows):
		if lastColour == boardColours[1]:
			lastColour = boardColours[0]
		else:
			lastColour = boardColours[1]
		for col in range(columns):
			if lastColour == boardColours[0]:
				lastColour = boardColours[1]
			else:
				lastColour = boardColours[0]
			gridSquare = pygame.Rect((row*gridSize)+(screenWidth-(buffer/2)-(rows*gridSize)), (col*gridSize)+((screenHeight-(gridSize*columns))/2), gridSize, gridSize)
			squareColour = lastColour
			name = str(row) + str(col)
			if name == '33' or name == '44' and rows == 8 and columns == 8:
				grid[name] = [gridSquare, squareColour, BLACK]
			elif name == '34' or name == '43' and rows == 8 and columns == 8:
				grid[name] = [gridSquare, squareColour, WHITE]
			else:
				grid[name] = [gridSquare, squareColour, None]
	
	while saving:
		intro = True
		running = True
		settings = False
		game = False
		final = False
		saving = False

	# intro screen loop
	while intro:
		# control loop speed
		clock.tick(FPS)
		# check for an event in pygame
		for event in pygame.event.get():
			# check if user quits game
			if event.type == pygame.QUIT:
				intro = False
				game = False
				final = False
				running = False
				settings = False
			# check for mouse click
			if event.type == pygame.MOUSEBUTTONUP:
				# get position of mouse click
				mouse_pos = pygame.mouse.get_pos()
				# check for collision with rects
				if introPlayRect.collidepoint(mouse_pos):
					running = True
					game = True
					intro = False
					final = False
					settings = False
				if introSettingsRect.collidepoint(mouse_pos):
					running = True
					game = False
					intro = False
					final = False
					settings = True
				if introQuitRect.collidepoint(mouse_pos):
					running = False
					game = False
					final = False
					intro = False
					settings = False
			# check for key press
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					# game quits if user presses escape
					running = False
					game = False
					final = True
					intro = False
					settings = False
				if event.key == pygame.K_RETURN:
					# game plays if user presses enter
					running = True
					game = True
					intro = False
					final = False

		# draw intro background
		screen.blit(introBackground, (0,0))
		# draw all the text
		introTitle = fontTitleBold.render("OTHELLO", False, WHITE)
		introPlay = fontTitle.render("Play", False, WHITE)
		introSettings = fontTitle.render("Settings", False, WHITE)
		introQuit = fontTitle.render("Quit", False, WHITE)
		introTitleRect = introTitle.get_rect()
		introPlayRect = introPlay.get_rect()
		introSettingsRect = introSettings.get_rect()
		introQuitRect = introQuit.get_rect()
		introTitleRect.center = (centerX, 75)
		introSettingsRect.center = (centerX, centerY+40)
		introPlayRect.center = (centerX, introSettingsRect.top-75)
		introQuitRect.center = (centerX, introSettingsRect.bottom+75)
		screen.blit(introTitle, introTitleRect)
		screen.blit(introPlay, introPlayRect)
		screen.blit(introSettings, introSettingsRect)
		screen.blit(introQuit, introQuitRect)
		# draw intro images
		screen.blit(pieces1, (introSettingsRect.left-80-pieces1.get_width(), screenHeight*(1/3)-(pieces1.get_height()/2)))
		screen.blit(pieces2, (introSettingsRect.right+80, screenHeight*(3/4)-(pieces2.get_height()/2)))
		# update the display
		pygame.display.flip()

	while settings:
		# control loop speed
		clock.tick(FPS)
		# check for an event in pygame
		for event in pygame.event.get():
			# check if user quits game
			if event.type == pygame.QUIT:
				intro = False
				game = False
				final = False
				running = False
				settings = False
			# check for mouse click
			if event.type == pygame.MOUSEBUTTONUP:
				# get position of mouse click
				mouse_pos = pygame.mouse.get_pos()
				# check for collision with rects
				if setSaveRect.collidepoint(mouse_pos):
					# settings save if user clicks save
					running = True
					game = False
					intro = False
					final = False
					settings = False
					saving = True
				if musicOnRect.collidepoint(mouse_pos):
					pygame.mixer.music.play(-1)
					music = True
					musicOnSelect = True
					musicOffSelect = False
				if musicOffRect.collidepoint(mouse_pos):
					pygame.mixer.music.stop()
					music = False
					musicOffSelect = True
					musicOnSelect = False
				if coloursBWRect.collidepoint(mouse_pos):
					boardColours = [BLACK, WHITE]
					coloursBWSelect = True
					coloursRBSelect = False
				if coloursRBRect.collidepoint(mouse_pos):
					boardColours = [RED, BLUE]
					BLUE = GREEN
					coloursBWSelect = False
					coloursRBSelect = True
				if boardX4Rect.collidepoint(mouse_pos):
					rows = 4
					boardX4Select = True
					boardX5Select = False
					boardX6Select = False
					boardX7Select = False
					boardX8Select = False
				if boardX5Rect.collidepoint(mouse_pos):
					rows = 5
					boardX4Select = False
					boardX5Select = True
					boardX6Select = False
					boardX7Select = False
					boardX8Select = False
				if boardX6Rect.collidepoint(mouse_pos):
					rows = 6
					boardX4Select = False
					boardX5Select = False
					boardX6Select = True
					boardX7Select = False
					boardX8Select = False
				if boardX7Rect.collidepoint(mouse_pos):
					rows = 7
					boardX4Select = False
					boardX5Select = False
					boardX6Select = False
					boardX7Select = True
					boardX8Select = False
				if boardX8Rect.collidepoint(mouse_pos):
					rows = 8
					boardX4Select = False
					boardX5Select = False
					boardX6Select = False
					boardX7Select = False
					boardX8Select = True
				if boardY4Rect.collidepoint(mouse_pos):
					columns = 4
					boardY4Select = True
					boardY5Select = False
					boardY6Select = False
					boardY7Select = False
					boardY8Select = False
				if boardY5Rect.collidepoint(mouse_pos):
					columns = 5
					boardY4Select = False
					boardY5Select = True
					boardY6Select = False
					boardY7Select = False
					boardY8Select = False
				if boardY6Rect.collidepoint(mouse_pos):
					columns = 6
					boardY4Select = False
					boardY5Select = False
					boardY6Select = True
					boardY7Select = False
					boardY8Select = False
				if boardY7Rect.collidepoint(mouse_pos):
					columns = 7
					boardY4Select = False
					boardY5Select = False
					boardY6Select = False
					boardY7Select = True
					boardY8Select = False
				if boardY8Rect.collidepoint(mouse_pos):
					columns = 8
					boardY4Select = False
					boardY5Select = False
					boardY6Select = False
					boardY7Select = False
					boardY8Select = True
			# check for key press
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					# game quits if user presses escape
					running = False
					game = False
					final = True
					intro = False
					settings = False
				if event.key == pygame.K_ENTER:
					# settings save if user presses enter
					running = True
					game = False
					intro = False
					final = False
					settings = False
					saving = True

		# draw settings background
		screen.blit(introBackground, (0,0))
		# draw all the settings and options
		setTitle = fontTitleBold.render("SETTINGS", False, WHITE)
		setMusic = fontTitle.render("Music:", False, WHITE)
		musicOn = fontTitle.render("ON", False, WHITE)
		musicOff= fontTitle.render("OFF", False, WHITE)
		setColours = fontTitle.render("Piece colours:", False, WHITE)
		coloursBW = fontTitle.render("B&W", False, WHITE)
		coloursRB = fontTitle.render("R&B", False, WHITE)
		setBoardX = fontTitle.render("Board X:", False, WHITE)
		boardX4 = fontTitle.render("4", False, WHITE)
		boardX5 = fontTitle.render("5", False, WHITE)
		boardX6 = fontTitle.render("6", False, WHITE)
		boardX7 = fontTitle.render("7", False, WHITE)
		boardX8 = fontTitle.render("8", False, WHITE)
		setBoardY = fontTitle.render("Board Y:", False, WHITE)
		boardY4 = fontTitle.render("4", False, WHITE)
		boardY5 = fontTitle.render("5", False, WHITE)
		boardY6 = fontTitle.render("6", False, WHITE)
		boardY7 = fontTitle.render("7", False, WHITE)
		boardY8 = fontTitle.render("8", False, WHITE)
		setSave = fontTitle.render("SAVE", False, WHITE)
		setTitleRect = setTitle.get_rect()
		setMusicRect = setMusic.get_rect()
		musicOnRect = musicOn.get_rect()
		musicOffRect = musicOff.get_rect()
		setColoursRect = setColours.get_rect()
		coloursBWRect = coloursBW.get_rect()
		coloursRBRect = coloursRB.get_rect()
		setBoardXRect = setBoardX.get_rect()
		boardX4Rect = boardX4.get_rect()
		boardX5Rect = boardX5.get_rect()
		boardX6Rect = boardX6.get_rect()
		boardX7Rect = boardX7.get_rect()
		boardX8Rect = boardX8.get_rect()
		setBoardYRect = setBoardY.get_rect()
		boardY4Rect = boardY4.get_rect()
		boardY5Rect = boardY5.get_rect()
		boardY6Rect = boardY6.get_rect()
		boardY7Rect = boardY7.get_rect()
		boardY8Rect = boardY8.get_rect()
		setSaveRect = setSave.get_rect()
		setTitleRect.center = (centerX, 75)
		setMusicRect.center = (centerX-150, setTitleRect.bottom+150)
		musicOnRect.center = (centerX+150, setTitleRect.bottom+150)
		musicOffRect.center = (musicOnRect.right+100, setTitleRect.bottom+150)
		setColoursRect.center = (centerX-150, setMusicRect.bottom+75)
		coloursBWRect.center = (centerX+125, setMusicRect.bottom+75)
		coloursRBRect.center = (coloursBWRect.right+75, setMusicRect.bottom+75)
		setBoardXRect.center = (centerX-150, setColoursRect.bottom+75)
		boardX4Rect.center = (centerX+150, setColoursRect.bottom+75)
		boardX5Rect.center = (boardX4Rect.right+50, setColoursRect.bottom+75)
		boardX6Rect.center = (boardX5Rect.right+50, setColoursRect.bottom+75)
		boardX7Rect.center = (boardX6Rect.right+50, setColoursRect.bottom+75)
		boardX8Rect.center = (boardX7Rect.right+50, setColoursRect.bottom+75)
		setBoardYRect.center = (centerX-150, setBoardXRect.bottom+75)
		boardY4Rect.center = (centerX+150, setBoardXRect.bottom+75)
		boardY5Rect.center = (boardY4Rect.right+50, setBoardXRect.bottom+75)
		boardY6Rect.center = (boardY5Rect.right+50, setBoardXRect.bottom+75)
		boardY7Rect.center = (boardY6Rect.right+50, setBoardXRect.bottom+75)
		boardY8Rect.center = (boardY7Rect.right+50, setBoardXRect.bottom+75)
		setSaveRect.center = (centerX, screenHeight-75)

		# draw the option selected boxes
		if musicOnSelect:
			pygame.draw.rect(screen, BLACK, musicOnRect)
		if musicOffSelect:
			pygame.draw.rect(screen, BLACK, musicOffRect)
		if coloursBWSelect:
			pygame.draw.rect(screen, BLACK, coloursBWRect)
		if coloursRBSelect:
			pygame.draw.rect(screen, BLACK, coloursRBRect)
		if boardX4Select:
			pygame.draw.rect(screen, BLACK, boardX4Rect)
		if boardX5Select:
			pygame.draw.rect(screen, BLACK, boardX5Rect)
		if boardX6Select:
			pygame.draw.rect(screen, BLACK, boardX6Rect)
		if boardX7Select:
			pygame.draw.rect(screen, BLACK, boardX7Rect)
		if boardX8Select:
			pygame.draw.rect(screen, BLACK, boardX8Rect)
		if boardY4Select:
			pygame.draw.rect(screen, BLACK, boardY4Rect)
		if boardY5Select:
			pygame.draw.rect(screen, BLACK, boardY5Rect)
		if boardY6Select:
			pygame.draw.rect(screen, BLACK, boardY6Rect)
		if boardY7Select:
			pygame.draw.rect(screen, BLACK, boardY7Rect)
		if boardY8Select:
			pygame.draw.rect(screen, BLACK, boardY8Rect)

		# blit everything to screen
		screen.blit(setTitle, setTitleRect)
		screen.blit(setMusic, setMusicRect)
		screen.blit(musicOn, musicOnRect)
		screen.blit(musicOff, musicOffRect)
		screen.blit(setColours, setColoursRect)
		screen.blit(coloursBW, coloursBWRect)
		screen.blit(coloursRB, coloursRBRect)
		screen.blit(setBoardX, setBoardXRect)
		screen.blit(boardX4, boardX4Rect)
		screen.blit(boardX5, boardX5Rect)
		screen.blit(boardX6, boardX6Rect)
		screen.blit(boardX7, boardX7Rect)
		screen.blit(boardX8, boardX8Rect)
		screen.blit(setBoardY, setBoardYRect)
		screen.blit(boardY4, boardY4Rect)
		screen.blit(boardY5, boardY5Rect)
		screen.blit(boardY6, boardY6Rect)
		screen.blit(boardY7, boardY7Rect)
		screen.blit(boardY8, boardY8Rect)
		screen.blit(setSave, setSaveRect)

		# update the display
		pygame.display.flip()

	current = pygame.time.get_ticks()
	# game loop
	while game:
		# control loop speed
		clock.tick(FPS)
		# check for an event in pygame
		for event in pygame.event.get():
			# check if user quits game
			if event.type == pygame.QUIT:
				intro = False
				game = False
				final = False
				running = False
				settings = False
			# check for mouse click
			if event.type == pygame.MOUSEBUTTONUP:
				# get position of mouse click
				mouse_pos = pygame.mouse.get_pos()
				# check for collision in each square
				for square in grid:
					rect, colour, status = grid[square]
					# check for collision
					if rect.collidepoint(mouse_pos):
						# make sure square is empty
						if status == BLUE:
							# add piece to square
							grid[square] = rect, colour, playerColour
							latestStatus = playerColour
							flipColour = latestStatus
							numMoves += 1
							numBlack = 0
							numWhite = 0
							# play sound effect
							moveSound.play()
							# switch player colours after a move
							if playerColour == BLACK:
								playerColour = WHITE
							elif playerColour == WHITE:
								playerColour = BLACK
							# execute captures
							for capturedSquare in captureCheck(square, latestStatus):
								rect, colour, status = grid[capturedSquare]
								if status == WHITE or status == BLACK:
									grid[capturedSquare] = [rect, colour, flipColour]
							for square in grid:
								rect, colour, status = grid[square]
								if status == BLACK:
									numBlack += 1
								elif status == WHITE:
									numWhite += 1

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					# game quits if user presses escape
					running = False
					game = False
					final = True
					intro = False
					settings = False
				if event.key == pygame.K_p:
					# pause or play music
					if music:
						pygame.mixer.music.stop()
						music = False
					else:
						pygame.mixer.music.play(-1)
						music = True

		# drawing the board and pieces
		screen.blit(background, (0,0))
		for square in grid:
			rect, colour, status = grid[square]
			pygame.draw.rect(screen, colour, rect)
			if status == WHITE:
				pygame.draw.circle(screen, WHITE, rect.center, radius)
			elif status == BLACK:
				pygame.draw.circle(screen, BLACK, rect.center, radius)
			elif status == BLUE:
				pygame.draw.circle(screen, BLUE, rect.center, radius/4)

		# writing and drawing the info on the side
		if numBlack > numWhite:
			winning = 'Black'
		elif numBlack == numWhite:
			winning = 'Tied'
		else:
			winning = 'White'
		time = math.trunc((pygame.time.get_ticks()-current)/1000)
		seconds = time % 60
		if seconds < 10:
			seconds = '0' + str(seconds)
		minutes = math.trunc(time/60)
		infoTurn = fontInfo.render("Turn:", False, WHITE)
		infoBlack = fontInfo.render("Black pieces: " + str(numBlack), False, WHITE)
		infoWhite = fontInfo.render("White pieces: " + str(numWhite), False, WHITE)
		infoWinning = fontInfo.render("Winning: " + str(winning), False, WHITE)
		infoMoves = fontInfo.render("Moves made: " + str(numMoves), False, WHITE)
		infoTime = fontInfo.render("Time played: " + str(minutes) + ':' + str(seconds), False, WHITE)
		infoMusic = fontInfoSmall.render("Press 'P' to toggle music!", False, WHITE)
		infoTurnRect = infoTurn.get_rect()
		infoBlackRect = infoBlack.get_rect()
		infoWhiteRect = infoWhite.get_rect()
		infoWinningRect = infoWinning.get_rect()
		infoMovesRect = infoMoves.get_rect()
		infoTimeRect = infoTime.get_rect()
		infoMusicRect = infoMusic.get_rect()
		infoTurnRect.topleft = (10, screenHeight*(1/10))
		infoBlackRect.topleft = (10, screenHeight*(2/10))
		infoWhiteRect.topleft = (10, screenHeight*(3/10))
		infoWinningRect.topleft = (10, screenHeight*(4/10))
		infoMovesRect.topleft = (10, screenHeight*(5/10))
		infoTimeRect.topleft = (10, screenHeight*(6/10))
		infoMusicRect.bottomleft = (10, screenHeight-10)
		if playerColour == BLACK:
			pygame.draw.circle(screen, BLACK, (int(infoTurnRect.right+radius+20), int(infoTurnRect.centery)), int(radius*(3/4)))
		else:
			pygame.draw.circle(screen, WHITE, (int(infoTurnRect.right+radius+20), int(infoTurnRect.centery)), int(radius*(3/4)))
		screen.blit(infoTurn, infoTurnRect)
		screen.blit(infoBlack, infoBlackRect)
		screen.blit(infoWhite, infoWhiteRect)
		screen.blit(infoWinning, infoWinningRect)
		screen.blit(infoMoves, infoMovesRect)
		screen.blit(infoTime, infoTimeRect)
		screen.blit(infoMusic, infoMusicRect)

		# check for possible moves and change status accordingly
		for square in grid:
			rect, colour, status = grid[square]
			if moveCheck(square, playerColour):
				if status == None:
					grid[square] = rect, colour, BLUE
			else:
				if status == BLUE:
					grid[square] = rect, colour, None

		# check if their are any possible moves
		for square in grid:
			rect, colour, status = grid[square]
			if status == BLUE:
				moves = True
				lastTurn = True
				break
			else:
				moves = False
		# if there are none...
		if moves == False:
			# check if game is over
			if lastTurn == False:
				game = False
				final = True
			# switch player colours to skip a turn
			if playerColour == BLACK:
				playerColour = WHITE
			elif playerColour == WHITE:
				playerColour = BLACK
			lastTurn = False
		
		# update the screen
		pygame.display.flip()

	# final screen loop
	while final:
		# control loop speed
		clock.tick(FPS)
		# check for an event in pygame
		for event in pygame.event.get():
			# check if user quits game
			if event.type == pygame.QUIT:
				intro = False
				game = False
				final = False
				running = False
				settings = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					# game quits if user presses escape
					running = False
					game = False
					final = False
					intro = False
					settings = False
				if event.key == pygame.K_p:
					# pause or play music
					if music:
						pygame.mixer.music.stop()
						music = False
					else:
						pygame.mixer.music.play(-1)
						music = True
			# check for mouse click
			if event.type == pygame.MOUSEBUTTONUP:
				# get position of mouse click
				mouse_pos = pygame.mouse.get_pos()
				# check for collision in each square
				if finalRestartRect.collidepoint(mouse_pos):
					# restart the game
					running = True
					game = False
					final = False
					intro = True
					settings = False
		# blit background image to screen
		screen.blit(background, (0,0))
		# draw all the text
		if winning == 'Black':
			finalScore1 = fontTitle.render(str(numBlack) + " ", False, BLACK)
			finalScore2 = fontTitle.render(" to " + str(numWhite), False, WHITE)
		else:
			finalScore1 = fontTitle.render(str(numWhite) + " ", False, WHITE)
			finalScore2 = fontTitle.render(" to " + str(numBlack) + " ", False, BLACK)
		if winning == 'Tied':
			finalWinner = fontTitle.render("It's a tie!", False, WHITE)			
		else:
			finalWinner = fontTitle.render(str(winning) + " won!", False, WHITE)
		finalMoves = fontTitle.render("Moves made: " + str(numMoves), False, WHITE)
		finalTime = fontTitle.render("Time played: " + str(minutes) + ':' + str(seconds), False, WHITE)
		finalRestart = fontTitle.render("RESTART", False, BLACK)
		finalScore1Rect = finalScore1.get_rect()
		finalScore2Rect = finalScore2.get_rect()
		finalWinnerRect = finalWinner.get_rect()
		finalMovesRect = finalMoves.get_rect()
		finalTimeRect = finalTime.get_rect()
		finalRestartRect = finalRestart.get_rect()
		finalWinnerRect.center = (centerX, centerY-100)
		finalScore1Rect.center = (centerX-70, finalWinnerRect.bottom+50)
		finalScore2Rect.center = (finalScore1Rect.right+50, finalWinnerRect.bottom+50)
		finalMovesRect.center = (screenWidth*(1/3), screenHeight*(3/4))
		finalTimeRect.center = (screenWidth*(2/3), screenHeight*(3/4))
		finalRestartRect.center = (centerX, screenHeight-100)
		pygame.draw.rect(screen, WHITE, finalRestartRect)
		screen.blit(finalScore1, finalScore1Rect)
		screen.blit(finalScore2, finalScore2Rect)
		screen.blit(finalWinner, finalWinnerRect)
		screen.blit(finalMoves, finalMovesRect)
		screen.blit(finalTime, finalTimeRect)
		screen.blit(finalRestart, finalRestartRect)
		# update the display
		pygame.display.flip()

print('----------------------------\nThanks for playing my game! \n-Danyal')