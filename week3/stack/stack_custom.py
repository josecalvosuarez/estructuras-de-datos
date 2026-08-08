class Node:
    def __init__(self, value):
        self.value = value
        self.next = None  # Pointer to next node

class Stack:
    def __init__(self):
        self.top = None

    def push(self, value):
        new_node = Node(value)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.top is None:
            return None
        value = self.top.value
        self.top = self.top.next
        return value

    def peek(self):
        return None if self.top is None else self.top.value

    def display(self):
        current = self.top
        while current:
            print(current.value, end=" -> ")
            current = current.next
        print("None")

# Example
s = Stack()
s.push(1)
s.push(2)
s.push(3)
s.display()         # 3 -> 2 -> 1 -> None
print(s.pop())      # 3
s.display()         # 2 -> 1 -> None
