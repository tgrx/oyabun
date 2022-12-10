# CHANGELOG

---

## 2022.12.12

Partial support for [Telegram Bot API 6.3](https://core.telegram.org/bots/api#november-5-2022)

### Added

#### Methods

- deleteMessage

#### Entities

##### Chat

- active_usernames
- emoji_status_custom_emoji_id
- is_forum

##### Message

- author_signature
- forward_date
- forward_from
- forward_from_chat
- forward_from_message_id
- forward_sender_name
- forward_signature
- has_protected_content
- is_automatic_forward
- is_topic_message
- left_chat_member
- media_group_id
- message_thread_id
- new_chat_members
- new_chat_photo
- new_chat_title
- sender_chat
- via_bot

#### Requests and Responses models

##### Requests

- DeleteMessageRequest

##### Responses

- DeleteMessageResponse

---

## 2022.08.20

### Compatibility break-ups

- Product is renamed to `oyabun`;
- Python supported: >=3.10;
- Development on Windows is not supported;
- [CalVer](https://calver.org/) versioning schema is using from now;
- `aiohttp` is used as a backend for bot;
- `orjson` is used as a backend for JSON operations;
- Long copy-pasted docs are removed;
- Poetry is used;
- Pyenv is used;

### Added

#### Tools

- Samurai: a test bot usage app.

#### Bot

- answerCallbackQuery
- editMessageCaption
- editMessageReplyMarkup
- editMessageText
- getChat
- getUpdates

#### Entities models

- Audio
- CallbackQuery
- ChatLocation
- ChatPermissions
- ChatPhoto
- Dice
- Document
- Location
- MaskPosition
- PhotoSize
- Sticker
- Video
- VideoNote
- Voice

#### Requests and Responses models

##### Requests

- AnswerCallbackQueryRequest
- EditMessageCaptionRequest
- EditMessageReplyMarkupRequest
- EditMessageTextRequest
- GetChatRequest
- GetUpdatesRequest

##### Responses

- AnswerCallbackQueryResponse
- EditMessageCaptionResponse
- EditMessageReplyMarkupResponse
- EditMessageTextResponse
- GetChatResponse
- GetUpdatesResponse


## [0.0.1] - 2021-10-03

### Added

#### Entities models
- [Chat](https://core.telegram.org/bots/api#chat)
- [ForceReply](https://core.telegram.org/bots/api#forcereply)
- [InlineKeyboardButton](https://core.telegram.org/bots/api#inlinekeyboardbutton)
- [InlineKeyboardMarkup](https://core.telegram.org/bots/api#inlinekeyboardmarkup)
- [KeyboardButton](https://core.telegram.org/bots/api#keyboardbutton)
- [Message](https://core.telegram.org/bots/api#message)
- [MessageEntity](https://core.telegram.org/bots/api#messageentity)
- [ReplyKeyboardMarkup](https://core.telegram.org/bots/api#replykeyboardmarkup)
- [ReplyKeyboardRemove](https://core.telegram.org/bots/api#replykeyboardremove)
- [Update](https://core.telegram.org/bots/api#update)
- [User](https://core.telegram.org/bots/api#user)
- [WebhookInfo](https://core.telegram.org/bots/api#webhookinfo)

#### Requests and Responses models

##### Requests
- [SendMessageRequest](https://core.telegram.org/bots/api#sendmessage)

##### Responses
- [GetMeResponse](https://core.telegram.org/bots/api#getme)
- [GetWebhookInfoResponse](https://core.telegram.org/bots/api#getwebhookinfo)
- [SendMessageResponse](https://core.telegram.org/bots/api#sendmessage)
- [SetWebhookResponse](https://core.telegram.org/bots/api#setwebhook)
