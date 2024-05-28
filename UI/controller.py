import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):

        years = [2015, 2016, 2017, 2018]
        for y in years:
            self._view.ddyear.options.append(ft.dropdown.Option(str(y)))

        countries = self._model.getAllCountries()
        for c in countries:
            self._view.ddcountry.options.append(ft.dropdown.Option(c))

        self._view.update_page()


    def handle_graph(self, e):
        self._model.buildGraph(self._view.ddyear.value, self._view.ddcountry.value)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo con {self._model.getNumNodi()} nodi e {self._model.getNumArchi()} archi"))
        self._view.update_page()


    def handle_volume(self, e):
        self._view.txtOut2.controls.clear()
        list = self._model.listaVolume()
        for l in list:
            self._view.txtOut2.controls.append(ft.Text(f"{l[0]} --> {l[1]}"))
        self._view.update_page()

    def handle_path(self, e):
        try:
            num = int(self._view.txtN.value)
        except:
            self._view.create_alert(f"Inserire un valore intero")

        if num < 2:
            self._view.create_alert(f"Deve essre almeno 2")
            return

        self._model.bestPath(num)

