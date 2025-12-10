import curses, random, time


def spawn_snake(screen):
	for i in range(3):
		screen.addch(1, i+1, curses.ACS_BLOCK)
		screen.refresh()
		time.sleep(0.25)
	snake = [(1, 1), (1, 2), (1, 3)]
	return snake
	
def move(screen):
	pass

def main(screen):
	curses.update_lines_cols()
	snake = spawn_snake(screen)

if __name__ == "__main__":
	curses.wrapper(main)
