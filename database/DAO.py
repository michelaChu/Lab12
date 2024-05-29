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
    def getAllConnessioni(year,country, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.Retailer_code as v0, t2.Retailer_code as v1, count(distinct(t1.Product_number)) as peso
                    from
                    (select gds.Retailer_code, gds.Product_number 
                    from go_daily_sales gds, go_retailers gr
                    where gds.Retailer_code = gr.Retailer_code
                    and year(gds.Date) = %s and gr.Country = %s) t1,
                    (select gds.Retailer_code, gds.Product_number 
                    from go_daily_sales gds, go_retailers gr
                    where gds.Retailer_code = gr.Retailer_code
                    and year(gds.Date) = %s and gr.Country = %s) t2
                    where t1.Product_number = t2.Product_number
                    and t1.Retailer_code < t2.Retailer_code
                    group by t1.Retailer_code, t2.Retailer_code"""

        cursor.execute(query, (year, country, year, country))

        for row in cursor:
            result.append(Connessione(idMap[int(row["v0"])],
                                      idMap[int(row["v1"])],
                                      row["peso"]))

        cursor.close()
        conn.close()
        return result

