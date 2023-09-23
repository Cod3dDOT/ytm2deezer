class Item:
    """A base class for songs/playlists"""

    _id: str = ""
    _name: str = ""
    _authors: list[str] = []

    def __init__(self, item_id: str, name: str, authors: list[str]) -> None:
        self._id = item_id
        self._name = name
        self._authors = authors

    @property
    def id(self) -> str:
        """Returns item id"""
        return self._id

    @property
    def name(self) -> str:
        """Returns item name"""
        return self._name

    @property
    def authors(self) -> list[str]:
        """Reruns item's authors"""
        return self._authors

    def __str__(self) -> str:
        return f"ITEM (id: {self.id} | name: {self.name} | authors: {self.authors})"

    def __repr__(self) -> str:
        return self.__str__()
