"""Module for the ShortAnswer quiz item class in the Adaptive Review System."""
# How do the testing 
# How to do the qtype import 
# theres an ask method in the method list but no implementation detials
import re
from ars.qtype.question import Question

class ShortAnswer(Question):
    """A quiz item representing a short answer question."""

    def __init__(self, question: str, answer: str, case_sensitive: bool = False):
        """
        Initialize a short answer quiz item.

        Args:
            question (str): The question prompt.
            answer (str): The correct answer.
            case_sensitive (bool, optional): Whether the answer comparison should be case-sensitive. 
                                             Defaults to False.
        """
        super().__init__(question, answer)
        self._case_sensitive = case_sensitive

    def _normalize(self, text: str) -> str:
        """
        Normalize the text for comparison.

        Args:
            text (str): The text to normalize.

        Returns:
            str: The normalized text.
        """
        text = text.strip()
        if not self._case_sensitive:
            text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def check_answer(self, answer: str) -> bool:
        """
        Check if the provided answer is correct.

        Args:
            answer (str): The provided answer.

        Returns:
            bool: True if the provided answer is correct, False otherwise.
        """
        normalized_provided_answer = self._normalize(answer)
        normalized_correct_answer = self._normalize(self._answer)
        return normalized_provided_answer == normalized_correct_answer

    def incorrect_feedback(self) -> str:
        """
        Return feedback for an incorrect answer.

        Returns:
            str: Feedback message for an incorrect answer.
        """
        return f"Incorrect. The correct answer is: {self._answer}"
