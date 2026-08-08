class Node:
    def __init__(self, value):
        self.value = value
        self.next = None  # Pointer to next node
        
class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, value):
        new_node = Node(value)
        if self.rear is None:  # Empty queue
            self.front = self.rear = new_node
            return
        self.rear.next = new_node
        self.rear = new_node

    def dequeue(self):
        if self.front is None:
            return None
        value = self.front.value
        self.front = self.front.next
        if self.front is None:  # Queue became empty
            self.rear = None
        return value

    def display(self):
        current = self.front
        while current:
            print(current.value, end=" <- ")
            current = current.next
        print("None")

# Example
q = Queue()
q.enqueue("A")
q.enqueue("B")
q.display()         # A <- B <- None
print(q.dequeue())  # A
q.display()         # B <- None
