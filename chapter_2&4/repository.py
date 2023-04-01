import abc
# to use the abc framework
import model


class AbstractRepository(abc.ABC):
    # abstraction over persistent storage
    @abc.abstractmethod
    def add(self, batch: model.Batch):
        #  put a new item in the repository
        raise NotImplementedError
        # code is not implemented then raises an error.

    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        # return a previously added item
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session
    # initializes the session

    def add(self, batch):
        self.session.add(batch)
    # adds batches to the database

    def get(self, reference):
        return self.session.query(model.Batch).filter_by(reference=reference).one()
    # returns one batch from database

    def list(self):
        return self.session.query(model.Batch).all()
    # returns all batches in the database

# should copy Fake Repository ??
