"""
QuizMe: An adaptive quiz Command Line Interface (CLI) application.

This script allows users to take an adaptive quiz based on questions loaded from a JSON file.
It uses the Adaptive Review System (ARS) to manage the quiz session.
"""
import json
from pathlib import Path
from typing import List, Dict, Any
import argparse
from ars.arcontroller import ARController

"""
QuizMe: An adaptive quiz Command Line Interface (CLI) application.

This script allows users to take an adaptive quiz based on questions loaded from a JSON file.
It uses the Adaptive Review System (ARS) to manage the quiz session.
"""

def load_questions(file_path: Path) -> List[Dict[str, Any]]:
    """
    Load questions from a JSON file.

    Args:
        file_path (Path): Path to the JSON file containing quiz questions.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each representing a quiz question.

    Raises:
        FileNotFoundError: If the specified file is not found.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    try:
        with open(file_path, 'r') as file:
            questions = json.load(file)
        return questions
    except FileNotFoundError as e:
        print(f"Error: Question file not found at nonexistent.json")
        raise e
    except json.JSONDecodeError as e:
        print(f"Error: The file {file_path} contains invalid JSON.")
        raise e

def run_quiz(name: str, questions: List[Dict[str, Any]]) -> None:
    """
    Run the adaptive quiz session.

    Args:
        name (str): The name of the quiz taker.
        questions (List[Dict[str, Any]]): A list of dictionaries containing question data.
    """
    print(f"Welcome, Test User! Let's start your adaptive quiz session.")
    controller = ARController(questions)
    controller.start()

def main() -> None:
    """
    Main function to set up and run the QuizMe CLI application.
    """
    parser = argparse.ArgumentParser(description="QuizMe: An adaptive quiz CLI application.")
    parser.add_argument('name', type=str, help="The name of the quiz taker.")
    parser.add_argument('--questions', type=Path, required=True, help="Path to the JSON file containing quiz questions.")
    
    args = parser.parse_args()
    
    try:
        questions = load_questions(args.questions)
        run_quiz(args.name, questions)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Exiting due to error in loading questions.")

if __name__ == "__main__":
    main()
