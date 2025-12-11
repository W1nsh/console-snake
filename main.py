import curses, time, random
import config

def spawn_snake(screen):
	scorer(screen, 0)
	for i in range(3, 6):
		screen.addch(10, i, curses.ACS_BLOCK, curses.color_pair(1))
		screen.refresh()
		time.sleep(0.25)
	snake = [(10, 3), (10, 4), (10, 5)]
	return snake

def change_move_to(screen, move_to: str):
	screen.timeout(100)
	ascii_code = screen.getch()
	match ascii_code:
		case curses.KEY_UP:
			move_to = 'up' if move_to != 'down' else move_to
		case curses.KEY_DOWN:
			move_to = 'down' if move_to != 'up' else move_to
		case curses.KEY_LEFT:
			move_to = 'left' if move_to != 'right' else move_to
		case curses.KEY_RIGHT:
			move_to = 'right' if move_to != 'left' else move_to
	return move_to

def generate_food(screen, snake):
	while True:
		food_y = random.randint(5, curses.LINES - 3)
		food_x = random.randint(3, curses.COLS - 3)
		food_yx = (food_y, food_x)
		if food_yx not in snake:
			screen.addch(food_y, food_x, curses.ACS_DIAMOND, curses.color_pair(1))
			screen.refresh()
			time_spawn_food = time.time()
			return food_yx, time_spawn_food

def move(screen, snake, move_to: str, food_yx, score: int):
	res = {}
	head_y, head_x = snake[-1]
	old_tail_y, old_tail_x = snake[0]
	match move_to:
		case 'up':
			new_head = (head_y - 1, head_x)
		case 'down':
			new_head = (head_y + 1, head_x)
		case 'left':
			new_head = (head_y, head_x - 1)
		case 'right':
			new_head = (head_y, head_x + 1)
	if (new_head in snake or 
		new_head[0] in [0, 1, 2, 3, 4, curses.LINES, curses.LINES - 1, curses.LINES - 2] or 
		new_head[1] in [0, 1, 2, curses.COLS, curses.COLS - 1, curses.COLS - 2]):
		game_over(screen, score)
		res['is_game'] = False
		return res
	snake.append(new_head)
	screen.addch(new_head[0], new_head[1], curses.ACS_BLOCK, curses.color_pair(1))
	if new_head != food_yx:
		snake.pop(0)
		screen.addch(old_tail_y, old_tail_x, ' ')
	else:
		score += 1
	screen.refresh()
	res['is_game'] = True
	res['score'] = score
	return res
	
def game_over(screen, score):
	screen.clear()
	screen.addstr("Game Over.\n", curses.color_pair(1))
	screen.addstr(str(score), curses.color_pair(1))
	screen.refresh()
	time.sleep(3)
	screen.timeout(-1)
	screen.getch()

def food_del(screen, food_yx):
	food_y, food_x = food_yx
	screen.addch(food_y, food_x, ' ')
	screen.refresh()

def food_time(time_spawn_food):
	current_time = time.time()
	if current_time - time_spawn_food > 15:
		return True
	return False

def border(screen):
	range_cols = curses.COLS - 2
	range_lines = curses.LINES - 2
	screen.addstr(2, 3, 'Console-Snake. Developed by W1nsh.', curses.color_pair(1))
	screen.addch(4, 2, curses.ACS_ULCORNER, curses.color_pair(1))
	screen.addch(4, range_cols, curses.ACS_URCORNER, curses.color_pair(1))
	screen.addch(range_lines, 2, curses.ACS_LLCORNER, curses.color_pair(1))
	screen.addch(range_lines, range_cols, curses.ACS_LRCORNER, curses.color_pair(1))
	for i in range(3, range_cols):
		screen.addch(4, i, curses.ACS_HLINE, curses.color_pair(1))
		screen.addch(range_lines, i, curses.ACS_HLINE, curses.color_pair(1))
	for i in range(5, range_lines):
		screen.addch(i, 2, curses.ACS_VLINE, curses.color_pair(1))
		screen.addch(i, range_cols, curses.ACS_VLINE, curses.color_pair(1))
	screen.refresh()

def scorer(screen, score):
	screen.addstr(2, 47, f'Score: {score}', curses.color_pair(1))
	screen.refresh()

def configer_color_theme():
	colors_for_themes ={
		'black': curses.COLOR_BLACK,
		'blue': curses.COLOR_BLUE,
		'cyan': curses.COLOR_CYAN,
		'green': curses.COLOR_GREEN,
		'magenta': curses.COLOR_MAGENTA,
		'red': curses.COLOR_RED,
		'white': curses.COLOR_WHITE,
		'yellow': curses.COLOR_YELLOW
	}
	curses.init_pair(1, 
				colors_for_themes.get(config.base_of_color_theme, curses.COLOR_MAGENTA), 
				colors_for_themes.get(config.background_of_color_theme, curses.COLOR_BLACK))

def game(screen):
	is_game = True
	border(screen)
	snake = spawn_snake(screen)
	generated_first_food = False
	time_spawn_food = 0
	score = 0
	move_to = 'right'
	while is_game:
		scorer(screen, score)
		move_to = change_move_to(screen, move_to)
		if food_time(time_spawn_food):
			if generated_first_food:
				food_del(screen, food_yx)
			elif not generated_first_food:
				generated_first_food = True
			food_yx, time_spawn_food = generate_food(screen, snake)
		game_progress = move(screen, snake, move_to, food_yx, score)
		is_game = game_progress['is_game']
		score = game_progress.get('score', False)


def main(screen):
	configer_color_theme()
	curses.update_lines_cols()
	curses.curs_set(0)
	game(screen)
	

if __name__ == '__main__':
	curses.wrapper(main)