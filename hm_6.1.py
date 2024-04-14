from collections import UserDict
import re

class WrongRecord(Exception):
    def __init__(self, message="No such record in address book"):
        self.message = message
        super().__init__(self.message)

class WrongPhone(Exception):
    def __init__(self, message="Error in phone"):
        self.message = message
        super().__init__(self.message)

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
		pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.is_phone = self.check_phone()
  
    def check_phone(self):
        pattern = r'^\d\s?(\d{3}\s?){2}\d{3}$'
        return bool(re.match(pattern, self.value))

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def find_phone(self, phone_str:str)-> Phone:
        return next((phone for phone in self.phones if phone.value == phone_str), None)
    
    def add_phone(self, phone_str:str):
        try:
            phone_to_add = Phone(phone_str)          
            if not phone_to_add.is_phone:
                raise WrongPhone (f"Phone {phone_str} must have 10 digits!")
            elif phone_to_add in self.phones:
                raise WrongPhone (f"Phone {phone_str} already exist in this record!")
            else:
                self.phones.append(phone_to_add)
        except Exception as ex:
                print(ex)


    def remove_phone(self, phone_str: str):
        try:
            phone_to_del = self.find_phone(phone_str)
            if phone_to_del:
                self.phones.remove(phone_to_del)
            else:
                raise WrongPhone (f"No such phone {phone_str} in record!")
        except Exception as ex:
            print(ex)
    
    def edit_phone(self, old_phone_str:str, new_phone_str:str):
        try:
            old_phone = self.find_phone(old_phone_str)
            new_phone = Phone(new_phone_str)
            if old_phone and new_phone.is_phone:
                i = self.phones.index(old_phone)
                self.phones[i] = new_phone
            else:
                raise WrongPhone (f"Can't change phone {old_phone}. It's not in records, or {new_phone} not a phone")
        except Exception as ex:
                print(ex)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    record_count = 0
    
    def __init__(self, name:str):
        self.name = Name(name)
        self.data = []
     
    def find(self, record_name: str) -> Record:
        return next((rec for rec in self.data if rec.name.value == record_name), None)
        
    def add_record(self, record:Record):
        try:
            if not self.find(record.name):
                self.data.append(record)
                self.record_count +=1                               
            else:
                raise WrongRecord(f"Record {record} already exist in phonebook {self.name}")
        except Exception as ex:
                print(ex)

    def delete(self, rec_name: str):
        try:
            record = self.find(rec_name)
            if record:
                self.data.remove(record)                
                self.record_count -=1
            else:
                raise WrongRecord(f"No such record {record} in phonebook {self.name}")
        except Exception as ex:
                print(ex)

    def __str__(self):
        message = f"Adress Book name is {self.name.value}.\nContacts: \n"
        for record in self.data:
                message += f"{record}\n"
        return message

def main():
    book = AddressBook("FirstBook")

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("1231231231")
    john_record.add_phone("123456")
    john_record.add_phone("123456789123")
    john_record.add_phone("12345678912")
    john_record.add_phone("1234567891")
    print(f"adding numbers to John, {john_record}")
    john_record.remove_phone("1234567891")
    print(f"deleting phone 1234567891 {john_record}")

    book.add_record(john_record)
    jane_record = Record("Jane")
    jane_record.add_phone("1478523690")
    book.add_record(jane_record)

    print(f"Adressbook after add Jane is {book}")

    john = book.find("John")

    john.edit_phone("1234567890", "1112223330")
    print(f"John after edit phone 1234567890 to 1112223330 is {john}")
    
    found_phone = john.find_phone("1231231231")
    if found_phone: 
        print(f"{found_phone} is phone of {john}")
    else:
        print(f"Record not found")
   
    book.delete("Jane")
    print(f"Adressbook after del Jane is {book}")

if __name__ == "__main__":
    main()