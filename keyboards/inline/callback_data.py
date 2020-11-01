from aiogram.utils.callback_data import CallbackData

settings_callback = CallbackData("settings", "settings_item")

delete_translate_callback = CallbackData('delete_translate', 'item')
delete_dictionary_callback = CallbackData('delete_dictionary', 'item')

select_dictionary_callback = CallbackData('select_dict', 'dictionary_id', 'dictionary_name')
select_translate_callback = CallbackData('select_word', 'dictionary_id', 'english_word', 'russian_word')

confirm_callback = CallbackData('accept_or_cancel', 'item')
cancel_button_callback = CallbackData('cancel_btn', 'state')

select_language_callback = CallbackData('select_lang', 'lang')

add_translate_callback = CallbackData('add_translate', 'is_selected')
repeat_translate_callback = CallbackData('repeat_translate', 'is_selected')
learn_remaining_callback = CallbackData('learn_remaining', 'is_selected')
