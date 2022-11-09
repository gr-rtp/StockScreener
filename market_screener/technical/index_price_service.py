from technical.db import DB_Service
from technical.helpers import iterations, get_table_suffix, get_dataset_name

TABLE_FIELDS = ("date", "open", "close", "high", "low", "volume")


class Index_Price(DB_Service):
    def __init__(self) -> None:
        super().__init__()

        if (self.connection.closed == 0):
            # print(self.connection)
            pass

    def add_index(self, symbol, date, open, close, high, low, volume) -> None:
        # open this to start writing a query
        cursor = self.open_cursor()

        cursor.execute("INSERT INTO "+ symbol +" (date, open, close, high, low, volume) VALUES(%s, %s, %s, %s, %s, %s);",
                       (date, open, close, high, low, volume))

        # commit changes to database
        self.connection.commit()

        # close the cursor when done with query
        cursor.close()
        return

    def get_all(self, symbol):
        # open this to start writing a query
        cursor = self.open_cursor()

        cursor.execute("SELECT * FROM " + symbol + ";")

        # commit changes to database
        self.connection.commit()

        # close the cursor when done with query
        cursor.close()
        return

    def get_date_values(self, symbol, date):
        # open this to start writing a query
        cursor = self.open_cursor()

        cursor.execute(
            "SELECT * FROM " + symbol + " WHERE date = %s LIMIT 1;", (date,))

        # commit changes to database
        self.connection.commit()

        # close the cursor when done with query
        cursor.close()
        return

    def update_index_price(self, symbol, date, **kwargs) -> None:
        # open this to start writing a query
        cursor = self.open_cursor()

        allowed_fields = []
        allowed_values = []

        for key, value in kwargs:
            if key in TABLE_FIELDS:
                allowed_fields.append(key)
                allowed_values.append(value)

        columns = ",".join(allowed_fields)
        values = ",".join(allowed_values)

        cursor.execute("UPDATE " + symbol + " (" + columns + ") VALUES(" +
                       values + ") WHERE date = %s;", (date,))

        # commit changes to database
        self.connection.commit()

        # close the cursor when done with query
        cursor.close()
        return

    def remove_price(self, symbol, date) -> None:
        # open this to start writing a query
        cursor = self.open_cursor()

        cursor.execute("DELETE FROM " + symbol + " WHERE date = %s;", (date,))

        # commit changes to database
        self.connection.commit()

        # close the cursor when done with query
        cursor.close()
        return
    
    def table_exists(self, symbol):
        cursor = self.open_cursor()

        cursor.execute("SELECT EXISTS (SELECT TABLE_NAME from information_schema.tables where table_name=LOWER(%s));", (symbol,))

        self.connection.commit()
        result = cursor.fetchone()

        cursor.close()
        return result[0]

    def init_table(self, symbol):
        # open this to start writing a query
        cursor = self.open_cursor()

        cursor.execute("CREATE TABLE " + symbol + " (id BIGSERIAL NOT NULL PRIMARY KEY, date DATE, open DOUBLE(10, 5), close DOUBLE(10, 5), high DOUBLE(10, 5), low DOUBLE(10, 5), volume INT);")

        # commit changes to database
        self.connection.commit()

        # close the cursor when done with query
        cursor.close()
        return

    def prepare_dataset(self, date, ref_index, symbols: list = []):
    # open this to start writing a query
        cursor = self.open_cursor()

        table_name = get_dataset_name(ref_index, date, homogenous=(len(symbols) == 0))

        suffixes = []

        if len(symbols) < 1:
            symbols = [ref_index]

        for symbol in symbols:
            suffixes.append(get_table_suffix(symbol))
        
        # don't create a new dataset if dataset for same set of stocks on same date already exists
        if self.table_exists(table_name):
            cursor.close()
            return

        # cursor.execute("DROP TABLE IF EXISTS " + table_name + ";")

        cursor.execute("CREATE TABLE " + table_name + " AS (SELECT \"table_name\", null::text as symbol, null::date as date, null::numeric(20, 10) as open, null::numeric(20, 10) as close, null::numeric(20, 10) as high, null::numeric(20, 10) as low, null::bigint as volume, null::numeric(20, 10) as sma10, null::numeric(20, 10) as sma50, null::numeric(20, 10) as sma100, null::numeric(20, 10) as sma150, null::numeric(20, 10) as sma200, null::bigint as volume10, null::bigint as volume50, null::bigint as volume100, null::bigint as volume150, null::bigint as volume200, null::numeric(20, 10) as high_52_week, null::numeric(20, 10) as low_52_week, null::numeric(20, 10) as relative_strength, null::numeric(20, 10) as relative_strength_sp500, null::numeric(20, 2) as rank FROM information_schema.tables WHERE \"table_name\" LIKE any (array['%" + "', '%".join(suffixes) + "']) AND table_schema='public');")

        # commit changes to database
        self.connection.commit()
        
        for suffix in suffixes:

            for i in range(iterations[symbol]):
                cursor.execute(
                    "DO $$DECLARE item record; " +
                    "target_table TEXT; " +
                    "BEGIN " +
                        "FOR item in SELECT \"table_name\" FROM " + table_name + " WHERE table_name like '%" + suffix + "' ORDER BY table_name LIMIT 2000 OFFSET " + str(2000 * i) + " " +
                        "LOOP " +
                        "target_table := item.table_name; " +
                            "EXECUTE 'UPDATE " + table_name + " SET (date, symbol, open, close, high, low, volume, sma10, sma50, sma100, sma150, sma200, volume10, volume50, volume100, volume150, volume200, low_52_week, high_52_week, relative_strength, relative_strength_sp500) = (s2.date, (select obj_description('|| quote_literal(target_table) ||'::regclass)), s2.open, s2.close, s2.high, s2.low, s2.volume, s2.sma10, s2.sma50, s2.sma100, s2.sma150, s2.sma200, s2.volume10, s2.volume50, s2.volume100, s2.volume150, s2.volume200, s2.low_52_week, s2.high_52_week, s2.relative_strength, s2.relative_strength_sp500) " +
                            "FROM (SELECT date, open, close, high, low, volume, sma10, sma50, sma100, sma150, sma200, volume10, volume50, volume100, volume150, volume200, low_52_week, high_52_week, relative_strength, relative_strength_sp500 from '|| quote_ident(target_table) ||' " + 
                            "WHERE CAST(date as TEXT)=''"+ date + "'') AS s2 WHERE table_name='|| quote_literal(target_table); " +
                        "END LOOP; " +
                    "END$$"
                    )

                # commit changes to database
                self.connection.commit()

        cursor.execute("UPDATE " + table_name + " SET \"rank\"=src.percent_rank FROM (SELECT DISTINCT ON (symbol) symbol, PERCENT_RANK() OVER (ORDER BY relative_strength_sp500), table_name FROM " + table_name + " WHERE relative_strength_sp500 IS NOT NULL) AS src WHERE " + table_name + ".table_name=src.table_name;")

        # commit changes to database
        self.connection.commit()

        # close the cursor when done with query
        cursor.close()
        return
