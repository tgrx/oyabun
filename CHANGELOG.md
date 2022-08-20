# CHANGELOG

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
