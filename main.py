import curses, time, random

def spawn_snake(screen):
	for i in range(3):
		screen.addch(10, i+1, curses.ACS_BLOCK)
		screen.refresh()
		time.sleep(0.25)
	snake = [(10, 1), (10, 2), (10, 3)]
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
		food_y = random.randint(0, curses.LINES - 1)
		food_x = random.randint(0, curses.COLS - 1)
		food_yx = (food_y, food_x)
		if food_yx not in snake:
			screen.addch(food_y, food_x, curses.ACS_DIAMOND)
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
	if new_head in snake:
		game_over(screen, score)
		res['is_game'] = False
		return res
	snake.append(new_head)
	screen.addch(new_head[0], new_head[1], curses.ACS_BLOCK)
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
	screen.addstr("Game Over.\n")
	screen.addstr(str(score))
	screen.refresh()
	time.sleep(5)
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

def game(screen):
	is_game = True
	snake = spawn_snake(screen)
	generated_first_food = False
	time_spawn_food = 0
	score = 0
	move_to = 'right'
	while is_game:
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
	curses.update_lines_cols()
	curses.curs_set(0)
	game(screen)
	

if __name__ == '__main__':
	curses.wrapper(main)