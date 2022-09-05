from collections import UserDict
from datetime import datetime
import re
from pprint import pprint
from random import randint


class Field:
    def __init__(self, value: str) -> None:
        self.__value = None
        self.value = value

    def __repr__(self) -> str:
        return self.value

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value: str) -> None:
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        phone = "".join(re.findall(r"\d+", value))
        if len(phone) == 10:
            phone = "+38" + phone
        elif len(phone) == 12:
            phone = "+" + phone
        else:
            raise ValueError(f"Phone number '{value}' entered incorrectly")
        Field.value.fset(self, phone)


class Birthday(Field):
    def __init__(self, value: str) -> None:
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if value != "":
            try:
                datetime.strptime(value, "%d.%m.%Y")
                Field.value.fset(self, value)
            except ValueError:
                raise ValueError(
                    f"The date '{value}' does not match the format 'DD .MM .YYYY'")


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None) -> None:
        self.name: Name = name
        self.phone: list[Phone] = [phone] if phone else []
        self.birthday: Birthday = birthday

    def __repr__(self) -> str:
        return f"{self.name.value} phones : {', '.join(phone.value for phone in self.phone)}\
        \n{self.name} birthday : {self.birthday}"

    def days_to_birthday(self):
        if self.birthday == None:
            return "Birthday not specified."
        birthday: datetime = datetime.strptime(self.birthday.value, "%d.%m.%Y")
        day_now = datetime.now().date()
        day_birthday = birthday.replace(year=datetime.now().year).date()
        if day_birthday < day_now:
            day_birthday = birthday.replace(
                year=(datetime.now().year+1)).date()
        return f"{self.name.value}: {(day_birthday - day_now).days} days until next birthday"

    def add_phone(self, *phone: Phone) -> None:
        self.phone.extend(phone)

    def change_phone(self, old_phone: Phone, new_phone: Phone) -> None:
        for phone in self.phone:
            if phone.value == old_phone.value:
                phone.value = new_phone.value
                return
        print(f"Phone number '{old_phone.value}' does not exist!")

    def remuve_phone(self, phone_remuve: Phone) -> None:
        for phone in self.phone:
            if phone.value == phone_remuve.value:
                self.phone.remove(phone)
                return
        print(f"Phone number '{phone_remuve.value}' does not exist!")


class AddressBook(UserDict):
    data: dict[str, Record] = {}
    quantity = 4
    count = 0
    index_count = 0

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def __iter__(self):
        return self

    def __next__(self):
        self.count += 1
        len_data = len(self.data)
        max_count = (len_data // self.quantity + 1) \
            if (len_data % self.quantity) else (len_data // self.quantity)
        if self.count > max_count:
            raise StopIteration
        else:
            data_list = list(self.data.items())
            start_index = self.index_count
            end_index = start_index + self.quantity
            if (len_data - end_index) > 0:
                to_return = data_list[start_index:(end_index)]
            else:
                to_return = data_list[start_index:]
        self.index_count = end_index
        return to_return


if __name__ == "__main__":
    def phone_rand():
        return "".join([str(randint(0, 9)) for _ in range(10)])

    def name_rand():
        return "".join([chr(randint(ord("a"), ord("z"))) for i in range(6)]).title()

    book = AddressBook()
    for i in range(6):
        record = Record(Name((str(i+1)+"_"+name_rand())), phone=Phone(
            phone_rand()), birthday=Birthday("30.09.1999"))
        record.add_phone(Phone(phone_rand()), Phone(phone_rand()))
        book.add_record(record)

    gen = iter(book)
    pprint(next(gen))
    pprint("=================================================================")
    pprint(next(gen))
    pprint("=================================================================")
    pprint(next(gen))
