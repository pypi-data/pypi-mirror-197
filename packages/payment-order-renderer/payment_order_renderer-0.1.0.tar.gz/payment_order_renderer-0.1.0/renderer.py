from payment_order_renderer import create_pdf
from payment_order_renderer import PaymentOrder


def render_payment_order_file(data: dict, path: str) -> bytes:
    """
    data: словарь с данными
    path: путь до png изображения штампа

    Пример ожидаемого словаря:

    payment_order_dict = {
        'creation_date': '2021-07-21T00:00:00+05:00',
        'last_transaction_date': '2021-07-21',
        'document_date': '2021-07-21',
        'document_number': '6000',
        'priority': '5',
        'transaction_type_code': '01',
        'purpose': 'Оплата по договору (номер/дата) без НДС',
        'payer_kpp': '773601001',
        'payer_inn': '280267860010',
        'payer_name': 'ООО "БИОШАНЬ"',
        'payer_bank': 'ТОЧКА ПАО БАНКА "ФК ОТКРЫТИЕ"',
        'payer_bank_address': 'г. Москва',
        'side_recipient_inn': '7839443197',
        'side_recipient_bank': 'ПАО Сбербанк',
        'side_recipient_bank_address': 'г. Екатернибург',
        'side_recipient_name': 'Дядя Толик',
        'side_recipient_kpp': None,
        'transaction_sum': '1488.23',
        'payer_account': '40702810401500014770',
        'payer_bank_code': '044525999',
        'payer_cr_account': '30101810845250000999',
        'side_recipient_bank_code': '044525593',
        'side_recipient_account': '42306810963160914857',
        'side_recipient_cr_account': '30101810845250000999',
        'finance_administrator_name': 'А.В. Прокопчук',
    }

    """
 
    payment_order = PaymentOrder(**data)

    return bytes(create_pdf(payment_order, path))
