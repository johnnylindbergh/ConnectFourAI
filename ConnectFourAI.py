class Board:
	def __init__(self, rows, cols):
		self.rows = rows
		self.cols = cols
		self.state = [[0 for i in xrange(cols)] for i in xrange(rows)]

	def display(self):
		print"-----------------------------"
		for i in range(6):
			for j in range(7):
				print "|", self.state[i][j],
			print "|"
		print"-----------------------------"
		print "  0   1   2   3   4   5   6"
	def makeMove(self, column, piece):
		if self.state[0][column] != 0:
			return False

		else:
			for i in range(self.rows):

				if self.state[i][column] != 0:
					self.state[i-1][column] = piece
					return True
				if i == 5:
					self.state[5][column] = piece
					return True


	def getPossibleMoves(self):
		listofPossibleMoves = []
		for i in range(7):

			if self.state[0][i] == 0:
				listofPossibleMoves.append(i)

		return listofPossibleMoves


	def isGameOver(self):
		for i in range(6):
			for j in range(7):
				if self.state[i][j] == 1 or self.state[i][j] == 2:

					if i < self.rows - 3:
						for r in range(4):
							 if self.state[i+r][j] == self.state[i][j]:
								if r == 3:
							 		return self.state[i][j], ' connected 4 vertically'
							 else:
							 	break

					if j < self.cols - 3:
						for u in range(4):
								if self.state[i][j+u] == self.state[i][j]:
									if u ==3:
										return self.state[i][j], ' alligned 4 pieces'
								else:
									break

					if i < self.rows - 3 and j < self.cols - 3:
						for d in range(4):
								if self.state[i+d][j+d] == self.state[i][j]:
									if d == 3:
										return self.state[i][j], ' alligned 4 diagonal pieces'
								else:
									break

					if i < self.rows + 3 and j < self.cols - 3:
						for d in range(4):
								if self.state[i-d][j+d] == self.state[i][j]:
									if d == 3:
										return self.state[i][j], ' won this game with 4 diagonal pieces'
								else:
									break


		return 0

class HumanPlayer:
	def __init__(self, number):
		self.number = number

	def getNextMove(self, board):
		print "Current Board:"
		board.display()



		while True:
				try:
					player_next_move = int(raw_input("Column:  "))
					break
				except ValueError:
					print "thats not 0-6. Try again"

		while not player_next_move in board.getPossibleMoves():
			while True:
				try:
					player_next_move = int(raw_input("Column:  "))
					break
				except ValueError:
					print "thats not 0-6. Try again"
		return player_next_move

import random
import Queue
import copy

class AIPlayer:
	def __init__(self, number, piece):
		self.number = number
		self.piece = piece

	def getNextMove(self, board):

		move_queue = Queue.PriorityQueue()
		for i in board.getPossibleMoves():
			board_copy = copy.deepcopy(board)
			board_copy.makeMove(i, self.number)
			#depth is specified here
			move_value = self.minimax(board_copy, 2, self.piece, True)
			move_queue.put((-1 * move_value, i))

		return move_queue.get()[1]

	def getScoreofList(self, list_of_4_positions):

			score_of_list = 0
			count_of_AI	= list_of_4_positions.count(self.number)
			count_of_player = list_of_4_positions.count(self.piece)
			count_of_0 = list_of_4_positions.count(0)

			if not 0 in list_of_4_positions:
				if count_of_AI == 4:
					return score_of_list + 10000
				if count_of_AI == 3:
					return score_of_list + 0
				if count_of_AI == 2:
					return score_of_list + 0
				if count_of_AI == 1:
					return score_of_list + 0
				if count_of_player == 4:
					return score_of_list - 5000000

			if 0 in list_of_4_positions and self.number in list_of_4_positions:

				if count_of_AI == 3:
					return score_of_list + 200

				if count_of_AI == 2:
					return score_of_list + 50

				if count_of_AI == 1:
					return score_of_list + 1

			if 0 in list_of_4_positions and self.piece in list_of_4_positions:

				if count_of_player == 3:
					return score_of_list - 200

				if count_of_player == 2:
					return score_of_list - 50

				if count_of_player == 1:
					return score_of_list - 1

			if 0 in list_of_4_positions and self.piece in list_of_4_positions and self.number in list_of_4_positions:
				if count_of_AI == 2:
					return score_of_list + 30

				if count_of_player == 2:
					return score_of_list - 30

				if count_of_0 == 2:
					return score_of_list + 0
			else:
				return score_of_list

	def getBoardScore(self, board):

		collective_board_score = 0
		list_of_4_positions = [0, 0, 0, 0]

		for i in range(board.rows):
			for j in range(board.cols):
				if j < board.cols - 3:
					for a in range(0,4):
						list_of_4_positions[a] = board.state[i][j+a]
					collective_board_score = collective_board_score + self.getScoreofList(list_of_4_positions)
				if i < board.rows -3:
					for a in range(0,4):
						list_of_4_positions[a] = board.state[i+a][j]
					collective_board_score = collective_board_score + self.getScoreofList(list_of_4_positions)
				if i < board.rows - 3 and j < board.cols -3:
					for a in range(0,4):
						list_of_4_positions[a] = board.state[i-a][j+a]
					collective_board_score = collective_board_score + self.getScoreofList(list_of_4_positions)
					for a in range(0,4):
						list_of_4_positions[a] = board.state[i+a][j+a]
					collective_board_score = collective_board_score + self.getScoreofList(list_of_4_positions)

		return collective_board_score



	def minimax(self, board, depth, piece, mini):
		if board.isGameOver() == 1 or board.isGameOver() == 2 or depth == 0:
			if board.isGameOver() > 0:
				print self.getBoardScore(board), "when", board.isGameOver(), "wins"
				board.display()
			return self.getBoardScore(board)
		else:
			list_of_boards = []
			list_of_scores = []

			for i in board.getPossibleMoves():
				Board_copy = copy.deepcopy(board)

				if mini:
					list_of_boards.append(Board_copy.makeMove(i, self.piece))
				else:
					list_of_boards.append(Board_copy.makeMove(i, self.number))

				scoreofscores = self.minimax(Board_copy, depth - 1, piece, not mini)
				list_of_scores.append(scoreofscores)

			if mini == True:
				return min(list_of_scores)

			if mini == False:
				return max(list_of_scores)





def main():


	board = Board(6, 7)
	p1 = HumanPlayer(1)
	p2 = AIPlayer(2, 1)



	while board.isGameOver() == 0:
		if len(board.getPossibleMoves()) == 0:
			print "tie"
		player_1s_move = p1.getNextMove(board)
		board.makeMove(player_1s_move, 1)

		if board.isGameOver() != 0:
			break
		if len(board.getPossibleMoves()) == 0:
			print "tie"
			break
		player_2s_move = p2.getNextMove(board)
		board.makeMove(player_2s_move, 2)
		print "AI chose", player_2s_move
		board.display()
		if len(board.getPossibleMoves()) == 0:
			print "tie"
			break
	print board.isGameOver()

print "Welcome to Connect Four!"
main()
print "Thanks for playing "
