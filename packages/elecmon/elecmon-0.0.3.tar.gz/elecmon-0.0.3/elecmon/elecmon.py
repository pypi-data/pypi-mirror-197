# import requests
# api_token = 'e21ea17f-1f66-449c-90de-e54906a459f5'

# endpoint = 'https://web-api.tp.entsoe.eu/api'

# params = {'securityToken': api_token,
#           'documentType': 'A44',
#           'in_Domain': '10YES-REE------0',
#           'out_Domain': '10YES-REE------0',
#           'periodStart': '202301290000',
#           'periodEnd': '202301302300'
#           }

# response = requests.get(url=endpoint, params=params)
# if response.status_code == 200:
#     data = response.json()
# else:
#     print(response.text)

# pass

import os
import requests
import json
import csv
from datetime import datetime, timedelta, timezone
import sqlite3
from pathlib import Path
import shutil

from baseutils_phornee import Config

PLAIN_KWH = 0.1623
PADDED_LINE = 60


class ElectricityMonitor():
    databaseElectricityMonitor = None

    def __init__(self, db_path: str = None):
        if not db_path:
            db_path = os.path.join(self.getHomevarPath(), 'energy.db')

            if not os.path.exists(self.getHomevarPath()):
                os.makedirs(self.getHomevarPath())

            if not os.path.exists(db_path):
                shutil.copy(os.path.join(Path(__file__).parent.resolve(), 'data/energy_template.db'), db_path)

        self.database = sqlite3.connect(db_path)

        self.config = Config(self.getClassName(), './config-template.yml', 'config.yml')

    @classmethod
    def getClassName(cls):
        return "elecmon"

    def getHomevarPath(self):
        return "{}/var/{}".format(str(Path.home()), self.getClassName())

    def add_pvpc_from_esios(self, day: datetime, day_info):
        # Esios GeoID: 8741 - Peninsula, 8742 - Canarias, 8743 - Baleares, 8744 - Ceuta, 8745 - Melilla
        url = "https://api.esios.ree.es/archives/70/download_json"
        url = "https://api.esios.ree.es/archives/70/download_json?date={}-{:02d}-{:02d}".format(day.year,
                                                                                                day.month,
                                                                                                day.day)
        params = {
            # "start_Date": "{}-{:02d}-{:02d}T00:00:00Z".format(
            #     day.year, day.month, day.day
            # ),
            # "end_Date": "{}-{:02d}-{:02d}T23:00:00Z".format(
            #     day.year, day.month, day.day
            # ),
            # "geo_ids": ["8741"],
            # "Date_type": "datos"
        }

        headers = {
            "Accept": "application/json; application/vnd.esios-api-v2+json",
            "Content-Type": "application/json",
            "Host": "api.esios.ree.es",
            "x-api-key": self.config['esios_api_key']
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            json_data = json.loads(response.text)

            if "PVPC" in json_data:
                pvpc_raw = json_data["PVPC"]
                for hour_data in pvpc_raw:
                    dat = datetime.strptime(hour_data["Dia"], r"%d/%m/%Y")
                    hour = int(hour_data["Hora"][:2])
                    dat = dat.replace(hour=hour)
                    if dat not in day_info:
                        day_info[dat] = {}
                    # PCB stands for "Peninsula, Canarias, Baleares" From esios it cames in Mwh. need to convert to kWh
                    day_info[dat]["pricekWh"] = (
                        float(hour_data["PCB"].replace(",", ".")) / 1000
                    )

    def get_timestamp_from_naive(self, date: datetime):
        return date.replace(tzinfo=timezone.utc).timestamp()

    def get_naive_date_from_timestamp(self, timestamp):
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).replace(tzinfo=None)

    def add_iberdrola_consumption_from_csv(self, day: datetime, day_info):
        added = False
        csvFilePath = (
            "elecmon/elecmon/data/consumo_periodo_{0:02d}-{1:02d}-{2}_{0:02d}-{1:02d}-{2}.csv".format(
                day.day, day.month, day.year
            )
        )
        if os.path.exists(csvFilePath):
            with open(csvFilePath) as csvFile:
                csvReader = csv.DictReader(csvFile, delimiter=";")
                for rows in csvReader:
                    dat = datetime.strptime(rows["Fecha"], r"%d/%m/%Y")
                    hour = int(rows["Hora"]) - 1
                    dat = dat.replace(hour=hour)
                    if dat not in day_info:
                        day_info[dat] = {}
                    day_info[dat]["kWh"] = float(rows["Consumo_kWh"].replace(",", "."))
            added = True
        else:
            print("No consumption CSV for day {}.".format(day.strftime("%Y/%m/%d")))

        return added

    def insert_info_into_db(self, day_info: dict):
        if day_info:
            cur = self.database.cursor()

            values_list = []
            for hour, hour_data in day_info.items():
                kWh = hour_data.get("kWh", None)
                if kWh is None:
                    kWh = "NULL"
                pricekWh = hour_data.get("pricekWh", None)
                if pricekWh is None:
                    pricekWh = "NULL"

                values_list.append((self.get_timestamp_from_naive(hour), kWh, pricekWh))

            values = ",".join(
                ["('{}', {}, {})".format(value[0], value[1], value[2]) for value in values_list]
            )

            sql = """INSERT INTO electricity(timestamp, kWh, pricekWh) VALUES {}
                    ON CONFLICT (timestamp) DO UPDATE
                    SET pricekWh = excluded.pricekWh,
                    kWh = excluded.kWh  """.format(
                values
            )
            res = cur.execute(sql)
            x = res.fetchall()

            self.database.commit()

    def get_info_from_db(self, day: datetime):
        end_of_day = day + timedelta(hours=23)
        cur = self.database.cursor()
        res = cur.execute(
            "SELECT * FROM electricity WHERE timestamp BETWEEN {} AND {}".format(
                self.get_timestamp_from_naive(day),
                self.get_timestamp_from_naive(end_of_day)
            )
        )
        pvpc = res.fetchall()

        return {
            self.get_naive_date_from_timestamp(timestamp): {"pricekWh": pricekWh, "kWh": kWh}
            for timestamp, kWh, pricekWh in pvpc
        }

    def has_pvpc(self, day_info):
        if day_info:
            first_hour_value = list(day_info.items())[0][1]
            has = first_hour_value.get('pricekWh', None)
        else:
            has = False
        return has

    def has_consumption(self, day_info):
        if day_info:
            first_hour_value = list(day_info.items())[0][1]
            has = first_hour_value.get('kWh', None)
        else:
            has = False
        return has

    def get_elec_info(self, day: datetime):
        elec_info = self.get_info_from_db(day)
        added = False
        if not self.has_pvpc(elec_info):
            self.add_pvpc_from_esios(day, elec_info)
            added = True

        if not self.has_consumption(elec_info):
            added_consumption = self.add_iberdrola_consumption_from_csv(day, elec_info)
            added = added or added_consumption

        if added:
            self.insert_info_into_db(elec_info)
        return elec_info

    def _print_padded_line(self, line):
        print("{s:=^{n}}".format(s=" {} ".format(line), n=PADDED_LINE))

    def print_date_range_data(self, start_day: datetime, end_day: datetime):
        self._print_padded_line(
            "START DAY {}  |  END DAY {}".format(
                start_day.strftime("%d/%m/%Y"), end_day.strftime("%d/%m/%Y")
            )
        )

        self._print_padded_line(
            "Number of days: {} | LIB price {}".format(
                (end_day - start_day).days, PLAIN_KWH
            )
        )

        tot_money_reg = 0
        tot_money_lib = 0
        total_kHw = 0
        day = start_day
        while day <= end_day:
            if day.weekday() == 0:
                print("." * PADDED_LINE)
            elec_info = self.get_elec_info(day)

            money_reg = 0
            money_lib = 0
            kWh_day = 0
            for hour, data in elec_info.items():
                if data.get("kWh", None):
                    kWh_day += data["kWh"]
                    total_kHw += data["kWh"]
                    money_reg += data["kWh"] * data["pricekWh"]
                    money_lib += data["kWh"] * PLAIN_KWH
            print(
                "{} | REG: {:.4f}€ | LIB: {:.4f}€ | AVG pricekWh: {:.4f}".format(
                    day.strftime("%Y/%m/%d"), money_reg, money_lib, money_reg/kWh_day
                )
            )

            tot_money_reg += money_reg
            tot_money_lib += money_lib

            day += timedelta(days=1)

        print(
                "TOTAL kWh: {:.4f} | TOTAL price: {:.4f}€ | LIB: {:.4f}€".format(
                    total_kHw, tot_money_reg, tot_money_lib
                )
            )
        if total_kHw > 0:
            print("AVG REG price kWh: {:.4f}".format(tot_money_reg / total_kHw))

    def print_date_detailed_data(self, day: datetime):
        self._print_padded_line("DAY {}".format(day.strftime("%d/%m/%Y")))

        tot_money_reg = 0
        tot_money_lib = 0

        elec_info = self.get_elec_info(day)

        money_reg = 0
        money_lib = 0
        total_kHw = 0
        for hour, data in elec_info.items():
            if data.get("kWh", None):
                total_kHw += data["kWh"]
                hour_reg = data["kWh"] * data["pricekWh"]
                hour_lib = data["kWh"] * PLAIN_KWH
            money_reg += hour_reg
            money_lib += hour_lib
            print(
                "{} | REG: {:.4f}€ | LIB: {:.4f}€".format(
                    self.get_naive_date_from_timestamp(hour).strftime("%H"), hour_reg, hour_lib
                )
            )

        tot_money_reg += money_reg
        tot_money_lib += money_lib

        print("TOTAL REG: {:.4f}€ | LIB: {:.4f}€".format(tot_money_reg, tot_money_lib))
        print("AVG REG price kWh: {:.4f}".format(tot_money_reg / total_kHw))

    def get_better_timeslice(self, timeslice_minutes: int, time: datetime = None):
        # If optional time is specified, use that instead of real "now"
        if time:
            now = time
        else:
            now = datetime.today()

        today = now.replace(hour=0, minute=0, second=0, microsecond=0)

        # Get info for today and tomorrow (if already available: its refreshed every day at 21:00 aprox.)
        elec_info = self.get_elec_info(today)
        elec_info.update(self.get_elec_info(today + timedelta(days=1)))

        timeslice_hours = int(timeslice_minutes / 60)

        hours = []
        # Get a list of prices per hour
        for hour, value in elec_info.items():
            if hour.hour >= now.hour:
                hours.append([hour, value["pricekWh"]])

        end_hours_idx = len(hours)

        # Real prices
        for idx in range(end_hours_idx):
            minutes_left = timeslice_minutes

            if idx == 0:
                minutes_left_this_hour = 60 - now.minute
            else:
                minutes_left_this_hour = 60

            hours[idx].extend([0, False])
            next_hours_idx = idx
            # Traverse following hours until covering all the timeslice_minutes
            while minutes_left > 0:
                # Clamp if we dont have data for some of the following hours: extrapolate the last one
                if next_hours_idx >= end_hours_idx:
                    clamped_hour = end_hours_idx - 1
                    hours[idx][3] = True
                else:
                    clamped_hour = next_hours_idx

                if minutes_left > minutes_left_this_hour:
                    minutes_applicable = minutes_left_this_hour
                else:
                    minutes_applicable = minutes_left

                if minutes_applicable > 60:
                    minutes_applicable = 60

                hours[idx][2] += hours[clamped_hour][1] * minutes_applicable / 60

                minutes_left -= minutes_applicable
                minutes_left_this_hour = 60
                next_hours_idx += 1

        min_price = 99999
        best_hour = None
        for idx, value in enumerate(hours):
            if value[2] < min_price:
                min_price = value[2]
                best_hour = hours[idx][0]

        return best_hour, min_price


if __name__ == '__main__':
    elec_mon = ElectricityMonitor()

    start_day = datetime(2023, 1, 9)
    end_day = datetime(2023, 3, 12)
    elec_mon.print_date_range_data(start_day, end_day)
