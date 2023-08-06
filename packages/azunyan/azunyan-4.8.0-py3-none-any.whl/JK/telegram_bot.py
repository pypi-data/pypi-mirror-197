from functools import wraps


def chat_action(action: str):
    """
    Decorator that sends `action` while processing func command.

    e.g.,

    ```python
    @chat_action(ChatAction.TYPING)
    async def func...

    @chat_action(ChatAction.UPLOAD_VIDEO)
    async def func...
    ```

    - `action` str\n
        - `ChatAction.TYPING`. See `telegram.constants.ChatAction` for more.
    """

    def decorator(func):
        @wraps(func)
        async def command_func(update, context, *args, **kwargs):
            await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return await func(update, context,  *args, **kwargs)
        return command_func

    return decorator
