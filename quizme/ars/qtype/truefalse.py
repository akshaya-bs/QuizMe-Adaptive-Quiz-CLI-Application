"""Module for the TrueFalse quiz item class in the Adaptive Review System."""
# How to the testing 
# How to do the import 
from ars.qtype.question import Question
from typing import Any

class TrueFalse(Question):
    """Class for a True/False quiz item."""

    def __init__(self, question: str, answer: bool, explanation: str = ""):
        """
        Initialize a true/false quiz item.
        
        Args:
            question (str): The question to be displayed.
            answer (bool): The correct answer, either True or False.
            explanation (str, optional): Additional information to explain the correct answer.
        
        Raises:
            ValueError: If the answer is not a boolean.
        """
        if not isinstance (answer,bool):
            raise ValueError("Answer must be a boolean (True or False).")
        super().__init__(question, answer)
        self._explanation = explanation

    def ask(self) -> str:
        """
        Return the true/false question text.
        
        Returns:
            str: The text of the question.
        """
        super().ask()  # Update the last asked timestamp
        return f"{self._question} (True/False)"

    def check_answer(self, answer: str) -> bool:
        """
        Check if the provided answer is correct.
        
        Args:
            answer (str): The user's answer to the question.
        
        Returns:
            bool: True if the answer is correct, False otherwise.
        
        Raises:
            ValueError: If the answer is not 'True' or 'False'.
        """
        normalized_answer = answer.strip().lower()
        if normalized_answer in ["true", "t"]:
            user_answer = True
        elif normalized_answer in ["false", "f"]:
            user_answer = False
        else:
            raise ValueError(" Answer must be 'True' or 'False'.")
        
        return user_answer == self._answer

    def incorrect_feedback(self) -> str:
        """
        Return feedback for an incorrect answer.
        
        Returns:
            str: Feedback message for an incorrect answer, including the explanation if provided.
        """
        feedback = "Incorrect. "
        if self._explanation:
            feedback += f"{self._explanation}"
        return feedback
