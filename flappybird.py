#!/usr/bin/env python3
"""Flappy: fly through the gaps in the pipes.
Controls: Space / Up / W to flap, P to pause, Q to quit."""
import curses, random, time
from pathlib import Path

W, H = 60, 22                  # play area size
GAP, PIPE_W, SPACING = 7, 3, 20  # gap height, pipe width, distance between pipes
GRAVITY, FLAP, SPEED = 0.15, -0.9, 0.5
