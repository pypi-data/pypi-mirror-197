import pandas
import random
from scipy.interpolate import interp1d
from typing import Literal
from pathlib import Path

DATA_DIR = Path(__file__).parent.absolute() / 'data'

def get_next_skill_score(
    skill_score,
    do_increase_skill_score: Literal["increase", "decrease", "leave"] = "leave",
):
    if do_increase_skill_score == "leave":
        next_skill_score = skill_score
    elif do_increase_skill_score == "increase":
        if skill_score >= 0.95:
            next_skill_score = round(random.uniform(0.95, 0.99), 2)
        else:
            next_skill_score = round(
                random.uniform(skill_score + 0.01, skill_score + 0.05), 2
            )
    elif do_increase_skill_score == "decrease":
        if skill_score <= 0.05:
            next_skill_score = round(random.uniform(0.01, 0.05), 2)
        else:
            next_skill_score = round(
                random.uniform(skill_score - 0.05, skill_score - 0.01), 2
            )

    return next_skill_score


def generate_start_stop_step(
    skill_score: float, path_to_csv_file: str = "scripts/quiz/data.csv"
):
    """generate start and step values interpolating results to function built from data from file"""
    df = pandas.read_csv(
        path_to_csv_file, delimiter=",", header=0, names=["skill_score", "start"]
    )
    all_rows = df.loc[:]

    difficulties = [row_data["skill_score"] for _, row_data in all_rows.iterrows()]
    starts = [row_data["start"] for _, row_data in all_rows.iterrows()]
    stops = [row_data["stop"] for _, row_data in all_rows.iterrows()]

    interp_start_func = interp1d(difficulties, starts)
    interp_stop_func = interp1d(difficulties, stops)
    generated_start = round(float(interp_start_func(skill_score)))
    generated_stop = round(float(interp_stop_func(skill_score)))
    if skill_score <= 0.3:
        step = 1
    elif skill_score > 0.6:
        step = 10
    else:
        step = 5
    return (generated_start, generated_stop, step)


def convert_sequence_to_string(start, stop, step, sep=", "):
    stop += 1  # increase by 1 to include stop value to sequence
    return sep.join([str(num) for num in range(start, stop, step)]) + sep
