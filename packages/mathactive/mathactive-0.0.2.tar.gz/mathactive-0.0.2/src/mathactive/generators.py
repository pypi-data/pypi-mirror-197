import random
from typing import Literal
from .questions import generate_question_data
from .utils import get_next_skill_score, generate_start_stop_step


def start_interactive_math(
    skill_score=0.01,
    do_increase_skill_score: Literal["increase", "decrease", "leave"] = "leave",
):
    next_skill_score = get_next_skill_score(skill_score, do_increase_skill_score)
    start, generated_stop, step = generate_start_stop_step(skill_score)
    for value in range(start, generated_stop + 1, step):
        if value <= generated_stop:
            stop = value
        else:
            break
    question_data = generate_question_data(
        start, stop, step, question_num=random.randint(0, 4)
    )

    question = question_data["question"]
    start = question_data["start"]
    stop = question_data["stop"]
    step = question_data["step"]
    answer = question_data["answer"]

    output = {
        "text": question,
        "skill_score": next_skill_score,
        "question_numbers": [start, stop, step, answer],
    }
    return output
