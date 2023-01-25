from aiogram import executor

import modules
from loader import dp

if __name__ == '__main__':
    print("TELEGRAM AUTH BOT IS WORK")
    executor.start_polling(dp)
