import curses, time, random

def spawn_snake(screen):
	for i in range(3):
		screen.addch(3, i+1, curses.ACS_BLOCK)
		screen.refresh()
		time.sleep(0.25)
	snake = [(3, 1), (3, 2), (3, 3)]
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
	snake.append(new_head)
	if new_head != food_yx:
		snake.pop(0)
		screen.addch(old_tail_y, old_tail_x, ' ')
	else:
		score += 1
	screen.addch(new_head[0], new_head[1], curses.ACS_BLOCK)
	screen.refresh()
	return snake
	
			
def food_time(time_spawn_food):
	current_time = time.time()
	if current_time - time_spawn_food > 15:
		return True
	return False

def main(screen):
	curses.update_lines_cols()
	time_spawn_food = 0
	score = 0
	snake = spawn_snake(screen)
	move_to = 'right'
	while True:
		move_to = change_move_to(screen, move_to)
		if food_time(time_spawn_food):
			food_yx, time_spawn_food = generate_food(screen, snake) # передать сюда змейку
		snake = move(screen, snake, move_to, food_yx, score) # передать сюда змейку и направление

if __name__ == '__main__':
	curses.wrapper(main)