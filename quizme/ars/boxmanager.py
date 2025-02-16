"""Module for managing boxes in the Adaptive Review System."""
#import qtype
# last question is it datetime.min

from datetime import timedelta
from typing import List, Dict, Optional
from ars.qtype.shortanswer import ShortAnswer
from ars.box import Box  # Assuming you have a Box class defined somewhere

class BoxManager:
    """Manages multiple boxes in the Adaptive Review System."""

    def __init__(self):
        """Initialize a new BoxManager instance.

        Creates predefined boxes with specific priority intervals:
            - "Missed Questions": 60 seconds
            - "Unasked Questions": 0 seconds (no delay)
            - "Correctly Answered Once": 180 seconds
            - "Correctly Answered Twice": 360 seconds
            - "Known Questions": timedelta.max
        """
        self._boxes = [
            Box("Missed Questions", timedelta(seconds=60)),
            Box("Unasked Questions", timedelta(seconds=0)),
            Box("Correctly Answered Once", timedelta(seconds=180)),
            Box("Correctly Answered Twice", timedelta(seconds=360)),
            Box("Known Questions", timedelta.max)
        ]
        self._question_location: Dict[str, int] = {}

    def add_new_question(self, question: ShortAnswer):
        """Add a new question to the Unasked Questions box.

        Args:
            question (ShortAnswer): The question to add.

        The question's ID is stored as a string key in the `_question_location` dictionary.
        """
        self._boxes[1].add_question(question)
        self._question_location[str(question.id)] = 1

    def move_question(self, question: ShortAnswer, answered_correctly: bool):
        """Move a question based on whether it was answered correctly.

        Args:
            question (ShortAnswer): The question to move.
            answered_correctly (bool): True if the question was answered correctly, False otherwise.

        Moves the question to a new box based on the current box and the correctness of the answer.
        Updates `_question_location` with the new index and logs the box counts.
        """
        current_box_index = self._question_location[str(question.id)]
        if not answered_correctly:
            new_box_index = 0
        else:
            new_box_index = min(current_box_index + 1, len(self._boxes) - 1)
        self._boxes[current_box_index].remove_question(question)
        self._boxes[new_box_index].add_question(question)
        self._question_location[str(question.id)] = new_box_index
        self._log_box_counts()

    def get_next_question(self) -> Optional[ShortAnswer]:
        """Determine and return the next question to present.

        Returns:
            Optional[ShortAnswer]: The next question to present, or None if no question is available.

        Iterates through all boxes except the "Known Questions" box to find the next priority question.
        """
        for box in self._boxes[:-1]:
            question = box.get_next_priority_question()
            if question:
                return question
        return None

    def _log_box_counts(self):
        """Log the number of questions in each box by name and count.

        Useful for tracking the distribution of questions across the system.
        """
        for box in self._boxes:
            print(f"{box.name}: {len(box._questions)} questions")

