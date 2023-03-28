class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node
    
class Data:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class HashTable:
    def __init__(self, table_size):
        self.table_size = table_size
        self.hash_table = [None] * table_size

    def custom_hash(self, key):
        hash_value = 0
        for i in key:
            # Return the Unicode code point for a one-character string.
            hash_value += ord(i)
            # add randomness
            hash_value = (hash_value * ord(i)) % self.table_size 
        return hash_value
    
    def add_key_value(self, key, value):
        hashed_key = self.custom_hash(key)
        if self.hash_table[hashed_key] is None:
            self.hash_table[hashed_key] = Node(Data(key, value), None)
        else:
            # a collision has occurred so iterate over linked list and add node 
            node = self.hash_table[hashed_key]
            while node.next_node:
                node = node.next_node
            # once you reach the last node
            node.next_node = Node(Data(key, value), None)
    
    def get_value(self, key):
        hashed_key = self.custom_hash(key)
        if self.hash_table[hashed_key] is not None:
            node = self.hash_table[hashed_key]
            if node.next_node is None:
                return node.data.value
            while node.next_node:
                if key == node.data.key:
                    return node.data.value
                node = node.next_node
            if key == node.data.key:
                return node.data.value
        return None 
    
    def print_table(self):
        print("{")
        for i, val in enumerate(self.hash_table):
            if val is not None:
                linked_list_string = ""
                node = val
                if node.next_node:
                    # print all node as long as there is next node
                    while node.next_node:
                        linked_list_string += (
                            str(node.data.key) + " : " + str(node.data.value) + " -->"
                        )
                        node = node.next_node

                    # get the last node and in linked list
                    linked_list_string += (
                        str(node.data.key) + " : " + str(node.data.value) + " --> None"
                    )
                    # traverse the linked list value as long as there is a next node
                    print(f" [{i}] {linked_list_string}")
                else:
                    # if last node get the key and value
                    print(f" [{i}] {val.data.key} : {val.data.value}")
            else:
                # if value is none print out the value
                print(f" [{i}] {val}")
        print("}")
