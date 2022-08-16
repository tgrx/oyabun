import enum


@enum.unique
class State(enum.Enum):
    UNKNOWN = ""
    S_WAIT_FOR_PLAIN_TEXT = "01"
    S_WAIT_FOR_EDITING_TEXT = "02"
    S_SEND_PHOTO = "03"
    S_04_PHOTO_TO_BOT = "04-photo-to-bot"
    FINISHED = "99-finished"
