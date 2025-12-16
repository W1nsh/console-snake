import time
import random
import json

import curses


# graphic
def snake_move_animation(screen: curses.window, snake: list[tuple[int, int]], tail: tuple[int, int]) -> None:
	cp = curses.color_pair(1)
	for y, x in snake:
		screen.addch(y, x, curses.ACS_BLOCK, cp)
	if tail is not None:
		screen.addch(*tail, ' ')


def game_over_graphic(screen: curses.window, score: int, game_over_yx: tuple[int, int], project_name_yx: tuple[int, int]) -> None:
	cp = curses.color_pair(1)
	y, x = game_over_yx
	screen.clear()
	draw_project_name(screen, project_name_yx)
	game_over_text = 'Game over.'
	score_text = f'Score: {score}.'
	screen.addstr(y, x, game_over_text, cp)
	screen.addstr(y + 2, x, score_text, cp)


def border_graphic(screen: curses.window, border_values: dict[str, int]):
	cp = curses.color_pair(1)
	u = border_values['up']
	d = border_values['down']
	r = border_values['right']
	l = border_values['left']

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


def draw_project_name(screen: curses.window, project_name_yx: tuple[int, int]) -> None:
	y, x = project_name_yx
	cp = curses.color_pair(1)
	project_name_text = 'Console-Snake. Developed by W1nsh.'
	screen.addstr(y, x, project_name_text, cp)


def draw_score(screen: curses.window, score: int, score_yx: tuple[int, int]) -> None:
	y, x = score_yx
	cp = curses.color_pair(1)
	score_text = f'Score: {score}'
	screen.addstr(y, x, score_text, cp)


def draw_and_del_food(screen: curses.window, foods: list[tuple[int, int]]):
	cp = curses.color_pair(1)
	food_y, food_x = foods[-1]
	if len(foods) == 2:
		past_food_y, past_food_x = foods[0]
		screen.addch(past_food_y, past_food_x, ' ')
	screen.addch(food_y, food_x, curses.ACS_DIAMOND, cp)



# logic
def game_over(screen: curses.window):
	time.sleep(3)
	screen.timeout(-1)
	screen.getch()
	return False


def snake_is_die(snake: list[tuple[int, int]], border_values: dict[str, int]) -> bool:
	return (
		snake[-1] in snake[:-1] or
		snake[-1][0] <= border_values['up'] or
		snake[-1][0] >= border_values['down'] or
		snake[-1][1] <= border_values['left'] or
		snake[-1][1] >= border_values['right']
	)


def move(snake: list[tuple[int, int]], direction: str) -> list[tuple[int, int]]:
	head_y, head_x = snake[-1]
	cords = {
		'up': (head_y - 1, head_x),
		'down': (head_y + 1, head_x),
		'left': (head_y, head_x - 1),
		'right': (head_y, head_x + 1)
	}
	snake.append(cords[direction])
	return snake


def change_direction(ascii_code: int, direction: str):
	values_ascii_codes = {
		258: 'down',
		259: 'up',
		260: 'left',
		261: 'right'
	}
	opposites = {
		'up': 'down',
		'down': 'up',
		'left': 'right',
		'right': 'left'
	}
	new_direction = values_ascii_codes.get(ascii_code, None)
	opposite_new_direction = opposites.get(new_direction, None)
	if opposite_new_direction == direction or opposite_new_direction is None:
		return direction
	return new_direction


def input_reader(screen: curses.window, tick: int) -> int:
	screen.timeout(tick)
	ascii_code = screen.getch()
	return	ascii_code


def scorer(score: int, snake: list[tuple[int, int]], foods: list[tuple[int, int]]) -> list[tuple[int, int]] | int:
	tail = None
	if foods[-1] == snake[-1]:
		score += 1
	else:
		tail = snake.pop(0)
	return snake, score, tail

def need_generation_food(time_food_generation: int, food_life_time: int):
	return time.time() - time_food_generation > food_life_time


def create_snake(start_snake_yx: tuple[int, int], snake_length: int):
	y, x = start_snake_yx
	snake = []
	for i in range(x, x + snake_length):
		el = (y, i)
		snake.append(el)
	return snake



