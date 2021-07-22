import os

def clear_path(path):
    for p in os.listdir(path):
        p = os.path.join(path, p)
        if os.path.isfile(p):
            os.remove(p)
        else:
            try:
                os.rmdir(p)
            except OSError as e:
                clear_path(p)
                os.rmdir(p)