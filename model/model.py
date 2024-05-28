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

        self.ricorsione([], num)

    def ricorsione(self, parziale, num):

        if len(parziale) == num:
            costo = self.calcolaCosto(parziale)
            if costo > self._maxCost:
                self._maxCost = costo
                self._bestPath = copy.deepcopy(parziale)
            return


    def calcolaCosto(self, parziale):
        peso =0
        for i in range(0, len(parziale)-1):
            peso += self._grafo[parziale[i]][parziale[i+1]]["weight"]
        return peso

    def buildGraph(self, year, country):
        self._grafo.clear()
        self._nodes = DAO.getAllNodes(country)
        self._grafo.add_nodes_from(self._nodes)

        connessioni = DAO.getAllConnessioni(year, self._idMap)
        for c in connessioni:
            if c.v0 in self._grafo and c.v1 in self._grafo:
                self._grafo.add_edge(c.v0, c.v1, weight=c.peso)

    def listaVolume(self):
        list = []
        for n in self._nodes:
            list.append((n, self.calcolaVolume(n)))
        return list.sort(key=lambda x: x[1], reverse=True)

    def calcolaVolume(self, v0):
        volume = 0
        for v in list(self._grafo.neighbors(v0)):
            volume += self._grafo[v0][v]["weight"]
        return volume


    def getAllCountries(self):
        return DAO.getAllCountries()

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)