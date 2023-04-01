from __future__ import annotations
# be able to work with future python updates
from dataclasses import dataclass
# how objects are manipulated
from datetime import date
# allows you to work with dates
from typing import Optional, List, Set
# these classes imported for the data


class OutOfStock(Exception):
    pass
# if it out of stock to not show error message


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {line.sku}")
# this fuction allows the class Orderline to allocate items to Batch there is inventory
# if there is no inventory it will raise the execption in line 11 and print message


@dataclass(frozen=True)
# does not change
class OrderLine:
    orderid: str
    sku: str
    qty: int
# creating class Orderline with the attrrbutes, the types are string and integer


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()  # track of all allocated orders
        Set[OrderLine]  # type: Set[OrderLine]
# creating class called batch with the parameters
# proteries are defined with parameters

    def __repr__(self):
        return f"<Batch {self.reference}>"
    # prints out a string that represents the object in Batch

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference
    # compares two batch references for equality

    def __hash__(self):
        return hash(self.reference)
    # calculate hash value for self.reference

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta
    # greater than method, eta must be greater than other
    # more explaination

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)
    # first checks to see if the line item can be allocated
    # if yes, then added to the self._allocations list

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)
    # if no, then removes from list

    @property  # not sure what @property is??
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)
    # assume will return the new total allocated

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity
    # assume will return the available inventory

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty
    # assume will check to see if there is enough inventory
