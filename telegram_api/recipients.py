from utility import config
import functions.function_definitions as func_defs


def find_recipient(chat_id=None, name=None):
    list_of_recipients = config.retrieve_config("telegram_recipients")
    if not list_of_recipients:
        return None
    for sub in list_of_recipients:
        if (chat_id and str(sub["chat_id"]) == str(chat_id)) or (
            name and sub["name"] == name
        ):
            return sub
    return None


def find_recipients(chat_ids=None, names=None):
    list_of_recipients = config.retrieve_config("telegram_recipients")

    if not list_of_recipients:
        return []
    if func_defs.placeholder_all in chat_ids or func_defs.placeholder_all in names:
        return list_of_recipients

    result = []
    for sub in list_of_recipients:
        if sub not in result:
            chat_id_found = chat_ids and str(sub["chat_id"]) in [
                str(id) for id in chat_ids
            ]
            if chat_id_found:
                result.append(sub)
            else:
                name_found = names and str(sub["name"]) in names
                if name_found:
                    result.append(sub)

    return result


def parse_recipient_array(recipient_array):
    return [item.split(":")[1] if ":" in item else item for item in recipient_array]
