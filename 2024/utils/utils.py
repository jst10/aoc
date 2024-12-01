
def read_file_content(file_path:str) -> list[str]:
    with open(file_path, 'r') as file:
        for line in file:
            ls=line.strip().rstrip('\n')
            if not ls:
                continue
            yield ls
