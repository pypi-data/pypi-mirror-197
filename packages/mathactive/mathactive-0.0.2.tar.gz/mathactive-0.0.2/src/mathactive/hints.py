import random


def generate_hint(start, stop, step, answer, difficulty):
    hints = [f"What number is greater than {stop} and less than {stop + 2 * step}?"]
    hint = random.choice(hints)

    output = {
        "text": hint,
        "difficulty": difficulty,
        "question_numbers": [start, stop, step, answer],
    }
    return output
