from __future__ import annotations

class NotFoundError(Exception):
    pass

class UniqueError(Exception):

    def __init__(self, scores: tuple[float, float], *args, **kwargs):
        self.scores = scores
        super().__init__(*args, **kwargs)

class HttpError(Exception):
    pass