class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node


class LinkedList:
    def __init__(self):
        self.head = None

    def push(self, value):
        self.head = Node(value, self.head)

    def append(self, value):
        if self.head is None:
            self.head = Node(value)
            return
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = Node(value)

    def to_list(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result

    @classmethod
    def from_iterable(cls, iterable):
        ll = cls()
        for item in iterable:
            ll.append(item)
        return ll


def reverse(linked_list: LinkedList) -> LinkedList:
    prev = None
    current = linked_list.head
    while current is not None:
        nxt = current.next
        current.next = prev
        prev = current
        current = nxt
    linked_list.head = prev
    return linked_list


def _split(head):
    slow = head
    fast = head.next
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    second = slow.next
    slow.next = None
    return head, second


def _merge_nodes(a, b):
    dummy = Node(None)
    tail = dummy
    while a is not None and b is not None:
        if a.value <= b.value:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
    tail.next = a if a is not None else b
    return dummy.next


def _merge_sort_nodes(head):
    if head is None or head.next is None:
        return head
    first, second = _split(head)
    return _merge_nodes(_merge_sort_nodes(first), _merge_sort_nodes(second))


def merge_sort(linked_list: LinkedList) -> LinkedList:
    linked_list.head = _merge_sort_nodes(linked_list.head)
    return linked_list


def merge_sorted_lists(a: LinkedList, b: LinkedList) -> LinkedList:
    result = LinkedList()
    result.head = _merge_nodes(a.head, b.head)
    return result


if __name__ == "__main__":
    ll = LinkedList.from_iterable([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
    print(f"Початковий список: {ll.to_list()}")

    reverse(ll)
    print(f"Реверсований:      {ll.to_list()}")

    merge_sort(ll)
    print(f"Відсортований:     {ll.to_list()}")

    a = LinkedList.from_iterable([1, 4, 7, 10])
    b = LinkedList.from_iterable([2, 3, 5, 8, 9])
    merged = merge_sorted_lists(a, b)
    print(f"Об'єднання [1,4,7,10] та [2,3,5,8,9]: {merged.to_list()}")
