class Person:
    """
    Kullanıcıları temsil eder. Socket objesi, adresi ve kullanıcı ismi bilgilerini tutar.
    """
    def __init__(self, addr, client):
        self.addr = addr
        self.client = client
        self.name = None

    def __repr__(self):
        return f"Person({self.addr, self.name})"

    def set_name(self, name):
        """
        Kullanıcının ismini set eder.
        :param name: str
        :return: None
        """
        self.name = name
