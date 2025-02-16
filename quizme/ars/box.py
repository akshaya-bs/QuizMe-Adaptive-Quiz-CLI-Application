"""Module for the Box class in the Adaptive Review System."""
#import qtype
# last question is it datetime.min
from datetime import datetime, timedelta
from typing import List, Optional
from ars.qtype.question import Question

class Box:
    """Represents a box that holds a set of questions for adaptive review."""

    def __init__(self, name: str, priority_interval: timedelta):
        """
        Initialize a new Box instance.

        Args:
            name (str): The name of the box.
            priority_interval (timedelta): The time interval for prioritizing questions.
        """
        self._name = name
        self._questions: List[Question] = [] #type hint is it required because in the attributes it says type
        self._priority_interval = priority_interval

    @property
    def name(self) -> str:
        """Returns the name of the box."""
        return self._name

    @property
    def priority_interval(self) -> timedelta:
        """Returns the priority interval of the box."""
        return self._priority_interval

    def add_question(self, question: Question) -> None:
        """
        Add a question to the box.

        Args:
            question (Question): The question to be added.
        """
        if question not in self._questions:
            self._questions.append(question)

    def remove_question(self, question: Question) -> None:
        """
        Remove a question from the box.

        Args:
            question (Question): The question to be removed.
        """
        if question in self._questions:
            self._questions.remove(question)

    def get_next_priority_question(self) -> Optional[Question]:
        """
        Return the next priority question if available.

        Returns:
            Optional[Question]: The next priority question or None if no priority question is available.
        """
        sorted_questions = sorted(self._questions, key=lambda q: q.last_asked or datetime.min)
        now = datetime.now()
        for question in sorted_questions:
            if (now - (question.last_asked or datetime.min)) >= self._priority_interval:
                return question
        return None

    def __len__(self) -> int:
        """Return the number of questions in the box."""
        return len(self._questions)

    def __str__(self) -> str:
        """Return a string representation of the Box object."""
        return f"Box(name='{self._name}', questions_count={len(self._questions)})"
