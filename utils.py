def paginate(limit: int, offset: int, total: int):
    return {
        "next": str(offset + limit) if offset + limit < total else None,
        "limit": limit,
        "previous": str(offset - limit) if offset > 0 else None
    }
