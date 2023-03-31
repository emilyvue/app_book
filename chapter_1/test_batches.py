from datetime import date
from model import Batch, OrderLine
# imports two functions from model.py


def test_allocating_to_a_batch_reduces_the_available_quantity():
    # testing to see if Orderline is subtracting correctly from Batch
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    line = OrderLine("order-ref", "SMALL-TABLE", 2)

    batch.allocate(line)
    # 2 tables are order and taken from batch

    assert batch.available_quantity == 18
    # will check to see if there is 18


def make_batch_and_line(sku, batch_qty, line_qty):
    # create a entry for Batch and Line
    return (
        Batch("batch-001", sku, batch_qty, eta=date.today()),
        OrderLine("order-123", sku, line_qty),
    )
# given SKU, will create two list one for Orderline and one for Batch


def test_can_allocate_if_available_greater_than_required():
    # testing to see if allocation works when available inventory is more than required
    large_batch, small_line = make_batch_and_line("ELEGANT-LAMP", 20, 2)
    assert large_batch.can_allocate(small_line)
    # checks to see if the large_batch instance can allocate any quantity less than or equal to that in small_line


def test_cannot_allocate_if_available_smaller_than_required():
    # testing to see that allocation should not work when inventory less than requried
    small_batch, large_line = make_batch_and_line("ELEGANT-LAMP", 2, 20)
    assert small_batch.can_allocate(large_line) is False
    # testing that a batch of 2 lamps cannot be allocated if the order line has more than 20.


def test_can_allocate_if_available_equal_to_required():
    # testing to see allocaiton will work when inventory equals required
    batch, line = make_batch_and_line("ELEGANT-LAMP", 2, 2)
    assert batch.can_allocate(line)


def test_cannot_allocate_if_skus_do_not_match():
    # testing to see that allocation should not work when skus don't match
    batch = Batch("batch-001", "UNCOMFORTABLE-CHAIR", 100, eta=None)
    different_sku_line = OrderLine("order-123", "EXPENSIVE-TOASTER", 10)
    assert batch.can_allocate(different_sku_line) is False
    # asserts that the batch cannot allocate this order line because they do not match


def test_allocation_is_idempotent():
    # testing that the allocation of an order line is will be the same
    batch, line = make_batch_and_line("ANGULAR-DESK", 20, 2)
    batch.allocate(line)
    assert batch.available_quantity == 18
    # assert checks that there are 18 available units in the batch


def test_deallocate():
    # testing that batch can be allocated and deallocated
    batch, line = make_batch_and_line("EXPENSIVE-FOOTSTOOL", 20, 2)
    batch.allocate(line)
    batch.deallocate(line)
    assert batch.available_quantity == 20
    # assert statement verifies that there are 20 items in the available quantity


def test_can_only_deallocate_allocated_lines():
    # testing that batch can only be deallocated when there are no more allocated lines.
    batch, unallocated_line = make_batch_and_line("DECORATIVE-TRINKET", 20, 2)
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 20
    # assert statement verifies that there are 20 items in the available quantity
