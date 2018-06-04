

class ListInventario:
    class __ListInventario:
        def __init__(self):
            self.usable = [
                {'img': 'bola.png', 'nome': 'Bola', 'help': 'Arraste até o Pet para usar'},
                {'img': 'maca.png', 'nome': 'Fruta', 'help': 'Arraste até o Pet para usar'},
                {'img': 'seringa.png', 'nome': 'Injeção', 'help': 'Arraste até o Pet para usar'},
            ]

        def loadItens(self):
            return self.usable

    instance = None

    def __init__(self):
        if not ListInventario.instance:
            ListInventario.instance = ListInventario.__ListInventario()

    def __getattr__(self, item):
        return getattr(self.instance, item)

