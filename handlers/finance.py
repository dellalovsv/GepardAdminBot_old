import config
from bot import bot, dp
from db import finances
from funcs.decorators import check_admin_bot
from funcs import check_type, check_msg, dt
from texts import finance

from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


class NewFinance(StatesGroup):
    type_rec = State()
    summa = State()
    dsc = State()
    accept = State()


class ShowFinance(StatesGroup):
    all = State()
    begin = State()
    end = State()


# ------------------- Добавление записи --------------------------
@dp.message_handler(commands='new_finance')
@check_admin_bot
async def new_finance(m: Message):
    await bot.send_message(m.chat.id, finance.New.start)
    await bot.send_message(m.chat.id, finance.New.get_cancel)
    await bot.send_message(m.chat.id, finance.New.get_type)
    await NewFinance.type_rec.set()


@dp.message_handler(state=NewFinance.type_rec)
async def finance_get_type_rec(m: Message, state: FSMContext):
    answer = m.text.strip()
    if check_msg.check_cancel(answer) is False:
        if '/' in answer:
            answer = answer.replace('/', '').strip()
            if check_type.check_int(answer):
                await state.update_data(type_rec=answer)
                await bot.send_message(m.chat.id, finance.New.get_summa)
                await NewFinance.next()
            else:
                await bot.send_message(m.chat.id, finance.New.error_answer_type_rec)
                await NewFinance.type_rec.set()
        else:
            await bot.send_message(m.chat.id, finance.New.no_slash_in_msg)
            await NewFinance.type_rec.set()
    else:
        await bot.send_message(m.chat.id, finance.New.set_cancel)
        await state.finish()


@dp.message_handler(state=NewFinance.summa)
async def finance_get_summa(m: Message, state: FSMContext):
    answer = m.text.strip()
    if check_msg.check_cancel(answer) is False:
        if check_type.check_float(answer):
            await state.update_data(summa=float(answer))
            await bot.send_message(m.chat.id, finance.New.get_dsc)
            await NewFinance.next()
        else:
            await bot.send_message(m.chat.id, finance.New.error_answer_summa)
            await NewFinance.summa.set()
    else:
        await bot.send_message(m.chat.id, finance.New.set_cancel)
        await state.finish()


@dp.message_handler(state=NewFinance.dsc)
async def finance_get_dsc(m: Message, state: FSMContext):
    answer = m.text.strip()
    if check_msg.check_cancel(answer) is False:
        await state.update_data(dsc=answer)
        data = await state.get_data()
        await bot.send_message(m.chat.id, finance.New.check_data % (
            finance.New.type_rec[int(data['type_rec'])],
            "%.2f" % float(data['summa']),
            data['dsc']
        ))
        await NewFinance.next()
    else:
        await bot.send_message(m.chat.id, finance.New.set_cancel)
        await state.finish()


@dp.message_handler(state=NewFinance.accept)
async def finance_check_msg(m: Message, state: FSMContext):
    answer = m.text.strip()
    if check_msg.check_cancel(answer) is False:
        if answer == '/yes':
            data = await state.get_data()
            if finances.new(data['type_rec'], data['summa'], data['dsc']):
                await bot.send_message(m.chat.id, finance.New.success % "Добавление новой записи в финансы")
                await state.finish()
            else:
                await bot.send_message(m.chat.id, finance.New.error)
                await state.finish()
        else:
            await bot.send_message(m.chat.id, finance.New.check_data_error)
            await state.finish()
    else:
        await bot.send_message(m.chat.id, finance.New.set_cancel)
        await state.finish()


# -------------------- Показ записей -------------------------
@dp.message_handler(commands='show_finance')
@check_admin_bot
async def show_finance(m: Message):
    await bot.send_message(m.chat.id, finance.Show.start)
    await bot.send_message(m.chat.id, finance.cancel_msg)
    await ShowFinance.all.set()


