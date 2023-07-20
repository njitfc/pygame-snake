# pygame-snake
simple snake game with pygame realised in less than 4 hours

the snake head is a circle with 2 little circles (eyes), its body is a list of circles.
the board is a 50 * 30 matrix of tiles of 25*25 pixel*pixel.
the game keeps track of the head position on the board.
the body parts positions are appended when the snake head eats a point, pushing its actual position onto the stack, the body parts position updates each turn, it removes the last inserted (the tail) and appends the head position.
the game runs in 60 fps, the snake moves twice per second.
red points randomly spawn at free space on board, the snake grows when it consumes it, forcing an other point to spawn.
game keeps track of the current score ,it is shown on the top left of the screen, when the game is over, a screen with 2 buttons and the previous game score shows up, allowing the user to either start a new game or exit.
