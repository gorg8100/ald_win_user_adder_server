class InfoRaise:
    def __init__(self, msg: str):
        self.msg = msg

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            raise RuntimeError(f"{self.msg}\n{type(exc_val).__name__}: {exc_val}")