@dp.message_handler(state=ShowFinance.all)
async def get_begin(m: Message, state: FSMContext):
    answer = m.text.strip()
    if check_msg.check_cancel(answer) is False:
        if answer == '/all':
            res = finances.show(True)
            if res is not None and len(res) > 0:
                res_msg = finance.Show.title_all
                dohod: float = 0
                rashod: float = 0
                for r in res:
                    if r['type'] == 1 or r['type'] == '1':
                        dohod += float(r['summa'])
                    if r['type'] == 2 or r['type'] == '2':
                        rashod += float(r['summa'])
                    r['date_add'] = dt.conv_date(str(r['date_add']))
                    r['type'] = finance.New.type_rec[int(r['type'])]
                    r['summa'] = "%.2f" % float(r['summa'])
                    res_msg += f'\n\n{finance.Show.msg % (r["date_add"], r["type"], r["summa"], r["dsc"])}'
                    if len(res_msg) > 3000:
                        await bot.send_message(m.chat.id, res_msg)
                if len(res_msg) > 0:
                    await bot.send_message(m.chat.id, res_msg)
                await bot.send_message(m.chat.id, finance.Show.summa_dohod_rashod % ("%.2f" % dohod,
                                                                                     "%.2f" % rashod,
                                                                                     "%.2f" % (dohod - rashod)))
            else:
                await bot.send_message(m.chat.id, finance.Show.records_not_found)
            await state.finish()
        elif answer == '/last_week':
            dates = dt.get_first_and_last_date_of_current_week()
            res = finances.show(False, dt.minus_days(1, dates[0]), dt.plus_days(1, dates[1]))
            if res is not None and len(res) > 0:
                res_msg = finance.Show.title_last_week % (dt.conv_date(dates[0]), dt.conv_date(dates[1]))
                dohod: float = 0
                rashod: float = 0
                for r in res:
                    if r['type'] == 1 or r['type'] == '1':
                        dohod += float(r['summa'])
                    if r['type'] == 2 or r['type'] == '2':
                        rashod += float(r['summa'])
                    r['date_add'] = dt.conv_date(str(r['date_add']))
                    r['type'] = finance.New.type_rec[int(r['type'])]
                    r['summa'] = "%.2f" % float(r['summa'])
                    res_msg += f'\n\n{finance.Show.msg % (r["date_add"], r["type"], r["summa"], r["dsc"])}'
                    if len(res_msg) > 3000:
                        await bot.send_message(m.chat.id, res_msg)
                if len(res_msg) > 0:
                    await bot.send_message(m.chat.id, res_msg)
                await bot.send_message(m.chat.id, finance.Show.summa_dohod_rashod % ("%.2f" % dohod,
                                                                                     "%.2f" % rashod,
                                                                                     "%.2f" % (dohod - rashod)))
            else:
                await bot.send_message(m.chat.id, finance.Show.records_not_found)
            await state.finish()
        elif answer == '/of_date':
            await bot.send_message(m.chat.id, finance.Show.get_begin_date)
            await ShowFinance.begin.set()
        else:
            await bot.send_message(m.chat.id, finance.Show.error_command)
            await bot.send_message(m.chat.id, finance.Show.start)
            await ShowFinance.all.set()
    else:
        # cancel
        await bot.send_message(m.chat.id, finance.Show.cancel_msg)
        await state.finish()


@dp.message_handler(state=ShowFinance.begin)
async def get_show_begin_date(m: Message, state: FSMContext):
    answer = m.text.strip()
    if check_msg.check_cancel(answer) is False:
        if '-' not in answer and '.' in answer:
            if dt.check_begin_date(answer):
                await state.update_data(begin=dt.conv_date(answer))
                await bot.send_message(m.chat.id, finance.Show.get_end_date)
                await ShowFinance.next()
            else:
                await bot.send_message(m.chat.id, finance.Show.error_date)
                await ShowFinance.begin.set()
        else:
            await bot.send_message(m.chat.id, finance.Show.error_type_date)
            await ShowFinance.begin.set()
    else:
        await bot.send_message(m.chat.id, finance.Show.cancel_msg)
        await state.finish()


@dp.message_handler(state=ShowFinance.end)
async def get_show_end_date(m: Message, state: FSMContext):
    answer = m.text.strip()
    if check_msg.check_cancel(answer) is False:
        if '-' not in answer and '.' in answer:
            await state.update_data(end=dt.conv_date(answer))
            data = await state.get_data()
            res = finances.show(False, dt.minus_days(1, data['begin']), dt.plus_days(1, data['end']))
            if res is not None and len(res) > 0:
                dohod: float = 0
                rashod: float = 0
                res_msg = finance.Show.title_of_date % (
                    dt.conv_date(data['begin']),
                    dt.conv_date(data['end'])
                )
                for r in res:
                    if r['type'] == '1' or r['type'] == 1:
                        dohod += float(r['summa'])
                    if r['type'] == '2' or r['type'] == 2:
                        rashod += float(r['summa'])
                    r['date_add'] = dt.conv_date(str(r['date_add']))
                    r['type'] = finance.New.type_rec[int(r['type'])]
                    r['summa'] = "%.2f" % float(r['summa'])
                    res_msg += f"\n\n{finance.Show.msg % (r['date_add'], r['type'], r['summa'], r['dsc'])}"
                    if len(res_msg) > 3000:
                        await bot.send_message(m.chat.id, res_msg)
                if len(res_msg) > 0:
                    await bot.send_message(m.chat.id, res_msg)
                await bot.send_message(m.chat.id, finance.Show.summa_dohod_rashod % (
                    "%.2f" % dohod,
                    "%.2f" % rashod,
                    "%.2f" % (dohod - rashod)
                ))
            await state.finish()
        else:
            await bot.send_message(m.chat.id, finance.Show.error_type_date)
            await ShowFinance.end.set()
    else:
        await bot.send_message(m.chat.id, finance.Show.cancel_msg)
        await state.finish()
