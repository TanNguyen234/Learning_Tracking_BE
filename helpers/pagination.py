

def paginate(current_page: int, limit: int, total_items: int):
    total_pages = int(total_items / limit) if limit > 0 else 1
    offset = (current_page - 1) * limit

    return {
        "current_page": current_page,
        "limit": limit,
        "offset": offset,
        "total_pages": total_pages,
        "total_items": total_items
    }