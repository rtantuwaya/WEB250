# lesson4.py

from flask import render_template, request, redirect, url_for
import random

# Function to generate a random number
def get_random_number(max_value):
    return random.randint(0, max_value)

# Function to handle the game logic and generate math problems
def start_game(value, expressions):
    game_data = []

    for _ in range(expressions):
        second_operand = get_random_number(value)
        sum_value = value + second_operand
        game_data.append({
            "expression": f"{value} + {second_operand} = ?",
            "correct_answer": sum_value
        })

    return game_data

# Function to check the user's answer
def check_answer(user_answer, correct_answer):
    if user_answer == correct_answer:
        return "Correct!"
    else:
        return f"Incorrect. The correct answer was {correct_answer}."
