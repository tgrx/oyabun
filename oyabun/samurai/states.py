import enum


@enum.unique
class State(enum.Enum):
    NOT_STARTED = ""
    WAIT_FOR_PLAIN_TEXT = "01"
    WAIT_FOR_EDITING_TEXT = "02"
    SEND_PHOTO = "03"
    WAIT_FOR_PHOTO = "04"
    FINISHED = "99"
