import sqlite3
# from dbinterface import configuration
# from dbinterface.DBAlgoAPI import KeyCodeTools
from configs_and_settings.settings import default_settings
from fundemental_fin_val_metrics import get_all_data_on_multiple_stocks
from configs_and_settings import stock_tickers

class DBManager():

    def __init__(self):
        """
        This method initializes the KeyCodeTools class with the parameter db being the str of the
        database's name including its .db extensioni.e. 'testdb.db'
        :param db: str of database's name including its .db extensioni.e. 'testdb.db'
        """
        self.db = default_settings["database_path"]
        self.connection = sqlite3.connect(self.db)
        self.cursor = self.connection.cursor()
        create_SectorsDB_table = """CREATE TABLE IF NOT EXISTS SectorsDB(SectorID INTEGER PRIMARY KEY,
                                            Sector TEXT NOT NULL,
                                            NumberOfIndustries INT NOT NULL,
                                            CreationDate TEXT NOT NULL);"""
        self.cursor.execute(create_SectorsDB_table)
        self.connection.commit()

    def close(self):
        print("Closing connection with the database")
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def __enter__(self):
        # make a database connection and return it
        # self.connect = sqlite3.connect(self.db)
        # self.cursor = self.connection.cursor()
        return self

    def __exit__(self):
        # make sure the dbconnection gets closed
        return self.close()

    def add_new_sector_into_marketsectorsdb(self, sector_name):
        """
        :param self:
        :param industry_name: name of the new subject being entered into the database
        :return: None
        """
        create_sector_industries_table_sql = """CREATE TABLE '{0}'(IndustryID INTEGER PRIMARY KEY,
                                        IndustryName TEXT NOT NULL,
                                        CreationDate TEXT NOT NULL,
                                        NumberOfStockCompanies INTEGER
                                        )""".format(sector_name)
        self.cursor.execute(create_sector_industries_table_sql)
        add_new_subject_sql = """INSERT INTO SectorsDB(Sector,CreationDate,NumberOfIndustries)
                              VALUES (?,date('now'),0)"""
        self.cursor.execute(add_new_subject_sql, (sector_name,))
        self.connection.commit()

    # def add_new_sector(self, sector_name):
    #     """
    #     :param self:
    #     :param industry_name: name of the new subject being entered into the database
    #     :return: None
    #     """
    #     create_sector_industries_table_sql = """CREATE TABLE '{0}'(IndustryID INTEGER PRIMARY KEY,
    #                                     IndustryName TEXT NOT NULL,
    #                                     CreationDate TEXT NOT NULL,
    #                                     NumberOfStockCompanies INTEGER,
    #                                     )""".format(sector_name)
    #     self.cursor.execute(create_sector_industries_table_sql)
    #     add_new_subject_sql = """INSERT INTO SectorsDB(Sector,CreationDate,NumberOfIndustries)
    #                           VALUES (?,date('now'),0)"""
    #     self.cursor.execute(add_new_subject_sql, (sector_name,))
    #     self.connection.commit()

    def add_new_industry(self, industry_name, sector_name):
        """
        :param self:
        :param industry_name: name of the new subject being entered into the database
        :return: None
        """
        create_subject_topics_table_sql = """CREATE TABLE '{0}'(IndustryID INTEGER PRIMARY KEY,
                                        CompanyName TEXT NOT NULL,
                                        PE Ratio '(TTM)' TEXT,
                                        EPS '(TTM)' TEXT,
                                        CreationDate TEXT NOT NULL,
                                        SectorName TEXT,
                                        SectorID INTEGER,
                                        FOREIGN KEY (SectorID) REFERENCES SectorsDB(SectorID))""".format(
            industry_name)
        self.cursor.execute(create_subject_topics_table_sql)
        add_new_subject_sql = """INSERT INTO SectorsDB(Sector,CreationDate,NumberOfIndustries) 
                              VALUES (?,date('now'),0)"""
        self.cursor.execute(add_new_subject_sql, (sector_name,))
        self.connection.commit()

    def add_new_company_stock(self, data_dict):
        """
        :param self:
        :param industry_name: name of the new subject being entered into the database
        :return: None
        """
        create_subject_topics_table_sql = """CREATE TABLE '{0}'(StockID INTEGER PRIMARY KEY,
                                        CompanyName TEXT NOT NULL,
                                        PE Ratio (TTM) TEXT,
                                        EPS (TTM) TEXT,
                                        CreationDate TEXT NOT NULL,
                                        IndustryID INTEGER,
                                        SectorID INTEGER,
                                        FOREIGN KEY (IndustryID) REFERENCES {1}(IndustryID))""".format(
            data_dict["company_name"], data_dict["sector"])
        self.cursor.execute(create_subject_topics_table_sql)
        add_new_subject_sql = """INSERT INTO SectorsDB(Sector,CreationDate,NumberOfIndustries)
                              VALUES (?,date('now'),0)"""
        self.cursor.execute(add_new_subject_sql, (data_dict["sector"],))
        self.connection.commit()



if __name__ == "__main__":
    x = DBManager()
    x.add_new_sector_into_marketsectorsdb("Technology")
    id = get_all_data_on_multiple_stocks(stock_tickers.SEMICONDUCTOR_TICKERS)
    # x.add_new_company_stock(id["NVDA"])




