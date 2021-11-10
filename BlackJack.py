import random 

deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11] * 4
random.shuffle(deck)
player_count = 0

while True:
	choice = input('Будете барать карту?: д/н\n')
	if choice == 'д':
		current = deck.pop()
		print(f'Вам попалась карта с достоинством {currnt}!\n')
		player_count += current()
		if player_count == 21:
			print('Вы выиграли!')
			break
		elif player_count > 21:
			print('Вы выиграли')
			break
		else:
			print(f'Вы еще в игре! У вас {player_count} очков.')
	else:
		print(f'Вы закончили игру. У вас {player_count} очков!')
		break
	