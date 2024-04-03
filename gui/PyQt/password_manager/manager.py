import json
from dataclasses import dataclass
from datetime import datetime

from password_manager.encryption.encryption import decrypt_data, encrypt_data


@dataclass
class PasswordEntry:
    name: str
    username: str
    password: str
    last_used_time: datetime

    def serialize(self) -> str:
        return json.dumps({
            'name': self.name,
            "username": self.username,
            "password": self.password,
            "last_used_time": self.last_used_time.isoformat(),
        })


class PasswordEntryFactory:
    @staticmethod
    def deserialize(serialized: str) -> PasswordEntry:
        dict = json.loads(serialized)
        return PasswordEntry(
            name=dict["name"],
            username=dict["username"],
            password=dict["password"],
            last_used_time=datetime.fromisoformat(dict["last_used_time"])
        )


@dataclass
class AddUpdatePasswordEntry:
    name: str
    username: str
    password: str


class Manager:
    def __init__(self, new_id: int, passwords: dict[int, PasswordEntry]) -> None:
        self.new_id = new_id
        self.passwords = passwords

    def add_password_entry(self, password_entry: AddUpdatePasswordEntry) -> None:
        self.passwords[self.new_id] = PasswordEntry(
            name=password_entry.name,
            username=password_entry.username,
            password=password_entry.password,
            last_used_time=datetime.now()
        )
        self.new_id += 1

    def update_password_entry(self, id: int, password_entry: AddUpdatePasswordEntry) -> None:
        self.passwords[id] = PasswordEntry(
            name=password_entry.name,
            username=password_entry.username,
            password=password_entry.password,
            last_used_time=datetime.now()
        )

    def remove_password_entry(self, id: int) -> None:
        del self.passwords[id]

    def serialize(self) -> str:
        return json.dumps({
            "new_id": self.new_id,
            "passwords": {id: password_entry.serialize() for id, password_entry in self.passwords.items()}
        })


class ManagerFactory:
    @staticmethod
    def _deserialize(serialized: str) -> Manager:
        dict = json.loads(serialized)
        return Manager(
            new_id=dict["new_id"],
            passwords={
                id: PasswordEntryFactory.deserialize(serialized_password_entry)
                for id, serialized_password_entry in dict["passwords"].items()
            }
        )

    @classmethod
    def from_file(cls, file_path: str, master_password: str) -> Manager:
        with open(file_path, "rb") as file:
            encrypted = file.read()

        manager_serialized = decrypt_data(master_password, encrypted).decode("UTF-8")  # Can throw DecryptionException
        return cls._deserialize(manager_serialized)

    @staticmethod
    def to_file(manager: Manager, file_path: str, master_password: str) -> None:
        manager_serialized = manager.serialize()
        encrypted = encrypt_data(master_password, manager_serialized.encode("UTF-8"))
        with open(file_path, "wb") as file:
            file.write(encrypted)


class AutoSavingPasswordManager:
    def __init__(self, manager: Manager, file_path: str, master_password: str) -> None:
        self.manager = manager
        self.file_path = file_path
        self.master_password = master_password

        ManagerFactory.to_file(manager=self.manager, file_path=self.file_path, master_password=self.master_password)

    @property
    def passwords(self):
        return self.manager.passwords

    def add_password_entry(self, password_entry: AddUpdatePasswordEntry) -> None:
        self.manager.add_password_entry(password_entry)
        ManagerFactory.to_file(manager=self.manager, file_path=self.file_path, master_password=self.master_password)

    def update_password_entry(self, id: int, password_entry: AddUpdatePasswordEntry) -> None:
        self.manager.update_password_entry(id, password_entry)
        ManagerFactory.to_file(manager=self.manager, file_path=self.file_path, master_password=self.master_password)

    def remove_password_entry(self, id: int) -> None:
        self.manager.remove_password_entry(id)
        ManagerFactory.to_file(manager=self.manager, file_path=self.file_path, master_password=self.master_password)
