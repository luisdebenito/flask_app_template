from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.orm import with_loader_criteria
from sqlalchemy.orm.mapper import Mapper

db = SQLAlchemy()


# this will be executed on every query, to avoid active=False  
# (soft deleted) records being queried, relatively fast
@event.listens_for(db.session, "do_orm_execute")
def add_global_active_filter(execute_state):
    mappers: list[Mapper] = list(db.Model.registry.mappers)
    criteria = []
    for mapper in mappers:
        _mappedClass = mapper.class_
        if not hasattr(_mappedClass, "active"):
            continue
        criteria.append(
            with_loader_criteria(
                _mappedClass,
                lambda cls: cls.active.is_(True),
                include_aliases=True,
            )
        )
    execute_state.statement = execute_state.statement.options(*criteria)