# Name: Joshua Arnett
# OSU Email: arnettj@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4
# Due Date: 07/30/2004
# Description: Defines an AVL class that inherits from a BST class that employs various methods, including methods
#               to add to, remove from, and traverse a tree.


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Adds a new node containing the specified value to the appropriate place in the BST.
        """
        parent_node = None
        current_node = self._root

        # We find the correct location to insert the node
        while current_node is not None:
            parent_node = current_node
            if current_node.value == value:     # No duplicates
                return None
            if value < current_node.value:
                current_node = current_node.left
            else:
                current_node = current_node.right

        # If parent_node is None, the BST is empty. So we set the root equal to an AVL node holding the specified value
        if parent_node is None:
            self._root = AVLNode(value)
        # Else, we determine whether the child should be on the left or right side
        else:
            if value < parent_node.value:
                parent_node.left = AVLNode(value)
                current_node = parent_node.left      # We set current_value equal to itself so it doesn't equal None
            else:
                parent_node.right = AVLNode(value)
                current_node = parent_node.right     # We set current_value equal to itself so it doesn't equal None
            current_node.parent = parent_node

            self._rebalance(current_node.parent)

    def remove(self, value: object) -> bool:
        """
        Removes a value from the AVL tree. Returns true if value is successfully removed, and False otherwise.
        """
        if self.is_empty():
            return False

        # Finding the node we want to remove
        node = self._root
        while node.value != value:
            if value < node.value:
                node = node.left
            else:
                node = node.right

            # We return False if the node is None before the value is found
            if node is None:
                return False

        parent_node = node.parent
        # If the node we are removing has no subtree #
        if node.left is None and node.right is None:
            last_modified_node = self._remove_no_subtrees(parent_node, node)

        # If the node we are removing has one subtree #
        elif node.left is None or node.right is None:
            last_modified_node = self._remove_one_subtree(parent_node, node)

        # If the node we are removing has two subtrees #
        else:
            last_modified_node = self._remove_two_subtrees(parent_node, node)

        if last_modified_node is not None:
            self._rebalance(last_modified_node)
        return True

    def _remove_no_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        """
        Removes a node that has no subtrees (no left or right nodes). Returns the last modified node.
        """
        # If we are removing the root, we set it equal to None. ELse, we point remove_node's parent to None.
        if remove_node == self._root:
            self._root = None
        elif remove_node.value < remove_parent.value:
            remove_parent.left = None
        else:
            remove_parent.right = None

        return remove_parent

    def _remove_one_subtree(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        """
        Removes a node that has a left or right subtree (only). Returns the last modified node.
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
            remove_node.right.parent = remove_parent

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
            remove_node.left.parent = remove_parent

        return remove_parent

    def _remove_two_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        """
        Removes a node that has two subtrees. Returns the last modified node.
        """
        # We find the node's inorder successor
        inorder_successor, inorder_successor_parent = self._find_inorder_successor(remove_node)

        # remove_node's left subtree becomes inorder_successor's
        inorder_successor.left = remove_node.left
        remove_node.left.parent = inorder_successor

        if remove_node.right != inorder_successor:
            # inorder_successor's right subtree becomes its parent's left
            inorder_successor_parent.left = inorder_successor.right
            if inorder_successor.right is not None:
                inorder_successor.right.parent = inorder_successor_parent

            # remove_node's right subtree becomes inorder_successor's
            inorder_successor.right = remove_node.right
            remove_node.right.parent = inorder_successor

        # Remove the node
        if remove_node == self._root:
            self._root = inorder_successor
        elif inorder_successor.value < remove_parent.value:
            remove_parent.left = inorder_successor
        else:
            remove_parent.right = inorder_successor

        # Update inorder_successor's parent value
        inorder_successor.parent = remove_parent

        # If inorder_successor != remove_node's right child, inorder_successor's parent is the last modified node
        if remove_node.right != inorder_successor:
            return inorder_successor_parent
        # Else, inorder_successor is the last modified node
        else:
            return inorder_successor

    def _find_inorder_successor(self, remove_node: AVLNode) -> (AVLNode, AVLNode):
        """
        Returns the inorder successor of an AVLNode object.
        """
        # Give our inorder successor and its parent starting values
        inorder_successor = remove_node.right

        # If remove_node's right child has a left subtree, we keep traversing left until we arrive at the lowest value
        while inorder_successor.left is not None:
            inorder_successor = inorder_successor.left

        return inorder_successor, inorder_successor.parent

    def _balance_factor(self, node: AVLNode) -> int:
        """
        Returns the balance factor of a node.
        """
        right_height = self._get_height(node.right)
        left_height = self._get_height(node.left)

        return right_height - left_height

    def _get_height(self, node: AVLNode) -> int:
        """
        Returns the height of a node.
        """
        if node is None:
            return -1
        return node.height

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        Rotate the given AVL node to the left. Returns the node whose position is upgraded.
        """
        c = node.right
        node.right = c.left
        if node.right is not None:
            node.right.parent = node
        c.left = node
        node.parent = c

        # Update the heights of the affected nodes
        self._update_height(node)
        self._update_height(c)
        return c

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        Rotate the given AVL node to the right. Returns the node whose position is upgraded.
        """
        c = node.left
        node.left = c.right
        if node.left is not None:
            node.left.parent = node
        c.right = node
        node.parent = c

        # Update the heights of the affected nodes
        self._update_height(node)
        self._update_height(c)
        return c

    def _update_height(self, node: AVLNode) -> None:
        """
        Updates the height of a node.
        """
        left_height = self._get_height(node.left)
        right_height = self._get_height(node.right)

        node.height = max(right_height, left_height) + 1

    def _rebalance(self, node: AVLNode) -> None:
        """
        Rebalances the given node and its ancestors within the AVL tree.
        """
        while node is not None:
            balance_factor = self._balance_factor(node)

            if balance_factor < -1 or balance_factor > 1:
                # If node is left heavy
                if balance_factor < -1:
                    # If node requires double left rotation
                    if self._balance_factor(node.left) > 0:
                        node.left = self._rotate_left(node.left)
                        node.left.parent = node
                    # Single right rotation
                    node_parent = node.parent
                    new_subtree_root = self._rotate_right(node)
                    new_subtree_root.parent = node_parent

                # If node is right heavy
                elif balance_factor > 1:
                    # If node requires double right rotation
                    if self._balance_factor(node.right) < 0:
                        node.right = self._rotate_right(node.right)
                        node.right.parent = node
                    # Single right rotation
                    node_parent = node.parent
                    new_subtree_root = self._rotate_left(node)
                    new_subtree_root.parent = node_parent

                # Update node_parent's child to equal the new subtree
                if node_parent is None:
                    self._root = new_subtree_root
                elif new_subtree_root.value < node_parent.value:
                    node_parent.left = new_subtree_root
                else:
                    node_parent.right = new_subtree_root
            else:
                # If the node does not require rebalancing, simply update its height
                self._update_height(node)

            # Rebalance its parent
            node = node.parent


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':
    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)
        tree.print_tree()

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.print_tree()
        tree.remove(del_value)
        print('RESULT :', tree)
        tree.print_tree()
        print('')

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
