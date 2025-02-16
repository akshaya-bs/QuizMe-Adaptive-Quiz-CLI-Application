"""Core module for running the Adaptive Review System (ARS) session."""
from typing import List, Dict, Any
from ars.boxmanager import BoxManager
from ars.qtype.shortanswer import ShortAnswer
from ars.qtype.truefalse import TrueFalse
from ars.qtype.question import Question


class ARController:
    """Main controller for running an adaptive review session."""

    def __init__(self, question_data: List[Dict[str, Any]]):
        """Initialize the Adaptive Review Controller.

        Args:
            question_data (List[Dict[str, Any]]): A list of dictionaries containing question data.
        """
        self._box_manager = BoxManager()
        self._initialize_questions(question_data)

    def _initialize_questions(self, question_data: List[Dict[str, Any]]):
        """Initialize questions and place them in the Unasked Questions box.

        Args:
            question_data (List[Dict[str, Any]]): A list of dictionaries containing question data.
        """
        for q_data in question_data:
            q_type = q_data.get("type")
            try:
                if q_type == "shortanswer":
                    question = ShortAnswer(
                        q_data["question"],
                        q_data["correct_answer"],
                        q_data.get("case_sensitive", False)
                    )
                elif q_type == "truefalse":
                    question = TrueFalse(
                        q_data["question"],
                        q_data["correct_answer"],
                        q_data.get("explanation", "")
                    )
                else:
                    print(f"Unsupported question type: {q_type}"f". Skipping this question.")
                    continue
                self._box_manager.add_new_question(question)
            except KeyError as e:
                print(f"Missing required field for question: {e}. Skipping this question.")

    def start(self) -> None:
        """Run the interactive adaptive review session."""
        print("Type 'q' at any time to quit the session.")
        while True:
            next_question = self._box_manager.get_next_question()
            if not next_question:
                print("All questions have been reviewed. Session complete!")
                break

            print(next_question.ask())
            user_answer = input("Your answer: ")
            if user_answer.lower() == 'q':
                break

            correct = next_question.check_answer(user_answer)
            if correct:
                print("Correct!")
            else:
                print(next_question.incorrect_feedback())
            self._box_manager.move_question(next_question, correct)

        print("Thank you, goodbye!")

