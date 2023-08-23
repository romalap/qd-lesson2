

def read_file(filename: str) -> List[str]:
    """ Read file """
    with open(filename, 'r', encoding="utf8") as f:
        return f.readlines()
