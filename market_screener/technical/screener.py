from technical.db import DB_Service
from technical.helpers import available_indexes, get_dataset_name
from technical.data_pipeline import data_pipeline as dp
import pandas as pd

class Screener(DB_Service):

    def __init__(self) -> None:
        super().__init__()
        return

    def merge_conditions(self, conditions = []):
        if len(conditions) == 0:
            return ""
        
        merged_conditions = " AND ".join(conditions)

        return "AND " + merged_conditions



    def screen_self(self, index, date = dp.yesterday.isoformat(), conditions = [], columns = ['symbol', 'close', 'relative_strength', 'rank']):
        """
        Screen a specified index

        """
        # open this to start writing a query
        cursor = self.open_cursor()

        table_name = get_dataset_name(index, date)

        conditions = self.merge_conditions(conditions)

        cursor.execute(
            "SELECT " + ", ".join(columns) + " FROM " + table_name + " WHERE " +
            "rank >= 0.7 " + conditions + " ORDER BY rank DESC"
            )

        results = cursor.fetchall()

        # commit changes to database
        self.connection.commit()

        # close the cursor when done with query
        cursor.close()

        dataset = pd.DataFrame(results, columns=columns)
        return dataset



    def screen_against_reference(self, ref_index = 'S&P500', date = dp.yesterday.isoformat(), conditions = [], columns = ['symbol', 'close', 'relative_strength_sp500', 'rank']):
        """
        Screen a list of indexes against a reference index
        """
        # open this to start writing a query
        cursor = self.open_cursor()

        table_name = get_dataset_name(ref_index, date, homogenous=False)

        conditions = self.merge_conditions(conditions)

        cursor.execute(
            "SELECT " + ", ".join(columns) + " FROM " + table_name + " WHERE " +
            "rank >= 0.7 " + conditions + " ORDER BY rank DESC"
            )

        results = cursor.fetchall()

        # commit changes to database
        self.connection.commit()

        # close the cursor when done with query
        cursor.close()

        dataset = pd.DataFrame(results, columns=columns)
        return dataset

screener = Screener()