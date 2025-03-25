class QueueOfDistinctStrings:
    """
    A FIFO queue that holds distinct strings.

    Abstraction Function:
        - The queue is represented by a list of strings (_items), where the element at index 0
          is considered the front and the element at the last index is the end.
        - This abstractly represents a collection of strings where each string appears only once,
          and the order of insertion is maintained (FIFO).

    Representation Invariant:
        - _items is not None.
        - No element in _items is None.
        - All elements in _items are unique.
    """

    def __init__(self):
        """Initializes an empty queue of distinct strings."""
        self._items = []

    def enqueue(self, element: str) -> None:
        """
        Appends the element at the end of the queue if it is not already present.
        
        Raises:
            ValueError: If element is None.
        """
        if element is None:
            raise ValueError("Cannot enqueue None")
        if element not in self._items:
            self._items.append(element)

    def dequeue(self) -> str:
        """
        Removes and returns the element from the front of the queue.
        
        Raises:
            ValueError: If the queue is empty.
        """
        if not self._items:
            raise ValueError("Queue is empty")
        return self._items.pop(0)

    def rep_ok(self) -> bool:
        """
        Checks the representation invariant of the queue.
        
        Returns:
            bool: True if the invariant holds, False otherwise.
        """
        if self._items is None:
            return False
        seen = set()
        for item in self._items:
            if item is None:
                return False
            if item in seen:
                return False
            seen.add(item)
        return True

    def __str__(self) -> str:
        """
        Returns a string representation of the queue, showing its items and indicating
        the front and end.
        """
        if not self._items:
            return "Queue is empty"
        front = self._items[0]
        end = self._items[-1]
        return (f"The queue consists of {self._items} "
                f"where the Front is '{front}' and the End is '{end}'")


# Educational points to note:
# 1. **Abstraction Function & Representation Invariant:** 
#    - The abstraction function maps the concrete list representation to the abstract queue concept.
#    - The rep invariant ensures that the internal list does not contain duplicates or None values.
#
# 2. **Encapsulation and Data Hiding:** 
#    - The internal attribute _items is prefixed with an underscore to indicate it is intended for internal use.
#
# 3. **Exception Handling:** 
#    - Instead of using a generic Exception, specific exceptions (like ValueError) are raised for clarity.
#
# 4. **Pythonic Practices:**
#    - Using docstrings and type hints improves code readability and maintainability.
#    - The __str__ method provides a meaningful string representation, which is useful for debugging and logging.
#
# 5. **Mutability and Immutability:**
#    - Although the queue is mutable (items can be added or removed), the design is structured to maintain
#      a valid state by ensuring the rep invariant is always satisfied.
#
# 6. **Testing the Implementation:**
#    - It is recommended to write unit tests to verify the behavior of enqueue, dequeue, rep_ok, and __str__ methods.

if __name__ == '__main__':
    q = QueueOfDistinctStrings()
    try:
        q.enqueue("apple")
        q.enqueue("banana")
        q.enqueue("apple")  # This will not be added again.
        q.enqueue("cherry")
        print(q)  # Expected to show a queue with "apple" at the front and "cherry" at the end.
        print("Representation OK:", q.rep_ok())
        print("Dequeued:", q.dequeue())
        print(q)
    except ValueError as e:
        print("Error:", e)