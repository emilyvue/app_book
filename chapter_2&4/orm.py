from sqlalchemy import Table, MetaData, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import registry, relationship

import model

# https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#imperative-mapping
# using SQLAlchemy 2.0-style imperative mapping
mapper_registry = registry()
# mapper_registry is created and registered with the registry() function
# metadata = MetaData()

order_lines = Table(
    "order_lines",
    mapper_registry.metadata,
    # maintaining a collection of mappings in metadate
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("orderid", String(255)),
)  # code creates a table order_lines with defined columns to store orders

batches = Table(
    "batches",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255)),
    Column("sku", String(255)),
    Column("_purchased_quantity", Integer, nullable=False),
    Column("eta", Date, nullable=True),
)  # code creates a table batch with defined columns to store batches

allocations = Table(
    "allocations",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderline_id", ForeignKey("order_lines.id")),
    Column("batch_id", ForeignKey("batches.id")),
)  # code creates a table allocaitons with defined columns to store the transactions between the two tabels


def start_mappers():
    lines_mapper = mapper_registry.map_imperatively(
        model.OrderLine, order_lines)
    mapper_registry.map_imperatively(
        model.Batch,
        batches,
        properties={
            "_allocations": relationship(
                lines_mapper,
                secondary=allocations,
                collection_class=set,
            )
        },
    )  # map the primary key for a OrderLine to another Batch
    # sets its properties to include all allocations from line_mappers
