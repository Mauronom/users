from enum import Enum


class ClueStatus(Enum):
    pending = "pending"
    investigating = "investigating"
    done = "done"
    error = "error"
    blacklisted = "blacklisted"


class ClueType(Enum):
    scout = "scout"
    entity = "entity"
    unknown = "unknown"


class Clue:
    def __init__(self, clue, status=ClueStatus.pending, type=ClueType.unknown,
                 score=5, source_clue="", times_returned=0, summary="", web=""):
        if not clue:
            raise ValueError("clue cannot be empty")
        if score < 0:
            raise ValueError("score cannot be negative")
        self.clue = clue
        self.status = status
        self.type = type
        self.score = score
        self.source_clue = source_clue
        self.times_returned = times_returned
        self.summary = summary
        self.web = web

    def clone(self):
        return Clue(self.clue, self.status, self.type, self.score, self.source_clue,
                    self.times_returned, self.summary, self.web)

    def __eq__(self, other):
        return self.clue == other.clue
