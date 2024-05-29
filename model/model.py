import copy

import networkx as nx

from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._allRetailers = DAO.getAllRetailers()
        self._idMap = {}
        for n in self._allRetailers:
            self._idMap[n.Retailer_code] = n
        self._bestPath = []
        self._maxCost = 0

    def bestPath(self, num):
        self._bestPath = []
        self._maxCost = 0
        parziale = []
        for v0 in self._nodes:
            parziale.append(v0)
            self.ricorsione(parziale, v0, num)
            parziale.pop()
        return self._bestPath, self._maxCost

    def ricorsione(self, parziale, v0, num):
        if len(parziale) == num+1:
            if parziale[-1] == v0:
                costo = self.calcolaCosto(parziale)
                if costo > self._maxCost:
                    self._maxCost = costo
                    self._bestPath = copy.deepcopy(parziale)
            return

        for v in self._grafo.neighbors(parziale[-1]):
            if v not in parziale[1:]:
                parziale.append(v)
                self.ricorsione(parziale, v0, num)
                parziale.pop()


    def calcolaCosto(self, listOfNodes):
        if len(listOfNodes) == 1:
            return 0

        score = 0
        for i in range(0, len(listOfNodes) - 1):
            score += self._grafo[listOfNodes[i]][listOfNodes[i + 1]]["weight"]
        return score

    def buildGraph(self, year, country):
        self._grafo.clear()
        self._nodes = DAO.getAllNodes(country)
        self._grafo.add_nodes_from(self._nodes)

        connessioni = DAO.getAllConnessioni(year, country, self._idMap)
        for c in connessioni:
            self._grafo.add_edge(c.v0, c.v1, weight=c.peso)

    def listaVolume(self):
        list = []
        for n in self._nodes:
            list.append((n, self.calcolaVolume(n)))
        lista_ordinata = sorted(list, key=lambda x: x[1], reverse=True)
        return lista_ordinata

    def calcolaVolume(self, v0):
        volume = 0
        for v in list(self._grafo.neighbors(v0)):
            volume += self._grafo[v0][v]["weight"]
        return volume

    def getPesoArco(self, v0, v1):
        return self._grafo[v0][v1]["weight"]

    def getAllCountries(self):
        return DAO.getAllCountries()

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)