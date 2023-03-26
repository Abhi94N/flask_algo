class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node

class LinkedList:
    def __init__(self):
        self.head = None
        self.last_node = None

    def print_linked_list(self):
        linked_list_string = ""
        node = self.head
        if node is None:
            print(None)
        while node:
            linked_list_string += f"{str(node.data)} -> "
            node = node.next_node
        linked_list_string += " None"
        print(linked_list_string)
    
    def insert_beginning(self, data):
        if self.head is None:
            self.head = Node(data, None)
            self.last_node = self.head
        new_node = Node(data, self.head)
        self.head = new_node

    def insert_at_end(self, data):
        if self.head is None:
            print(data)
            self.insert_beginning(data)
            return
        else:
            self.last_node.next_node = Node(data, None)
            self.last_node = self.last_node.next_node


linked_list = LinkedList()
Node4 = Node("data4", None)
Node3 = Node("data3", Node4)
Node2 = Node("data2", Node3)
Node1 = Node("data1", Node2)
linked_list.head = Node1

linked_list.print_linked_list()

linked_list.insert_beginning("data0")
linked_list.insert_beginning("not_data")
linked_list.insert_at_end("data5")
linked_list.insert_at_end("data6")
linked_list.print_linked_list()