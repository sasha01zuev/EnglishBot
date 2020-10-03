from aiogram.utils.callback_data import CallbackData

settings_callback = CallbackData("settings", "settings_item", "setting_choose")
delete_translate_callback = CallbackData('delete_translate', 'item')
confirm_callback = CallbackData('accept_or_cancel', 'item')
select_dictionary_callback = CallbackData('select_dict', 'dictionary_id', 'dictionary_name')
select_translate_callback = CallbackData('select_word', 'dictionary_id', 'english_word', 'russian_word')
