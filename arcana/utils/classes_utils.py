


def validate_classes_names(name_1: str | list[str], name_2: str | list[str]):
    if isinstance(name_1, str):
        name_1 = [name_1]
    if isinstance(name_2, str):
        name_2 = name_2

    if not all(name1 in name_2 for name1 in name_1):
        for name1 in name_1:
            for name2 in name_2:
                if name1 != name2:
                    raise ValueError(f"{name1} != {name2}. Classes should have the same prefix.")
