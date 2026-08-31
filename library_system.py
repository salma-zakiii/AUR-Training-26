from abc import ABC, abstractmethod
from enum import Enum

class ItemStatus(Enum):
    AVAILABLE = "AVAILABLE"
    CHECKED_OUT = "CHECKED_OUT"
    LOST = "LOST"

class LibraryItem(ABC):

    def __init__(self, title: str, status: ItemStatus = ItemStatus.AVAILABLE):
        self.title = title
        self._status = status 

    @property
    def status(self) -> ItemStatus:
        return self._status

    @property
    @abstractmethod
    def loan_period(self) -> int:
        pass

    def checkout(self) -> bool:
        if self._status == ItemStatus.AVAILABLE:
            self._status = ItemStatus.CHECKED_OUT
            return True
        return False

    def return_item(self) -> bool:
        if self._status == ItemStatus.CHECKED_OUT:
            self._status = ItemStatus.AVAILABLE
            return True
        return False

    def mark_lost(self):
        self._status = ItemStatus.LOST

    def __lt__(self, other):
        return self.title.lower() < other.title.lower()

    def __str__(self):
        return f"{self.title} ({self.__class__.__name__}) — {self._status.value.title()}"

    def __repr__(self):
        return f"{self.__class__.__name__}(title={self.title!r})"

    @staticmethod
    def validate_isbn(isbn: str) -> bool:
        """Validates ISBN-13 checksum."""
        s = isbn.replace("-", "").replace(" ", "")
        if len(s) != 13 or not s.isdigit():
            return False
        return (
            sum(int(x) * (1 if i % 2 == 0 else 3) for i, x in enumerate(s)) % 10
            == 0
        )

    @classmethod
    def from_dict(cls, data: dict):
        t = data.get("type")
        cls_map = {"Book": Book, "DVD": DVD, "Magazine": Magazine}
        target_cls = cls_map.get(t)
        if not target_cls:
            raise ValueError(f"Unknown type {t}")

        st = ItemStatus[data.get("status", "AVAILABLE")]
        if target_cls == Book:
            return Book(data["title"], data["author"], data["isbn"], st)
        elif target_cls == DVD:
            return DVD(data["title"], data["director"], st)
        elif target_cls == Magazine:
            return Magazine(data["title"], data["issue"], st)

class Book(LibraryItem):

    def __init__(
        self,
        title: str,
        author: str,
        isbn: str,
        status: ItemStatus = ItemStatus.AVAILABLE,
    ):
        super().__init__(title, status)
        self.author, self.isbn = author, isbn

    @property
    def loan_period(self) -> int:
        return 21

class DVD(LibraryItem):

    def __init__(
        self,
        title: str,
        director: str,
        status: ItemStatus = ItemStatus.AVAILABLE,
    ):
        super().__init__(title, status)
        self.director = director

    @property
    def loan_period(self) -> int:
        return 5

class Magazine(LibraryItem):

    def __init__(
        self,
        title: str,
        issue: str,
        status: ItemStatus = ItemStatus.AVAILABLE,
    ):
        super().__init__(title, status)
        self.issue = issue

    @property
    def loan_period(self) -> int:
        return 14

class Database:

    def __init__(self, filepath: str = "database.txt"):
        self.filepath = filepath

    def load_items(self) -> list:
        items = []
        try:
            with open(self.filepath, "r") as f:
                for line in f:
                    if line.strip():
                        pairs = line.strip().split("|")
                        d = dict(p.split("=", 1) for p in pairs)
                        items.append(LibraryItem.from_dict(d))
        except FileNotFoundError:
            pass
        return items

    def save_items(self, items: list):
        lines = []
        for item in items:
            f = [f"type={item.__class__.__name__}", f"title={item.title}"]
            if isinstance(item, Book):
                f.extend([f"author={item.author}", f"isbn={item.isbn}"])
            elif isinstance(item, DVD):
                f.append(f"director={item.director}")
            elif isinstance(item, Magazine):
                f.append(f"issue={item.issue}")
            f.append(f"status={item.status.name}")
            lines.append("|".join(f))
        with open(self.filepath, "w") as f:
            f.write("\n".join(lines) + "\n")

class Library:

    def __init__(self):
        self.items = []

    def add_item(self, item: LibraryItem):
        self.items.append(item)

    def find_by_title(self, title: str):
        return next(
            (i for i in self.items if i.title.lower() == title.lower()), None
        )

    def checkout(self, title: str) -> bool:
        item = self.find_by_title(title)
        return item.checkout() if item else False

    def return_item(self, title: str) -> bool:
        item = self.find_by_title(title)
        return item.return_item() if item else False

    def list_available(self) -> list:
        return [
            i for i in sorted(self.items) if i.status == ItemStatus.AVAILABLE
        ]

if __name__ == "__main__":
    db = Database("database.txt")
    lib = Library()
    lib.items = db.load_items()
    print("--- Available Items ---")
    for item in lib.list_available():
        print(item)

    print("\n--- Testing Checkout ---")
    if lib.checkout("Dune"):
        print("Successfully checked out Dune!")
    db.save_items(lib.items)