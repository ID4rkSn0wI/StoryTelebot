# from handlers.custom_heandlers import lowprice
# from handlers.custom_heandlers import highprice
# from handlers.custom_heandlers import bestdeal
# from utils.misc.show_hotels import send_hotel
# from database.database import User, db
# from loguru import logger
#
#
# @logger.catch
# def path(message):
#     """
#     Данная функция-переадресовщик
#     Она перенаправляет аргументы в нужные функции
#     """
#     with db:
#         user = User.get(telegram_id=message.chat.id)
#         if user.callback == 'lowprice':
#             user.callback = ''
#             user.keyboard = ''
#             user.save()
#             lowprice.find_lowprice(message)
#         elif user.call == 'lowprice':
#             user.call = ''
#             user.save()
#             lowprice.handle_text(message)
#         elif user.callback == 'highprice':
#             user.callback = ''
#             user.keyboard = ''
#             user.save()
#             highprice.find_highprice(message)
#         elif user.call == 'highprice':
#             user.call = ''
#             user.save()
#             highprice.handle_text(message)
#         elif user.callback == 'bestdeal':
#             user.callback = ''
#             user.keyboard = ''
#             user.save()
#             bestdeal.find_bestdeal(message)
#         elif user.call == 'bestdeal':
#             user.call = ''
#             user.save()
#             bestdeal.handle_text(message)
#         elif user.call_hotels != '':
#             send_hotel(message)
