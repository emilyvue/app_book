from datetime import date, timedelta
# allow us to work with dates
import pytest
# will allow us to run test
from model import allocate, OrderLine, Batch, OutOfStock
# imports certain fuctions from our model.py


today = date.today()
# will return todays date
tomorrow = today + timedelta(days=1)
# will add 2 days to todays
later = tomorrow + timedelta(days=10)
# will add 10 days to today


def test_prefers_current_stock_batches_to_shipments():
    # test to ensure that the current stock batches are preferred over shipments
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)
    line = OrderLine("oref", "RETRO-CLOCK", 10)

    allocate(line, [in_stock_batch, shipment_batch])
    # both are allocated to Orderline
    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100
    # assert checks the available quantity of each batch matches their quantity.


def test_prefers_earlier_batches():
    # tests the preference of batches by comparing their available_quantity.
    earliest = Batch("speedy-batch", "MINIMALIST-SPOON", 100, eta=today)
    medium = Batch("normal-batch", "MINIMALIST-SPOON", 100, eta=tomorrow)
    latest = Batch("slow-batch", "MINIMALIST-SPOON", 100, eta=later)
    line = OrderLine("order1", "MINIMALIST-SPOON", 10)

    allocate(line, [medium, earliest, latest])
    # they batches are allocated to Orderline

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100
    # assert checks the available quanity of each preference


def test_returns_allocated_batch_ref():
 # testing that the allocation of an Orderline is equal to the reference for a batch.
    in_stock_batch = Batch("in-stock-batch-ref",
                           "HIGHBROW-POSTER", 100, eta=None)
    shipment_batch = Batch("shipment-batch-ref",
                           "HIGHBROW-POSTER", 100, eta=tomorrow)
    line = OrderLine("oref", "HIGHBROW-POSTER", 10)

    allocation = allocate(line, [in_stock_batch, shipment_batch])
    # they batches are allocated to Orderline

    assert allocation == in_stock_batch.reference
    # assert checks the allocation equals in stock


def test_raises_out_of_stock_exception_if_cannot_allocate():
    # testing out of stock exeptions
    batch = Batch("batch1", "SMALL-FORK", 10, eta=today)
    allocate(OrderLine("order1", "SMALL-FORK", 10), [batch])

    with pytest.raises(OutOfStock, match="SMALL-FORK"):
        allocate(OrderLine("order2", "SMALL-FORK", 1), [batch])
    # OutOfStock exception is raised when trying to allocate another OrderLine with order2 using this same batch.
