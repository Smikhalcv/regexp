import re
import csv

# Ваша задача: починить адресную книгу, используя регулярные выражения.
# Структура данных будет всегда:
# lastname,firstname,surname,organization,position,phone,email
# Предполагается, что телефон и e-mail у человека может быть только один.
# Необходимо:
#
# поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно. В записной книжке изначально может быть Ф + ИО, ФИО, а может быть сразу правильно: Ф+И+О;
# привести все телефоны в формат +7(999)999-99-99. Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999;
# объединить все дублирующиеся записи о человеке в одну.

from pprint import pprint

# читаем адресную книгу в формате CSV в список contacts_list

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


# TODO 1: выполните пункты 1-3 ДЗ
# ваш код

def str_text(contact_list):
    '''Преобразует список в строку, для работы regexp'''
    list_text = contacts_list[1:]
    text = str()
    for line in list_text:
        text += ' '.join(line) + ' '
    return text


def unic_full_name():
    '''По средствам regexp создаёт список уникальных полных имён контактов,
    с поправкой, что нет полных тёсок и встречается полностью имя'''
    pattern_fname_lname = re.compile(r'([А-ЯЁ][а-яё]+)\s+([А-ЯЁ][а-яё]+)\s+([А-ЯЁ][а-яё]+)?')
    list_fname_lname = re.findall(pattern_fname_lname, str_text(contacts_list))
    list_fname_lname = list(set(list_fname_lname))
    list_full_name = []
    for i in list_fname_lname:
        if i[2]:
            list_full_name.append(i)
    return list_full_name


# Функции по изменению в тексте
def fix_text_name():
    '''Функция находит по шаблону имя фамилия отчество и подставляет перед ними firstname, lastname и surname
    (перед firstname ставится ; для упрощения дальнейшего разделения)'''
    pattern_name = re.compile(r'([А-ЯЁ][а-яё]+)\s+([А-ЯЁ][а-яё]+)\s+([А-ЯЁ][а-яё]+)?')
    new_pattern_name = r'; firstname: \1, lastname: \2, surname: \3, '
    text_1 = pattern_name.sub(new_pattern_name, str_text(contacts_list))
    text_1 = text_1[2:]  # обрезает первую ;
    return text_1


def fix_phone():
    '''Функция находит по шаблону номера телефонов вместе дополнительными
    и преобразует их в соответстии с заданием'''
    pattern_tel = re.compile(r'(\+?[7|8]\s*\(?(\d{3})\)?[\s*|\-*]?(\d{3})\-?(\d{2})\-?(\d{2}))((\s+\(?(доб\.)\s(\d{4})\)?)?)')
    fix_pattern_tel = r'phone: +7(\2)\3-\4-\5 \8\9,'
    fix_tel_text = pattern_tel.sub(fix_pattern_tel, fix_text_name())
    return fix_tel_text


def fix_email():
    '''Функция находит email и преобразует'''
    pattern_email = re.compile(r'(\S+@\w+\.\w{2,3})')
    new_pattern_email = r'email: \1,'
    fix_email_text = pattern_email.sub(new_pattern_email, fix_phone())
    return fix_email_text


def fix_organization():
    '''Функция преобразует название организации'''
    pattern_organization = re.compile('(ФНС|Минфин)')
    new_pattern_organization = r'organization: \1,'
    fix_org_text = pattern_organization.sub(new_pattern_organization, fix_email())
    return fix_org_text


def fix_position_1():
    '''Не смог подобрать один шаблон под должности, поэтому нахожу их по отдельности'''
    pattern_position_1 = re.compile('(\w+\s\w+\s\W\s\w+\s\w+\s\w+\s\w\s\w+\s\w+\s\w+\s\w+\s\w+\s\w+\s\w\s\w+\s\w+\s\w+)')
    new_pattern_position_1 = r'position: \1,'
    fix_pos_text_1 = pattern_position_1.sub(new_pattern_position_1, fix_organization())
    return fix_pos_text_1


def fix_position_2():
    '''Находит второую позицию'''
    pattern_position_2 = re.compile('([a-яё]+\s\w+\s[А-ЯЁ]\w+\s\w+\s[А-ЯЁ]\w+\s\w+\s\w+)')
    new_pattern_position_2 = r'position: \1,'
    fix_pos_text_2 = pattern_position_2.sub(new_pattern_position_2, fix_position_1())
    return fix_pos_text_2


def fix_text():
    '''Функция разделяет текст на список через ';', которые установили в начале
    Итерируется по списку уникальных имён, с которых и начинает новый список
    После чего итерируется по отсекает ФИО от неё, уберает из отстатка пустые места
    и добвыляет к новому списку'''
    list_text = fix_position_2().split(';')
    phone_book = []
    i = 0
    for man in unic_full_name():
        phone_book.append(f'firstname: {man[0]},lastname: {man[1]},surname: {man[2]}'.split(','))
        for contact in list_text:
            if man[0] in contact.split()[1]:
                pazzle = contact.split(',')[3:]
                for element in pazzle:
                    if element.strip():
                        if element.strip() not in phone_book[i]:
                            phone_book[i].append(element.strip())
        i += 1
    return phone_book


if __name__ in '__main__':

    for i in fix_text():
        print(i)

    # TODO 2: сохраните получившиеся данные в другой файл
    # код для записи файла в формате CSV
    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        # Вместо contacts_list подставьте свой список
        datawriter.writerows(fix_text())
