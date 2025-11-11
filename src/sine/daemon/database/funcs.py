from sqlalchemy import select


def get_all_by_titles(session, model, titles: list[str]):
        query = select(model) \
            .where(model.title.in_(titles))
        for obj in session.scalars(query).unique().yield_per(10):
            yield obj


OPERATORS = {
    "eq": lambda col, val: col == val,
    "ne": lambda col, val: col != val,
    "gt": lambda col, val: col > val,
    "lt": lambda col, val: col < val,
    "ge": lambda col, val: col >= val,
    "le": lambda col, val: col <= val,
    "contains": lambda col, val: col.like(f"%{val}%"),
    "icontains": lambda col, val: col.ilike(f"%{val}%"),
    "in": lambda col, val: col.in_(val if isinstance(val, list) else [val]),
}

def apply_filters(query, model, filters: dict):
    simple_kwargs = {}
    complex_expressions = []

    for key, value in filters.items():
        if "__" in key:
            field, op = key.split("__", 1)
            if not hasattr(model, field):
                continue
            column = getattr(model, field)
            if op in OPERATORS:
                expr = OPERATORS[op](column, value)
                complex_expressions.append(expr)
        else:
            simple_kwargs[key] = value

    if simple_kwargs:
        query = query.filter_by(**simple_kwargs)

    if complex_expressions:
        query = query.filter(*complex_expressions)

    return query

