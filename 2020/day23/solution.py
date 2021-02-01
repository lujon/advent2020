import fileinput


class Node:
    def __init__(self, value, next):
        self.value, self.next = value, next


class CircularLinkedList:
    def __init__(self, iterable=()):
        self.head = self.tail = None
        self.value_to_node = {v: self._append(v) for v in iterable}

    def _append(self, value):
        node = Node(value, self.head)
        if self.tail is None:
            self.head = self.tail = node
            node.next = node
        else:
            self.tail.next = node
            self.tail = node
        return node

    def __len__(self):
        return len(self.value_to_node)

    def __iter__(self):
        if self.head is None:
            return iter(())
        curr = self.head
        while True:
            yield curr.value
            curr = curr.next
            if curr == self.head:
                break

    def __getitem__(self, value):
        return self.value_to_node[value]

    def move_head(self):
        self.head, self.tail = self.head.next, self.head


def make_move(cup_list):
    current_cup = cup_list.head
    x = cup_list.head.next
    y = cup_list.head.next.next
    z = cup_list.head.next.next.next

    destination_value = current_cup.value

    while (destination_value := destination_value - 1) in (x.value, y.value, z.value) or destination_value == 0:
        if destination_value == 0:
            destination_value = len(cup_list) + 1

    current_cup.next = z.next
    destination_cup = cup_list[destination_value]
    z.next = destination_cup.next
    destination_cup.next = x
    cup_list.move_head()


input_rows = [line.rstrip() for line in fileinput.input('input.txt')]

numbers = [int(x) for x in input_rows[0]]

# Part 1

cup_list = CircularLinkedList(numbers)

for _ in range(100):
    make_move(cup_list)

while cup_list.head.value != 1:
    cup_list.move_head()

print("".join(map(str, cup_list))[1:])

# Part 2

cup_list = CircularLinkedList(numbers + list(range(len(numbers) + 1, 1_000_001)))

for _ in range(10_000_000):
    make_move(cup_list)

print(cup_list[1].next.value * cup_list[1].next.next.value)
