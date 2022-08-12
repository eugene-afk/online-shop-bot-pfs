from aiogram.dispatcher.filters.state import State, StatesGroup

class ImportDocumentState(StatesGroup):
    import_document = State()