def food_generator(snake: tuple[int, int], border_values: dict[str, int], foods: list[tuple[int, int]]):
	food_y = random.randint(border_values['up'] + 1, border_values['down'] - 1)
	food_x = random.randint(border_values['left'] + 1, border_values['right'] - 1)
	food_yx = (food_y, food_x)
	if food_yx in snake:
		return food_generator(snake, border_values, foods)
	time_food_generation = time.time()
	if len(foods) == 2:
		foods.pop(0)
	foods.append(food_yx)
	return foods, time_food_generation


def border(border_distance: dict[str, int], screen_size: tuple[int, int]):
	return {
		'up': border_distance['up'],
		'down': screen_size[0] - border_distance['down'],
		'right': screen_size[1] - border_distance['right'],
		'left': border_distance['left']
	}


def set_colors(main_color: str, background_color: str) -> None:
	colors = {
		'black': curses.COLOR_BLACK,
		'blue': curses.COLOR_BLUE,
		'cyan': curses.COLOR_CYAN,
		'green': curses.COLOR_GREEN,
		'magenta': curses.COLOR_MAGENTA,
		'red': curses.COLOR_RED,
		'white': curses.COLOR_WHITE,
		'yellow': curses.COLOR_YELLOW
	}
	curses.init_pair(
		1, 
		colors.get(main_color),
		colors.get(background_color)
	)


def config_reader() -> int: # will upd
	with open('config.json', 'r') as f:
		config = json.load(f)

		main_color = config['main_color']
		background_color = config['background_color']

		food_life_time = config['time']['food_life_time_sec']
		tick = config['time']['tick_ms']

		border_distance = config['border_distance']

		project_name_yx = (config['text']['project_name']['y'], config['text']['project_name']['x'])
		score_yx = (config['text']['score']['y'], config['text']['score']['x'])
		game_over_yx = (config['text']['game_over']['y'], config['text']['game_over']['x'])

		start_snake_yx = (config['snake']['start_cords']['y'], config['snake']['start_cords']['x'])
		snake_length = config['snake']['length']

	return food_life_time, tick, border_distance, project_name_yx, score_yx, main_color, background_color, start_snake_yx, snake_length, game_over_yx


def main(screen: curses.window):
	curses.update_lines_cols()
	curses.curs_set(0)
	food_life_time, tick, border_distance, project_name_yx, score_yx, main_color, background_color, start_snake_yx, snake_length, game_over_yx = config_reader()
	set_colors(main_color, background_color)	
	game(screen, food_life_time, tick, border_distance, project_name_yx, score_yx, start_snake_yx, snake_length, game_over_yx)


def game(screen: curses.window, food_life_time: int, tick: int, border_distance: dict[str, int], project_name_yx: tuple[int, int], score_yx: tuple[int, int], start_snake_yx: tuple[int, int], snake_length: int, game_over_yx: tuple[int, int]):
	screen_size = (curses.LINES, curses.COLS)
	is_game = True
	border_values = border(border_distance, screen_size)
	snake = create_snake(start_snake_yx, snake_length)
	score = 0
	time_food_generation = 0
	foods = []
	direction = 'right'
	border_graphic(screen, border_values)
	draw_project_name(screen, project_name_yx)
	
	while is_game:
		draw_score(screen, score, score_yx)
		if need_generation_food(time_food_generation, food_life_time):
			foods, time_food_generation = food_generator(snake, border_values, foods)
			draw_and_del_food(screen, foods)
		ascii_code = input_reader(screen, tick)
		direction = change_direction(ascii_code, direction)
		snake = move(snake, direction)
		snake, score, tail = scorer(score, snake, foods)
		snake_move_animation(screen, snake, tail)
		if snake_is_die(snake, border_values):
			game_over_graphic(screen, score, game_over_yx, project_name_yx)
			screen.refresh()
			is_game = game_over(screen)

		screen.refresh()


if __name__ == '__main__':
	curses.wrapper(main)
