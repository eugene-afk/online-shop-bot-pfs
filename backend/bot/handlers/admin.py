from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types.message import ContentTypes
import io, json

from ..instance import dp, bot
from ..states.admin import ImportDocumentState
from ..services.products import ProductsService

@dp.message_handler(commands=['load_data'], is_admin=True)
async def import_json(message: types.Message):    
    await message.answer(text="Send json file with data.")
    await ImportDocumentState.import_document.set()

@dp.message_handler(content_types=ContentTypes.DOCUMENT, 
    state=ImportDocumentState.import_document, is_admin=True)
async def import_json(message: types.Message, state: FSMContext):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)    
    file_path = file.file_path
    if not ".json" in file_path.lower():
        await message.answer(text="Your file is not json extension!")
        return
        
    # In this case I'm loading the file to memory stream, but in cases with large files it should need a generator and loading by chunks
    result: io.BytesIO = await bot.download_file(file_path)
    data = json.loads(result.read().decode("utf-8"))
    service = ProductsService()
    res = await service.update_products_by_json(data)

    if res:
        await message.answer(text="Products successfully updated!")
    else:
        await message.answer(text="Error was occured! Try again later.")
    await state.finish()