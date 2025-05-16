from enum import Enum, auto

class ViewType(Enum):
    DESCRIPTIVE_LIST_VIEW = auto()
    GRID_VIEW = auto()
    TEXT_AND_IMAGE_LIST_VIEW = auto()
    TEXT_LIST_VIEW = auto()
    POPUP_TEXT_LIST_VIEW = auto()

def get_next_view_type(current_view_type: ViewType, direction: int, exclude: list[ViewType] = [ViewType.POPUP_TEXT_LIST_VIEW]) -> ViewType:
    exclude = exclude or []

    # Build the filtered list of allowed view types
    view_types = [vt for vt in ViewType if vt not in exclude]

    if current_view_type not in view_types:
        raise ValueError(f"Current view type {current_view_type} is excluded or invalid.")

    current_index = view_types.index(current_view_type)
    next_index = (current_index + direction) % len(view_types)
    return view_types[next_index]