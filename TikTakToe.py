import os
import random

# ############# 

 # Логика ходов компьютера. Выстраивает свою комбинацию из пяти меток, если игрок скоро выиграет, то перекрывает ему некоторые позиции. 

def next_to_mark(cells : list, mark : str, count_next_to_marks : int) -> int:
	"""Нахождение позиции, в которой рядом находятся метки"""
	prev_move = 0
	count_marks = 0
	aviable_moves = []

	if cells:
		for ind, item in enumerate(cells):
			
			try:
				if cells[ind + 1] == mark and not item in ("X", "O"):
					aviable_moves.append(item)
			except Exception:
				break

	cells = list(reversed(cells))
	print(cells)
	if cells:
		for ind, item in enumerate(cells):
			try:
				print(ind, cells[ind])
				if cells[ind + 1]	 == mark and not item in ("X", "O"):
					aviable_moves.append(item)
					
			except Exception:
				break
	
	return aviable_moves


def create_list_moves(mark : str, user_mark: str, collections : list):
	"""Создание и списка возможных позиций для компьютера"""
	count_user_mark = 0
	count_comp_mark = 0
	aviable_moves = []

	for ind in collections:
		if ind == user_mark:
			count_user_mark += 1
			count_comp_mark = 0

		elif ind == mark:
			count_comp_mark += 1
			count_user_mark = 0

		if count_user_mark == 3:
			aviable_moves += next_to_mark(collections, user_mark, 3)
			break

		if count_comp_mark in (1,2,3,4):
			aviable_moves += next_to_mark(collections, mark, 4)
			break
		
	return aviable_moves


def priority_move(game_area : list, count_cell : int, mark : str, user_position : int, user_mark: str, last_comp_position):
	"""Создание списка возможных позиций для компьютера. 
	position_row - строка, в которой находится позиция игрока или компьютера
	position_col - столбец, в котором находится позиция игрока или компьютера 
	"""
	position_row = user_position // count_cell
	position_col = user_position % count_cell
	aviable_moves = []

	row = [game_area[position_row * count_cell + x] for x in range(count_cell)]

	col = [game_area[x * count_cell + position_col] for x in range(count_cell)]

	aviable_moves += create_list_moves(mark, user_mark,  row)
	aviable_moves += create_list_moves(mark, user_mark,  col)


	if aviable_moves:
		return list(set(aviable_moves))

	position_row = last_comp_position // count_cell
	position_col = last_comp_position % count_cell

	row = [game_area[position_row * count_cell + x] for x in range(count_cell)]

	col = [game_area[x * count_cell + position_col] for x in range(count_cell)]
	

	aviable_moves += create_list_moves(mark, user_mark,  row)
	aviable_moves += create_list_moves(mark, user_mark,  col)


	return list(set(aviable_moves))


def computer_move(game_area : list, count_cell : int, mark : str, user_mark: str, user_position : int, last_comp_position : int) -> None:
	"""Ход компьютера"""
	priority_moves = []
	aviable_moves = []
	for i in game_area:
		if i in ("X", "O"):
			continue
		aviable_moves.append(i)

	priority_moves = priority_move(game_area, count_cell, mark, user_position, user_mark, last_comp_position)

	if (last_comp_position == -1 and not priority_moves) : 
		move = random.choice(aviable_moves)
		set_mark_position(mark, game_area, move)
		return move
	else:
		move = priority_moves.pop()
		while not set_mark_position(mark, game_area, move) and priority_moves:
			move = priority_moves.pop()
			move = min(priority_moves)
		return move


###########################################################################################################################################  



def print_menu() -> str:
	"""Вывод на экран режимов игры. Возвращает значение, которое выбрал пользователь."""
	return input("Введите номер режима игры:\n"\
				 "1. Играть против компьютера\n"\
				 "2. Играть против человека\n"\
				 "3. Выход\n")


def create_game_area(count_cell : int) -> list:
	"""Создание игрового поля. Возвращает массив со значениям в поле"""
	return [numb for numb in range(count_cell * count_cell)]


