"""Module for the base Question class in the Adaptive Review System."""
#Any import at multiple locations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Optional
import uuid

class Question(ABC):
    """Abstract base class for quiz questions in the Adaptive Review System."""

    def __init__(self, question: str, answer: Any):
        """
        Initialize a new Question instance.

        Args:
            question (str): The text of the question.
            answer (object): The correct answer to the question.
        """
        self._id = uuid.uuid4()
        self._question = question
        self._answer = answer
        self._last_asked = datetime.min

    @property
    def id(self) -> uuid.UUID:
        """Get the unique identifier of the question."""
        return self._id

    @property
    def last_asked(self) -> Optional[datetime]:
        """Get the timestamp of when the question was last asked."""
        return self._last_asked

    def ask(self) -> str:
        """
        Return the question as a string and update the last asked time.

        Returns:
            str: The text of the question.
        """
        self._last_asked = datetime.now()
        return self._question

    def reset(self) -> None:
        """Reset the last asked time to None."""
        self._last_asked = None

    @abstractmethod
    def check_answer(self, answer: Any) -> bool:
        """
        Check if the provided answer is correct.

        Args:
            answer (object): The answer to check.

        Returns:
            bool: True if the answer is correct, False otherwise.
        """
        pass

    @abstractmethod
    def incorrect_feedback(self) -> str:
        """
        Return feedback for an incorrect answer.

        Returns:
            str: Feedback message for an incorrect answer.
        """
        pass

    def __eq__(self, other: object) -> bool:
        """
        Define equality based on the question's unique id.

        Args:
            other (object): The object to compare with.

        Returns:
            bool: True if the other object is a Question with the same id, False otherwise.
        """
        if isinstance(other, Question):
            return self._id == other.id
        return False

    def __hash__(self) -> int:
        """
        Define a hash value based on the question's unique id.

        Returns:
            int: Hash value of the question's unique id.
        """
        return hash(self._id)

    def __repr__(self) -> str:
        """
        Return a string representation of the Question object.

        Returns:
            str: String representation of the Question object.
        """
        return f"Question(id={self._id}, question={self._question})"
