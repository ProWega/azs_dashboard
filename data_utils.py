import sqlite3
import pandas as pd
import datetime
import time

connection = sqlite3.connect('azs.db')
cursor = connection.cursor()

cursor.execute('''SELECT * FROM oil''')
oil = cursor.fetchall()
oil_ids = [el[0] for el in oil]
oil_names = [el[1] for el in oil]
oil_name_to_oil_id = dict(zip(oil_names, oil_ids))
oil_id_to_oil_name = dict(zip(oil_ids, oil_names))

cursor.execute('''SELECT * FROM type_oil''')
oil_types = cursor.fetchall()
oil_types_id = [el[0] for el in oil_types]
oil_types_names = [el[1] for el in oil_types]
oil_type_name_to_oil_type_id = dict(zip(oil_types_names, oil_types_id))
oil_type_id_to_oil_type_name = dict(zip(oil_types_id, oil_types_names))

cursor.execute('''SELECT * FROM station''')
station = cursor.fetchall()
id_stations = [el[0] for el in station]
links_station = [el[1] for el in station]
id_stations_to_links_station = dict(zip(id_stations, links_station))
links_station_to_id_stations = dict(zip(links_station, id_stations))

cursor.execute('''SELECT * FROM station_company''')
station_company = cursor.fetchall()
id_stations = [el[0] for el in station_company]
id_company = [el[1] for el in station_company]
id_station_to_id_company = dict(zip(id_stations, id_company))

cursor.execute('''SELECT * FROM company''')
company = cursor.fetchall()
id_company_company = [el[0] for el in company]
name_company = [el[1] for el in company]
id_company_to_name_company = dict(zip(id_company_company, name_company))
name_company_to_id_company = dict(zip(name_company, id_company_company))

cursor.execute('''SELECT * FROM oil_brand_or_not''')
company = cursor.fetchall()
id_oil_ = [el[0] for el in company]
brand_status = [el[1] for el in company]
oil_id_to_brand_status = dict(zip(id_oil_, brand_status))

cursor.execute('''SELECT * FROM type_company''')
res = cursor.fetchall()
id_type_company = [el[0] for el in res]
company_status_name = [el[1] for el in res]
id_type_company_to_company_status_name = dict(zip(id_type_company, company_status_name))
company_status_name_to_id_type_company = dict(zip(company_status_name, id_type_company))

cursor.execute('''SELECT * FROM company_type_company''')
res = cursor.fetchall()
id_company = [el[0] for el in res]
id_type_company = [el[1] for el in res]
name_type_company = [id_type_company_to_company_status_name[el] for el in id_type_company]
id_company_to_name_type_company = dict(zip(id_company, name_type_company))

cursor.execute('''SELECT * FROM oil_id_type_oil_id''')
res = cursor.fetchall()
oil_ids = [el[0] for el in res]
type_oil_id = [el[1] for el in res]
name_type_oil_id = [oil_type_id_to_oil_type_name[el] for el in type_oil_id]
oil_id_to_type_oil_id = dict(zip(oil_ids, type_oil_id))
oil_id_to_name_of_type_oil_id = dict(zip(oil_ids, name_type_oil_id))

connection.commit()
connection.close()


def DateFromTimeStamp(timestamp_value):
    date = datetime.datetime.fromtimestamp(timestamp_value)
    return date


def StringFromDate(date):
    return date.strftime('%d-%m-%Y')


def TimestampFromDate(date):
    return time.mktime(date.timetuple())
class DataWorker:
    def __init__(self):
        connection = sqlite3.connect('azs.db')

        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM price''')
        res = cursor.fetchall()
        connection.commit()
        connection.close()

        id_stations_ = []
        id_oils = []
        oil_names_ = []
        oil_types_ = []
        date = []
        prices = []
        company_names = []
        company_statuses = []
        brand_statuses = []
        links = []
        i = 0
        for el in res:
            i += 1
            id_station = el[0]
            id_stations_.append(id_station)
            id_oil = el[1]
            id_oils.append(id_oil)
            oil_names_.append(oil_id_to_oil_name[id_oil])
            oil_types_.append(oil_id_to_name_of_type_oil_id[id_oil])
            brand_statuses.append(oil_id_to_brand_status[id_oil])
            date.append(DateFromTimeStamp(el[2]))
            prices.append(el[3])
            id_company_ = id_station_to_id_company[id_station]
            company_names.append(id_company_to_name_company[id_company_])

            company_statuses.append(id_company_to_name_type_company[id_company_])
            links.append(id_stations_to_links_station[id_station])

        df = pd.DataFrame({"Ссылка": links,
                           "Компания": company_names,
                           "Тип компании": company_statuses,
                           "Топливо": oil_names_,
                           "Тип топлива": oil_types_,
                           "Брендинг": brand_statuses,
                           "Цена": prices,
                           "Дата": date})
        print(f"Count {i}")
        self.max_date = df['Дата'].values.max()
        self.main_df = df




    def GetDictOilTypes(self):
        connection = sqlite3.connect('azs.db')
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM type_oil''')
        types_oil = cursor.fetchall()
        id_oil = [el[0] for el in types_oil]
        name_oil = [el[1] for el in types_oil]
        oil_type_dict = dict(zip(name_oil, id_oil))
        connection.commit()
        connection.close()
        return oil_type_dict

    def GetOilIdsByTypeName(self, type_oil_name):
        oil_type_id = oil_type_name_to_oil_type_id[type_oil_name]
        connection = sqlite3.connect('azs.db')
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM oil_id_type_oil_id''')
        res = cursor.fetchall()
        oil_ids = [el[0] for el in res if el[1] == oil_type_id]
        connection.commit()
        connection.close()
        return oil_ids

    def GetMainDf(self):
        return self.main_df

    def GetLastUpdateDf(self):
        date = self.max_date.tolist()
        date = DateFromTimeStamp(float(date) / (10**9))

        date_max = datetime.datetime(year=date.year, month=date.month, day=date.day)
        return self.main_df[self.main_df['Дата'] >= date_max]

    def GetFuelDfLastUpdate(self):

        fuel_df = pd.DataFrame(columns=['Тип топлива', 'Мин', 'Макс', "Средн"])
        max_date = self.max_date
        df_max_date = self.main_df[self.main_df['Дата'] == max_date]
        print(max_date)

        for type_oil_name in oil_types_names:
            df = df_max_date[df_max_date['Тип топлива'] == type_oil_name]
            df_brand = df[df['Брендинг']=='Бренд']
            df_non_brand = df[df['Брендинг']!='Бренд']
            if len(df_non_brand) > 0:
                price_non_brand_min  = round(df_non_brand['Цена'].values.min(), 2)
                price_non_brand_max = round(df_non_brand['Цена'].values.max(), 2)
                price_non_brand_mean = round(df_non_brand['Цена'].values.mean(), 2)
                fuel_df.loc[len(fuel_df)] = [type_oil_name, price_non_brand_min, price_non_brand_max, price_non_brand_mean]


            if len(df_brand) > 0:
                price_brand_min = round(df_brand['Цена'].values.min(), 2)
                price_brand_max = round(df_brand['Цена'].values.max(), 2)
                price_brand_mean = round(df_brand['Цена'].values.mean(), 2)
                fuel_df.loc[len(fuel_df)] = [type_oil_name + " Бренд", price_brand_min, price_brand_max,
                                                 price_brand_mean]

        return fuel_df

