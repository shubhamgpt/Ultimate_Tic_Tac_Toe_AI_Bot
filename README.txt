Ultimate_Tic_Tac_Toe_GameAI
==========================

Details:
--------
1) game.py
	- main class
	- manages board data
	- take and control human input

2) randomai.py
	- controller for random legitimate moves

3) minmaxai.py
	- controller for alpha-beta pruning based ai

-------------------------------------------------------

Execute:
--------
python game.py <game_mode>
<game_mode> is	1 => Random player vs. Random player
		2 => Human vs. Random Player
		3 => Human vs. Human

-------------------------------------------------------

Sample Input:
------------


R\C	0 1 2 3 4 5 6 7 8
0	_ _ _ _ _ _ _ _ _
1	_ _ _ _ _ _ _ _ _
2	_ _ _ _ _ _ _ _ _
3	_ _ _ _ _ _ _ _ _
4	_ _ _ _ _ _ _ _ _
5	_ _ _ _ _ _ _ _ _
6	_ _ _ _ _ _ _ _ _
7	_ _ _ _ _ _ _ _ _
8	_ _ _ _ _ _ _ _ _

Enter your move: (row column) (you're playing with X): 4 4

R\C	0 1 2 3 4 5 6 7 8
0	_ _ _ _ _ _ _ _ _
1	_ _ _ _ _ _ _ _ _
2	_ _ _ _ _ _ _ _ _
3	_ _ _ _ _ _ _ _ _
4	_ _ _ _ X _ _ _ _
5	_ _ _ _ _ _ _ _ _
6	_ _ _ _ _ _ _ _ _
7	_ _ _ _ _ _ _ _ _
8	_ _ _ _ _ _ _ _ _



