class Node:
    def __init__(self, value):
        self.obj = value
        self.next = None  # Pointer to next node

class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert(self, value):
        new_node = Node(value)
        if self.head is None:  # Empty list
            self.head = new_node
            return
        # Traverse to the end
        current = self.head
        while current.next:    
            current = current.next
        current.next = new_node

    def display(self):
        current = self.head
        while current:
            print(current.obj, end=" -> ")
            current = current.next
        print("None")

# Example
lst = SinglyLinkedList()
lst.insert(10)
lst.insert(20)
lst.insert(30)
lst.display()  # 10 -> 20 -> 30 -> None
