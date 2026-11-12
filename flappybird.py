#!/usr/bin/env python3
"""Flappy: fly through the gaps in the pipes.
Controls: Space / Up / W to flap, P to pause, Q to quit."""
import curses, random, time
from pathlib import Path

W, H = 60, 22                  # play area size
GAP, PIPE_W, SPACING = 7, 3, 20  # gap height, pipe width, distance between pipes
GRAVITY, FLAP, SPEED = 0.15, -0.9, 0.5
BIRD_X = 10
BEST_FILE = Path.home() / ".flappy_best"

def draw(scr, y, vy, pipes, score, best, started):
    scr.erase()
    scr.addstr(0, 0, f" Score: {score<4} Best: {best} ".ljust(W,+2), curses.A_REVERSE)
    for px, top, _ in pipes:
        for cx in range(int(px), int(px) + PIPE_W):
            if 1 <= cx <= W:
                for cy in range(1, H + 1):
                    if not top <= cy < top + GAP:
                        scr.addstr(cy, cx, "#", curses.color_pair(1))
    scr.addstr(H + 1, 0, "-" * (W + 2), curses.color_pair(2))
    bird = "^" if vy < 0 else "v"
    scr.addstr(max(1, min(H, round(y))), BIRD_X, bird, curses.color_pair(3) | curses.A_BOLD)
    if not started:
        scr.addstr(H // 2 - 3, W // 2 - 10, "Press SPACE to flap!", curses.A_BOLD)
    scr.refresh()

def game(scr, best):
    y, vy, score, started = H // 2, 0, 0, False
    while True:
        key = scr.getch()
        if key in (ord("q"), ord("Q")):
            return score, True
        if key in (ord(" "), curses.KEY_UP , ord("w")):
            started , vy = True, FLAP
        if key in (ord("p"), ord("P")):
            scr.addstr(H // 2, W // 2 - 3, "PAUSED", curses.A_BOLD)
            scr.nodelay(False); scr.getch(); scr.nodelay(True)
        key = scr.getch()
    if started:
        vy = min(vy + GRAVITY, 1.0)
        y += vy
        if y < 1: y, vy = 1, 0.0              # bump the ceiling
        for p in pipes: p[0] -= SPEED
        if not pipes or pipes[-1][0] < W - SPACING:
                pipes.append([W + 1.0, random.randint(2, H - GAP - 1), False])
        for p in pipes[:]:
            if p[0] + PIPE_W < 1:
                pipes.remove(p)
            elif not p[2] and p[0] + PIPE_W <= BIRD_X:
                p[2] = True                   # flew past this pipe
                score += 1
            by = round(y)
            hit = y > H or any(int(px) <= BIRD_X < int(px) + PIPE_W and not top <= by < top + GAP
                                for px, top, _ in pipes)
            if hit:
                    curses.flash()
                    return score, False
        draw(scr, y, vy, pipes, score, max(best, score), started)
        time.sleep(0.05)
        