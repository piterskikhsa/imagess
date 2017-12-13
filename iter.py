def find_zero(tuple):
    for _ in tuple:
        if len(_)>3 and _[3]==0:
            return True
        else:
            continue
    return False