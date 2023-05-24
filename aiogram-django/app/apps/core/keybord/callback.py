from aiogram.filters.callback_data import CallbackData


class ExportCallback(CallbackData, prefix="export"):
    report: str
    label: str
    chat_id: str
    # prefix_file: str


class CancelCallback(CallbackData, prefix="cancel"):
    action: str
