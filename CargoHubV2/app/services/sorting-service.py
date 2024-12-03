from sqlalchemy.orm import Query
from sqlalchemy.exc import SQLAlchemyError

def apply_sorting(query: Query, model, sort_by: str = "id", order: str = "asc") -> Query:
    """
    Apply sorting to a SQLAlchemy query.

    :param query: SQLAlchemy query object.
    :param model: The SQLAlchemy model to validate attributes.
    :param sort_by: The column name to sort by (default is "id").
    :param order: Sorting order, "asc" for ascending or "desc" for descending.
    :return: A sorted SQLAlchemy query.
    """
    try:
        # Validate that the column exists in the model
        if not hasattr(model, sort_by):
            raise ValueError(f"Invalid sort attribute: {sort_by}")

        # Get the column from the model
        column = getattr(model, sort_by)

        # Apply sorting order
        if order == "desc":
            return query.order_by(column.desc())
        return query.order_by(column.asc())
    except SQLAlchemyError as e:
        raise ValueError(f"Error applying sorting: {str(e)}")
