class Scripts(object):
    START_TXT = "Hey, I'm your group management bot! I monitor messages for explicit abusive language."
    WARN_TXT = "{mention}, your message was deleted for containing explicit abusive language. Keep it respectful!"
    LINK_DELETE_TXT = "{mention}, links are not allowed in this group."
    UNAUTHORIZED_GROUP_TXT = "🚫 Sorry, this bot is not authorized to work for you.\n\nDeploy your own instance if needed."
    USER_INFO_TXT = (
        "<b>User Info:</b>\n"
        "<b>ID:</b> {id}\n"
        "<b>First Name:</b> {first_name}\n"
        "<b>Username:</b> {username}\n"
        "<b>User Link:</b> {link}\n"
        "<b>DC:</b> {dc}\n"
        "<b>Premium Status:</b> {premium}"
    )
    SELF_ID_TXT = "Your ID: <code>{id}</code>"
    USER_ID_TXT = "{mention}'s ID is <code>{id}</code>"
    CHAT_ID_TXT = "This Chat ID is: <code>{id}</code>"
    FORWARDED_CHANNEL_ID_TXT = "{mention}'s ID is <code>{user_id}</code>.\nThe forwarded channel, {channel_title}, has an ID <code>{channel_id}</code>."
