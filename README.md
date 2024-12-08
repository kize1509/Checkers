# Checkers Game with AI

## Overview

This Checkers game is a Python-based project designed to simulate a classic board game experience with an intelligent AI opponent. The AI leverages advanced techniques like the **Minimax algorithm with Alpha-Beta pruning**, **Zobrist hashing**, and **transposition tables** to optimize its performance.

## Features

- **AI with Depth Configurability**: Customize the depth of the AI's decision tree to balance performance and response time.
- **Heuristic Function**: The AI evaluates the board state using a heuristic that considers multiple parameters, such as:
  - Piece count (normal and king pieces)
  - Positional advantages
  - Potential captures
  - Mobility and board control
  - Promotion line distance
  - Most usable patterns
- **Optimized Search**:
  - **Minimax with Alpha-Beta Pruning**: Reduces the search space for optimal moves.
  - **Zobrist Caching**: Speeds up repeated state evaluations using efficient hashing.
  - **Transposition Tables**: Avoids redundant calculations for identical board states.
- **User-Friendly GUI**: Includes a clean and interactive graphical interface for seamless gameplay.

## Technologies Used

- **Programming Language**: Python
- **GUI Library**: `pygame`
- **Algorithmic Enhancements**: Minimax, Alpha-Beta pruning, variable depth, Zobrist hashing, and transposition tables.

## Screenshots

### Gameplay Interface
![checkers-home](https://github.com/user-attachments/assets/9cb23b5d-3fa6-4f20-8f6b-c8fd3a2f8da5)

![win red](https://github.com/user-attachments/assets/f09774ed-4b27-408f-a9a1-9234e62d648a)


