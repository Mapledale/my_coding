#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

"""
Design your implementation of the linked list.
You can choose to use the singly linked list or the doubly linked list.
A node in a singly linked list should have two attributes: val and next.
val is the value of the current node, and next is a pointer/reference
to the next node. If you want to use the doubly linked list, you will need
one more attribute prev to indicate the previous node in the linked list.
Assume all nodes in the linked list are 0-indexed.

Implement these functions in your linked list class:

get(index) : Get the value of the index-th node in the linked list. If
the index is invalid, return -1.

addAtHead(val) : Add a node of value val before the first element of the
linked list. After the insertion, the new node will be the first node of
the linked list.

addAtTail(val) : Append a node of value val to the last element of the
linked list.

addAtIndex(index, val) : Add a node of value val before the index-th node
in the linked list. If index equals to the length of linked list, the node
will be appended to the end of linked list. If index is greater than the
length, the node will not be inserted.

deleteAtIndex(index) : Delete the index-th node in the linked list, if the
index is valid.

Example:
MyLinkedList linkedList = new MyLinkedList();
linkedList.addAtHead(1);
linkedList.addAtTail(3);
linkedList.addAtIndex(1, 2);  // linked list becomes 1->2->3
linkedList.get(1);            // returns 2
linkedList.deleteAtIndex(1);  // now the linked list is 1->3
linkedList.get(1);            // returns 3

Note:
All values will be in the range of [1, 1000].
The number of operations will be in the range of [1, 1000].
Please do not use the built-in LinkedList library.
"""


class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None


class MyLinkedList:
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.head = None
        self.size = 0

    def get(self, index: int) -> int:
        """ Get the value of the index-th node in the linked list.
        If the index is invalid, return -1.
        """
        if index < 0 or index >= self.size or self.head is None:
            return -1
        return self.findIndex(index).val

    def addAtHead(self, val: int) -> None:
        """ Add a node of value val
        before the first element of the linked list. After the insertion,
        the new node will be the first node of the linked list.
        """
        self.addAtIndex(0, val)

    def addAtTail(self, val: int) -> None:
        """
        Append a node of value val to the last element of the linked list.
        """
        self.addAtIndex(self.size, val)

    def addAtIndex(self, index: int, val: int) -> None:
        """ Add a node of value val
        before the index-th node in the linked list. If index equals to
        the length of linked list, the node will be appended to the end
        of linked list. If index is greater than the length, the node
        will not be inserted.
        """
        if index > self.size:
            return -1
        elif index == 0:
            head = ListNode(val)
            head.next, self.head = self.head, head
        else:
            pre = self.findIndex(index - 1)
            cur = ListNode(val)
            cur.next, pre.next = pre.next, cur
        self.size += 1

    def deleteAtIndex(self, index: int) -> None:
        """
        Delete the index-th node in the linked list, if the index is valid.
        """
        if index < 0 or index >= self.size:
            return -1
        cur = self.findIndex(index - 1)
        cur.next = cur.next.next
        self.size -= 1

    def findIndex(self, index: 'int') -> 'None':
        cur = self.head
        for _ in range(index):
            cur = cur.next
        return cur

# Your MyLinkedList object will be instantiated and called as such:
# obj = MyLinkedList()
# param_1 = obj.get(index)
# obj.addAtHead(val)
# obj.addAtTail(val)
# obj.addAtIndex(index,val)
# obj.deleteAtIndex(index)
