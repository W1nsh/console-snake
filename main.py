import curses, time, random
import config

def spawn_snake(screen, border_values: dict):
	snake_line = 10
	beginning_body = border_values['left'] + 1
	end_body = beginning_body + 3
	graphic_spawn_snake(screen, snake_line, beginning_body, end_body)
	snake = logic_spawn_snake(snake_line, beginning_body, end_body)
	return snake


def graphic_spawn_snake(screen, snake_line: int, beginning_body: int, end_body: int):
	for i in range(beginning_body, end_body):
		screen.addch(snake_line, i, curses.ACS_BLOCK, curses.color_pair(1))
		screen.refresh()
		time.sleep(0.1)


def logic_spawn_snake(snake_line: int, beginning_body: int, end_body: int):
	return [(snake_line, i) for i in range(beginning_body, end_body)]


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


def generate_food(screen, snake: list[tuple[int, int]], border_values: dict):
	cp = curses.color_pair(1)

	min_y = border_values['up'] + 1
	max_y = border_values['down'] - 1
	min_x = border_values['left'] + 1
	max_x = border_values['right'] - 1

	while True:
		food_y = random.randint(min_y, max_y)
		food_x = random.randint(min_x, max_x)
		food_yx = (food_y, food_x)
		if food_yx not in snake:
			screen.addch(food_y, food_x, curses.ACS_DIAMOND, cp)
			screen.refresh()
			time_spawn_food = time.time()
			return food_yx, time_spawn_food


def move(
		screen, 
		snake: list[tuple[int, int]], 
		move_to: str, 
		food_yx: tuple[int, int], 
		border_values: dict,
		score: int=0 
		) -> dict:
	res = {}
	head_y, head_x = snake[-1]
	old_tail_y, old_tail_x = snake[0]
	cp = curses.color_pair(1)
	match move_to:
		case 'up':
			new_head = (head_y - 1, head_x)
		case 'down':
			new_head = (head_y + 1, head_x)
		case 'left':
			new_head = (head_y, head_x - 1)
		case 'right':
			new_head = (head_y, head_x + 1)

	if is_game_over(new_head, snake, border_values):
		graphic_game_over(screen, score)
		res['is_game'] = False
		return res
	res['is_game'] = True
	
	snake.append(new_head)
	screen.addch(new_head[0], new_head[1], curses.ACS_BLOCK, cp)

	if new_head != food_yx:
		snake.pop(0)
		screen.addch(old_tail_y, old_tail_x, ' ')
	else:
		score += 1
		graphic_scorer(screen, score)

	screen.refresh()
	res['score'] = score
	res['snake'] = snake
	return res


def graphic_game_over(screen, score: int):
	screen.clear()
	screen.addstr("Game Over.\n", curses.color_pair(1))
	screen.addstr(str(score), curses.color_pair(1))
	screen.refresh()
	time.sleep(3)
	screen.timeout(-1)
	screen.getch()

def is_game_over(
		new_head: tuple[int, int], 
		snake: list[tuple[int, int]], 
		border_values: dict
		) -> bool:
	y, x = new_head

	u = border_values['up']
	d = border_values['down']
	r = border_values['right']
	l = border_values['left']

	return (
		new_head in snake or 
		y in (u, d) or
		x in (l, r)
		)


def food_del(screen, food_yx: tuple[int, int]):
	food_y, food_x = food_yx
	screen.addch(food_y, food_x, ' ')
	screen.refresh()


def food_time(time_spawn_food: int):
	current_time = time.time()
	if current_time - time_spawn_food > 15:
		return True
	return False


def graphic_border(screen):
	cp = curses.color_pair(1)
	border_values = {
	'up': 4,
	'down': curses.LINES - 2,
	'right': curses.COLS - 2,
	'left': 2
	}

	u, d, r, l = border_values['up'], border_values['down'], border_values['right'], border_values['left']
	text_line = 2
	text_col = 3

	screen.addstr(text_line, text_col, 'Console-Snake. Developed by W1nsh.', cp)
	graphic_scorer(screen)

	screen.addch(u, l, curses.ACS_ULCORNER, cp)
	screen.addch(u, r, curses.ACS_URCORNER, cp)
	screen.addch(d, l, curses.ACS_LLCORNER, cp)
	screen.addch(d, r, curses.ACS_LRCORNER, cp)

	for i in range(l + 1, r):
		screen.addch(u, i, curses.ACS_HLINE, cp)
		screen.addch(d, i, curses.ACS_HLINE, cp)

	for i in range(u + 1, d):
		screen.addch(i, l, curses.ACS_VLINE, cp)
		screen.addch(i, r, curses.ACS_VLINE, cp)

	screen.refresh()
	return border_values



def graphic_scorer(screen, score: int=0):
	cp = curses.color_pair(1)
	text_line = 2
	start_text_col = 47
	screen.addstr(text_line, start_text_col, f'Score: {score}', cp)
	screen.refresh()


def configer_color_theme():
	colors_for_themes = {
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
	border_values = graphic_border(screen)
	is_game = True
	snake = spawn_snake(screen, border_values)
	generated_first_food = False
	time_spawn_food = 0
	move_to = 'right'
	while is_game:
		move_to = change_move_to(screen, move_to)
		if food_time(time_spawn_food):
			if generated_first_food:
				food_del(screen, food_yx)
			else:
				generated_first_food = True
			food_yx, time_spawn_food = generate_food(screen, snake, border_values)
		game_progress = move(screen, snake, move_to, food_yx, border_values)
		is_game = game_progress['is_game']
		snake = game_progress.get('snake', snake)
		score = game_progress.get('score', 0)


def main(screen):
	configer_color_theme()
	curses.update_lines_cols()
	curses.curs_set(0)
	game(screen)
	

if __name__ == '__main__':
	curses.wrapper(main)