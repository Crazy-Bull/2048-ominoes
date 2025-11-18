# 2048-ominoes

**2048-ominoes** is a project that evaluates all 8-omino playboards. It aims at exploring the possiblity of non-traditional playboards and giving statistical support to the development of 2048 formations.

---
## About polynominoes

A polynomino is a shape formed by 1*1 squares, starting with a single square, and each time adding another square adjacent to an existing one (For example, a domino is the only polynomino of size 2). This ensures connectivity 
and makes any polynomio possible to become a playboard in 2048.

There are **369** distinct 8-ominoes in total (reflecting and rotating is considered the same one).

---
## Criteria

This project introduces 5 criteria to evaluate each of the 369 chessboards.

- **128/256/512 rate:** The possibility to craft an 128/256/512 on this board.
- **E[score]:** The expected value of your score when the game ends.
- **E[sum]:** The expected value of the sum of all numbers on the board when the game ends.

By default, each criteria is measured under 4sr(4 spawn rate)=0.1, and assume that the best strategy is taken on each step. Note that the best strategy may not be the same for each criteria.

---
## Usage

The project contains a **summary.xlsx** file that contains all data for all 369 cases. You can check and compare the stats for each playboard.

Other files are source codes and intermediate data. If you are not a developer, they can be ignored.

---
## Developer tutorial

Todo

---
## Leaderboard