def output_game_area(game_area : int, count_cell : int) -> None:
	"""Вывод игрового поля на экран. Ничего не возвращает"""
	print('\n'*5)
	for i in range(count_cell):
		row = '| '
		for j in range(count_cell):
			row += f'{game_area[i * count_cell + j]:>3} | '
		print(row)
		print('--' * (len(row) // 2))


def set_mark_position(user_mark : str, game_area : int, position : int) -> bool:
	"""Установка маркера игрока в соответствующую позицию. Иначе вернет False"""
	if game_area[position] in ('X', 'O'):
		return False

	game_area[position] = user_mark 
	return True


def win_check(game_area : list, mark : str, count_cell : int, position : int) -> bool:
	"""Проверка победителя. Возвращает:
		False - Если игра продолжается,
		True - Если кто-то выиграл,
	"""

	numb_row = position // count_cell
	numb_col = position % count_cell


	def five_mark_check(temp : str, mark : int) -> bool:
		"""Проверяет, есть ли рядом пять маркеров"""
		if temp.find(mark * 5) > -1:
			return True
		return False

	def horizontal_check() -> bool:
		"""Проверка маркеров на горизонтали"""
		row = [game_area[numb_row * count_cell + x] for x in range(count_cell)]
		row = list(map(str, row))
		
		return five_mark_check(''.join(row), mark)
		

	def vertical_check() -> bool:
		"""Проверка маркеров на вертикали"""
		col = [game_area[x * count_cell + numb_col] for x in range(count_cell)]
		col = list(map(str, col))
		# print(col)
		return five_mark_check(''.join(col), mark)

	def Is_Main_Diagonal(ind) -> bool:

		ind_row = ind // count_cell
		ind_col = ind % count_cell
		return ((ind_row - ind_col) ** 2 == (numb_row - numb_col) ** 2)

	def Is_Sec_Diagonal(ind) -> bool:
		ind_row = ind // count_cell
		ind_col = ind % count_cell
		return ((ind_row + ind_col)  == (numb_row + numb_col))

	def create_diagonal(key1 : int, key2 : int, right_to_left : bool) -> list:
		ind_start = (numb_row + key1) * count_cell + (numb_col + key2)

		diagonal = []

		ind = position
		ind_row = ind // count_cell
		ind_col = ind % count_cell
		
		if Is_Main_Diagonal(ind_start) or Is_Sec_Diagonal(ind_start):
			if (ind_start > 0) and (ind_start < count_cell * count_cell):
				while True:

					ind = (ind_row + key1) * count_cell + (ind_col + key2) 
					ind_row = ind // count_cell
					ind_col = ind % count_cell

					

					ind_next = (ind_row + key1) * count_cell + (ind_col + key2)
					ind_row_next = ind_next // count_cell
					ind_col_next = ind_next % count_cell

					

					if  (ind_next < 0) or (ind_next > count_cell * count_cell):
						break

					if right_to_left and not Is_Main_Diagonal(ind_next):
						break
					elif not right_to_left and not Is_Sec_Diagonal(ind_next):
						break

		ind_row_tmp = ind // count_cell
		ind_col_tmp = ind % count_cell

		i = 0
		while i < count_cell:
			try:
				if key2 > 0:
					ind = (i + ind_row) * count_cell + (-i + ind_col) 
				else:
					ind = (i + ind_row) * count_cell + (i + ind_col) 

				if right_to_left and not Is_Main_Diagonal(ind):
					break
				elif not right_to_left and not Is_Sec_Diagonal(ind):
					break

				
				diagonal.append(game_area[ind])
				i += 1
			except IndexError:
				return diagonal

		return diagonal	
			


	def diagonal_check() -> bool:
		"""Проверка маркеров по диагоналям"""
		diagonal = create_diagonal(-1, -1, True)
		diagonal = list(map(str, diagonal))
		if five_mark_check(''.join(diagonal), mark): return True
		

		diagonal = create_diagonal(-1, 1, False)
		diagonal = list(map(str, diagonal))
		if five_mark_check(''.join(diagonal),  mark): return True
		return False

	return (horizontal_check() or 
		    vertical_check() or
		    diagonal_check()
		   )


def full_check(game_area : list) -> bool:
	"""Проверка на ничью"""
	if game_area.count('X') == game_area.count('O'):
		return True
	return False


def first_move() -> int:
	"""Выбор того, кто ходит первым. Компьютер является всегда вторым игроком"""
	return random.choice([0, 1])


def check_user_position(user_positon : int, count_cell, user_mark, game_area) -> bool:
	if (user_positon < 0) or ((count_cell ** 2) < user_positon):
		print('С таким номером ячеек нет!')
		return False

	if not set_mark_position(user_mark, game_area, user_positon):
		print("Это место уже занято!")
		return False

	return True


def game_two_players(game_area, count_cell):
	marks = ['X', 'O']
	first_player = input("Выберите чем будете играть: X или O: ").strip().upper()
	marks.remove(first_player)
	second_player = marks[0]

	players = [first_player, second_player]
	first = first_move()
	print(first)
	COUNT_MOVE = 0 + first
	
	print(f"Первым ходит {players[first]}!\n")

	while True:
		output_game_area(game_area, count_cell)
		user_mark = players[COUNT_MOVE % 2]

		if COUNT_MOVE % 2 != 0:
			# Ход первого игрока игрока

			user_positon = int(input(f"Введите номер позиции цифрами, на которую хотите поставить {user_mark}: "))

			if not check_user_position(user_positon, count_cell, user_mark, game_area):
				continue

			output_game_area(game_area, count_cell)

			if win_check(game_area, user_mark, count_cell, user_positon):
				print("Выиграл второй {user_mark}!!!!")
				break
		else:
			# Ход втогоро игрока 
			user_positon = int(input(f"Введите номер позиции цифрами, на которую хотите поставить {players[COUNT_MOVE % 2]}: "))

			if not check_user_position(user_positon, count_cell, user_mark, game_area):
				continue

			output_game_area(game_area, count_cell)

			if win_check(game_area, user_mark, count_cell, user_positon):
				print("Выиграл второй {user_mark}!!!!")
				break

		COUNT_MOVE += 1


def game_with_computer(game_area, count_cell) -> None:
	"""Запуск игры против компьютера"""
	marks = ['X', 'O']
	
	COUNT_MOVE = 0
	USER_MARK = input("Выберите чем будете играть: X или O: ").strip().upper()
	marks.remove(USER_MARK)
	COMP_MARK = marks[0]
	last_comp_positon = -1

	while True:
		output_game_area(game_area, count_cell)
		# Ход игрока
		user_positon = int(input(f"Введите номер позиции цифрами, на которую хотите поставить {USER_MARK}: "))

		if not check_user_position(user_positon, count_cell, USER_MARK, game_area):
			continue

		output_game_area(game_area, count_cell)

		if win_check(game_area, USER_MARK, count_cell, user_positon):
			print("Победа")
			break


		# Ход компьютера 
			
		position_comp = computer_move(game_area, count_cell, COMP_MARK, USER_MARK, user_positon, last_comp_positon)
		last_comp_positon = position_comp


		if win_check(game_area, COMP_MARK, count_cell, position_comp):
			print("Проиграл. ПК WIN!!!!")
			break

		COUNT_MOVE += 1


def main():
	COUNT_CELL = 10 #int(input("Введите количество размер поля, X*X (Одно число): "))

	user_input = print_menu()
	if user_input == '1':
		game_area = create_game_area(COUNT_CELL)
		game_with_computer(game_area, COUNT_CELL)
	elif user_input == '2':
		game_area = create_game_area(COUNT_CELL)
		game_two_players(game_area, COUNT_CELL)
	else:
		print('До скорого!')
		exit()


if __name__ == "__main__":
	main()