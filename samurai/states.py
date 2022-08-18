import enum


@enum.unique
class State(enum.Enum):
    NOT_STARTED: str = ""
    WAIT_FOR_PLAIN_TEXT: str = "01"
    WAIT_FOR_EDITING_TEXT: str = "02"
    SEND_PHOTO: str = "03"
    WAIT_FOR_PHOTO: str = "04"
    FINISHED: str = "99"
