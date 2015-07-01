# -*- coding: utf-8 -*-
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import ClauseElement


def get_or_create(session, model, **kwargs):
    """Get or create a record in the database."""
    try:
        query = session.query(model).filter_by(**kwargs)
        instance = query.first()

        if instance:
            return instance, False

        else:
            session.begin(nested=True)
            try:
                params = dict((key, value) for key, value in kwargs.iteritems()
                              if not isinstance(value, ClauseElement))
                instance = model(**params)
                session.add(instance)
                session.commit()
                return instance, True
            except IntegrityError as error:
                session.rollback()
                instance = query.one()
                return instance, False

    except Exception as exception:
        raise exception
