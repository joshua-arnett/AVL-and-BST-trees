# Name: Joshua Arnett
# OSU Email: arnettj@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4
# Due Date: 07/30/2004
# Description: Defines a BST (binary search tree) class that employs various methods, including methods
#               to add to, remove from, and traverse a tree.


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value   # to store node's data
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    def print_tree(self):
        """
        Prints the tree using the print_subtree function.

        This method is intended to assist in visualizing the structure of the
        tree. You are encouraged to add this method to the tests in the Basic
        Testing section of the starter code or your own tests as needed.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.get_root():
            self._print_subtree(self.get_root())
        else:
            print('(empty tree)')

    def _print_subtree(self, node, prefix: str = '', branch: str = ''):
        """
        Recursively prints the subtree rooted at this node.

        This is intended as a 'helper' method to assist in visualizing the
        structure of the tree.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """

        def add_junction(string):
            if len(string) < 2 or branch == '':
                return string
            junction = '|' if string[-2] == '|' else '`'
            return string[:-2] + junction + '-'

        if not node:
            print(add_junction(prefix) + branch + "None")
            return

        if len(prefix) > 2 * 16:
            print(add_junction(prefix) + branch + "(tree continues)")
            return

        if node.left or node.right:
            postfix = ' (root)' if branch == '' else ''
            print(add_junction(prefix) + branch + str(node.value) + postfix)
            self._print_subtree(node.right, prefix + '| ', 'R: ')
            self._print_subtree(node.left, prefix + '  ', 'L: ')
        else:
            print(add_junction(prefix) + branch + str(node.value) + ' (leaf)')

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Adds a new node containing the specified value to the appropriate place in the BST.
        """
        parent_node = None
        current_node = self._root
        while current_node is not None:
            parent_node = current_node
            if value < current_node.value:
                current_node = current_node.left
            else:
                current_node = current_node.right

        # If parent_node is None, the BST is empty. So we set the root equal to a BST node holding the specified value
        if parent_node is None:
            self._root = BSTNode(value)
        # Else, we determine whether the child should be on the left or right side
        else:
            if value < parent_node.value:
                parent_node.left = BSTNode(value)
            else:
                parent_node.right = BSTNode(value)

    def remove(self, value: object) -> bool:
        """
        Removes a node from a BST.
        """
        if self.is_empty():
            return False
        node = self._root

        # Finding the node we want to remove, as well as its parent
        parent = node
        while node.value != value:
            parent = node
            if value < node.value:
                node = node.left
            else:
                node = node.right

            # We return False if the node is None before the value is found
            if node is None:
                return False

        # If the node we are removing has no children #
        if node.left is None and node.right is None:
            self._remove_no_subtrees(parent, node)

        # If the node we are removing has one subtree #
        if node.left is None or node.right is None:
            self._remove_one_subtree(parent, node)

        # If the node we are removing has two subtrees #
        else:
            self._remove_two_subtrees(parent, node)

        return True

    def _remove_no_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Removes a node that has no subtrees (no left or right nodes).
        """
        if remove_node == self._root:
            self._root = None
        elif remove_node.value < remove_parent.value:
            remove_parent.left = None
        else:
            remove_parent.right = None

    def _remove_one_subtree(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Removes a node that has a left or right subtree (only).
        """
        # If our node only has a right subtree...
        if remove_node.left is None:
            # And we are removing the root, replace the root with the subtree
            if remove_node == self._root:
                self._root = remove_node.right

            # We connect it to the parent node
            elif remove_node.value < remove_parent.value:
                remove_parent.left = remove_node.right
            else:
                remove_parent.right = remove_node.right

        # If our node only has a left subtree...
        elif remove_node.right is None:
            # And we are removing the root, replace the root with the subtree
            if remove_node == self._root:
                self._root = remove_node.left

            # We connect it to the parent node
            elif remove_node.value < remove_parent.value:
                remove_parent.left = remove_node.left
            else:
                remove_parent.right = remove_node.left

    def _remove_two_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Removes a node that has two subtrees.
        """
        # We find the node's inorder successor
        inorder_successor, inorder_successor_parent = self._find_inorder_successor(remove_node)

        # We update pointers to give the node’s children to its inorder successor, based on whether
        # remove_node.right has a left subtree
        if remove_node.right.left is not None:
            inorder_successor.left = remove_node.left
            inorder_successor_parent.left = inorder_successor.right
            inorder_successor.right = remove_node.right
        else:
            inorder_successor.left = remove_node.left

        # Remove the node
        if remove_node == self._root:
            self._root = inorder_successor
        elif inorder_successor.value < remove_parent.value:
            remove_parent.left = inorder_successor
        else:
            remove_parent.right = inorder_successor

    def _find_inorder_successor(self, remove_node: BSTNode) -> (BSTNode, BSTNode):
        """
        Returns the inorder successor of a BSTNode object.
        """
        # Give our inorder successor and its parent starting values
        inorder_successor = remove_node.right
        inorder_successor_parent = remove_node

        # If remove_node's right child has a left subtree, we keep traversing left until we arrive at the lowest value
        while inorder_successor.left is not None:
            inorder_successor_parent = inorder_successor
            inorder_successor = inorder_successor.left

        return inorder_successor, inorder_successor_parent

    def contains(self, value: object) -> bool:
        """
        Returns True if the specified value is found within the BST. Returns False otherwise.
        """
        node = self._root

        # We traverse the tree until we arrive at our value.
        while node is not None:
            if node.value == value:
                return True
            elif value < node.value:
                node = node.left
            else:
                node = node.right

        return False

    def inorder_traversal(self) -> Queue:
        """
        Returns a Queue object that contains the values of BST nodes in inorder traversal order.
        """
        # -------------------- inorder traversal follows an LNR algorithm -------------------- #
        stack = Stack()
        queue = Queue()

        if self.is_empty():
            return queue

        # Start from the root
        node = self._root
        while node is not None:
            # We push all the leftmost values of the tree to the stack        <-- LEFT
            while node is not None:
                stack.push(node)
                node = node.left

            # We pop the most recent one (leftmost value)           <-- NODE
            node = stack.pop()
            queue.enqueue(node.value)

            # We traverse the right subtree             <-- RIGHT
            if node.right is not None:
                node = node.right
            else:
                while node.right is None and stack.is_empty() is False:
                    # Until the stack is empty or a right child is available, we keep moving back up the tree

                    node = stack.pop()
                    queue.enqueue(node.value)
                node = node.right

        return queue

    def find_min(self) -> object:
        """
        Returns the max value within a BST.
        """
        if self.is_empty():
            return None

        node = self._root
        value = node.value
        while node is not None:
            value = node.value
            node = node.left

        return value

    def find_max(self) -> object:
        """
        Returns the max value within a BST.
        """
        if self.is_empty():
            return None

        node = self._root
        value = node.value
        while node is not None:
            value = node.value
            node = node.right

        return value

    def is_empty(self) -> bool:
        """
        Returns True if BST is empty.
        """
        return self._root is None

    def make_empty(self) -> None:
        """
        Empty a BST.
        """
        self._root = None


# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)
        tree.print_tree()

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.print_tree()
        tree.remove(del_value)
        print('RESULT :', tree)
        tree.print_tree()
        print('')

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
