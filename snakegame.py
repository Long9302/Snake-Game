import curses
import random

def main(stdscr):
    # Setup
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)
    w.timeout(100)

    # Initial snake + food
    snk_x = sw // 4
    snk_y = sh // 2
    snake = [
        [snk_y, snk_x],
        [snk_y, snk_x - 1],
        [snk_y, snk_x - 2]
    ]

    food = [sh // 2, sw // 2]
    w.addch(food[0], food[1], curses.ACS_PI)

    key = curses.KEY_RIGHT
    score = 0

    while True:
        next_key = w.getch()
        key = key if next_key == -1 else next_key

        # Calculate new head
        y = snake[0][0]
        x = snake[0][1]

        if key == curses.KEY_DOWN:
            y += 1
        elif key == curses.KEY_UP:
            y -= 1
        elif key == curses.KEY_LEFT:
            x -= 1
        elif key == curses.KEY_RIGHT:
            x += 1

        new_head = [y, x]

        # Collision detection
        if (
            y in [0, sh] or
            x in [0, sw] or
            new_head in snake
        ):
            msg = f"Game Over! Score: {score}"
            w.addstr(sh//2, sw//2 - len(msg)//2, msg)
            w.nodelay(0)
            w.getch()
            break

        snake.insert(0, new_head)

        # Food eaten
        if snake[0] == food:
            score += 1
            food = None
            while food is None:
                nf = [
                    random.randint(1, sh - 2),
                    random.randint(1, sw - 2)
                ]
                food = nf if nf not in snake else None
            w.addch(food[0], food[1], curses.ACS_PI)
        else:
            tail = snake.pop()
            w.addch(tail[0], tail[1], ' ')

        # Draw snake
        w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

        # Display score
        w.addstr(0, 2, f"Score: {score}")

if __name__ == "__main__":
    curses.wrapper(main)