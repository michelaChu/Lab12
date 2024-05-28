from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.retailer import Retailer

class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct gr.Country 
                    from go_retailers gr """

        cursor.execute(query)

        for row in cursor:
            result.append(row["Country"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllRetailers():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from go_retailers gr
                 """

        cursor.execute(query)

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(country):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from go_retailers gr
                    where Country=%s"""

        cursor.execute(query, (country,))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllConnessioni(year, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select gds1.Retailer_code as v0, gds2.Retailer_code as v1, count(*) as peso
                    from go_daily_sales gds1
                    join go_daily_sales gds2 on  gds1.Product_number = gds2.Product_number 
                    where gds1.Retailer_code  < gds2.Retailer_code 
                    and year(gds1.Date) = %s and year(gds1.Date) = year(gds2.Date)
                    group by gds1.Retailer_code, gds2.Retailer_code """

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(Connessione(idMap[int(row["v0"])],
                                      idMap[int(row["v1"])],
                                      row["peso"]))

        cursor.close()
        conn.close()
        return result

