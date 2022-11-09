# import sys
# sys.path.append('/technical/db.py')

from technical.db import DB_Service

TABLE_FIELDS = ("id", "date", "open", "close", "high", "low", "volume", "sma10", "sma50", "sma100", "sma150", "sma200", "volume10", "volume50", "volume100", "volume150", "volume200", "high_52_week", "low_52_week", "relative_strength", "relative_strength_sp500")


class Stock_Price(DB_Service):
    def __init__(self) -> None:
        super().__init__()

        if (self.connection.closed == 0):
            # print(self.connection)
            pass

    def add_stock(self, symbol, date, open_price, close, high, low, volume) -> None:

        # open this to start writing a query
        cursor = self.open_cursor()

        try:
            cursor.execute("INSERT INTO "+ symbol +" (date, open, close, high, low, volume) VALUES(%s, %s, %s, %s, %s, %s);", (date, open_price, close, high, low, volume))

        except:
            print("===========================================================")
            print(symbol + " " + str(open_price) + " " + str(close) + " " + str(high) + " " + str(low) + " " + str(volume))
            print("===========================================================")

            cursor.execute("rollback")

            cursor.execute("INSERT INTO "+ symbol +" (date, open, close, high, low, volume) VALUES(%s, %s, %s, %s, %s, %s);", ("1900-1-1", 1, 1, 1, 1, 1))
        # commit changes to database
        self.connection.commit()

        # close the cursor when done with query
        cursor.close()
        return

    def bulk_add_stock(self, symbol, stocks_tuple) -> None:

        # open this to start writing a query
        cursor = self.open_cursor()

        try:
            args_str = ','.join(cursor.mogrify("(%s, %s, %s, %s, %s, %s)", x).decode("utf-8") for x in stocks_tuple)

            cursor.execute("INSERT INTO "+ symbol +" (date, open, close, high, low, volume) VALUES " + args_str + ";")

            # commit changes to database
            self.connection.commit()

            # close the cursor when done with query
            cursor.close()

        except:
            cursor.execute("rollback")

            # commit changes to database
            self.connection.commit()

            # close the cursor when done with query
            cursor.close()

            for row in stocks_tuple:
                self.add_stock(symbol, row[0], row[1], row[2], row[3], row[4], row[5])
        return

    def bulk_add_sma_volume(self, symbol, tuple_list) -> None:
        # open this to start writing a query
        cursor = self.open_cursor()

        args_str = ','.join(cursor.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", x).decode("utf-8") for x in tuple_list)

        cursor.execute("UPDATE " + symbol +
                           " as s SET sma10 = s2.sma10, sma50 = s2.sma50, sma100 = s2.sma100, sma150 = s2.sma150, sma200 = s2.sma200, " 
                           + "volume10 = s2.volume10, volume50 = s2.volume50, volume100 = s2.volume100, volume150 = s2.volume150, volume200 = s2.volume200" + 
                           " FROM (VALUES " + args_str + ") as s2(date, sma10, sma50, sma100, sma150, sma200, volume10, volume50, volume100, volume150, volume200) where s2.date = s.date;")
        # commit changes to database
        self.connection.commit()

        # close the cursor when done with query
        cursor.close()
        return

    def get_all_prices(self, symbol, cols = None):
        # open this to start writing a query
        cursor = self.open_cursor()

        if cols is None:
            cols = []

        selected_fields = []

        for col in cols:
            if col in TABLE_FIELDS:
                selected_fields.append(col)

        if len(selected_fields) > 0:
            values = ", ".join(selected_fields)
        else:
            values = "*"

        cursor.execute("SELECT " + values + " FROM " + symbol + " ORDER BY date;")
        index_row = cursor.fetchall()

        # commit changes to database
        self.connection.commit()

        # close the cursor when done with query
        cursor.close()
        return index_row

    def get_some_prices(self, symbol, fetch_days, offset_days, cols = ['date', 'close'], order = 'ASC'):
        # open this to start writing a query
        cursor = self.open_cursor()

        period = ""

        if fetch_days != "max":
            period = " OFFSET " + str(offset_days) + " ROWS FETCH NEXT "+ str(fetch_days) +" ROWS ONLY;"

        selected_fields = []

        for item in cols:
            if item in TABLE_FIELDS:
                selected_fields.append(item)

        items = ", ".join(selected_fields)

        cursor.execute("SELECT " + items + " FROM " + symbol + " ORDER BY date " + order + period + ";")
        index_row = cursor.fetchall()

        # commit changes to database
        self.connection.commit()

        # close the cursor when done with query
        cursor.close()
        return index_row
    
    def get_prices_between_dates(self, symbol, start, end_date, cols = ['date', 'close'], order = 'ASC'):
        # open this to start writing a query
        cursor = self.open_cursor()

        selected_fields = []

        for item in cols:
            if item in TABLE_FIELDS:
                selected_fields.append(item)

        items = ", ".join(selected_fields)

        cursor.execute("SELECT " + items + " FROM " + symbol + " WHERE date >= %s AND date <= %s ORDER BY date "+ order +";", (start, end_date,))
        index_row = cursor.fetchall()

        # commit changes to database
        self.connection.commit()

        # close the cursor when done with query
        cursor.close()
        return index_row

    def get_last_price(self, symbol):
        # open this to start writing a query
        cursor = self.open_cursor()

        cursor.execute("SELECT * FROM " + symbol + " ORDER BY date DESC LIMIT 1;")
        last_row = cursor.fetchone()

        # commit changes to database
        self.connection.commit()

        # close the cursor when done with query
        cursor.close()
        return last_row

    def get_first_price(self, symbol):
        # open this to start writing a query
        cursor = self.open_cursor()

        cursor.execute("SELECT * FROM " + symbol + " ORDER BY date ASC LIMIT 1;")
        first_row = cursor.fetchone()

        # commit changes to database
        self.connection.commit()

        # close the cursor when done with query
        cursor.close()
        return first_row

    def get_total_stocks(self):
        # open this to start writing a query

        cursor = self.open_cursor()

        cursor.execute("select count(*) from information_schema.tables where table_schema = 'public' and table_type = 'BASE TABLE' and table_name not like 'index_%' and table_name not like '%daily%';")
        total_stocks = cursor.fetchone()[0]
 
        cursor.execute("select count(*) from information_schema.tables where table_schema = 'public' and table_type = 'BASE TABLE' and table_name not like 'index_%' and table_name not like '%daily%' and table_name like '%_dow';")    
        total_dow = cursor.fetchone()[0]

        cursor.execute("select count(*) from information_schema.tables where table_schema = 'public' and table_type = 'BASE TABLE' and table_name not like 'index_%' and table_name not like '%daily%' and table_name like '%_s_p500';")    
        total_sp500 = cursor.fetchone()[0]

        cursor.execute("select count(*) from information_schema.tables where table_schema = 'public' and table_type = 'BASE TABLE' and table_name not like 'index_%' and table_name not like '%daily%' and table_name like '%_nyse';")    
        total_nyse = cursor.fetchone()[0]

        cursor.execute("select count(*) from information_schema.tables where table_schema = 'public' and table_type = 'BASE TABLE' and table_name not like 'index_%' and table_name not like '%daily%' and table_name like '%_nasdaq';")    
        total_nasdaq = cursor.fetchone()[0]

        # commit changes to database
        self.connection.commit()

        # close the cursor when done with query
        cursor.close()
        return total_stocks, total_dow, total_sp500, total_nyse, total_nasdaq

    def add_comment(self, table_name, symbol):
        # open this to start writing a query
        cursor = self.open_cursor()

        cursor.execute("COMMENT ON TABLE " + table_name + " IS '" + symbol + "';")

        # commit changes to database
        self.connection.commit()

        # close the cursor when done with query
        cursor.close()
        return

    def get_row_count(self, symbol):
        # open this to start writing a query
        cursor = self.open_cursor()

        cursor.execute("SELECT reltuples AS estimate FROM pg_class WHERE relname = '"+ symbol + "';")
        row_count = cursor.fetchone()

        # commit changes to database
        self.connection.commit()

        # close the cursor when done with query
        cursor.close()
        return row_count

    def get_record_at_date(self, symbol, date):
        # open this to start writing a query
        cursor = self.open_cursor()

        cursor.execute(
            "SELECT * FROM " + symbol + " WHERE date = %s LIMIT 1;", (date,))

        # commit changes to database
        self.connection.commit()

        # close the cursor when done with query
        cursor.close()
        return

    def update_stock_at_date(self, symbol, date, **kwargs) -> None:
        # open this to start writing a query
        cursor = self.open_cursor()

        allowed_fields = []
        allowed_values = []

        for key, value in kwargs.items():
            if key in TABLE_FIELDS:
                allowed_fields.append(key)
                allowed_values.append(value)

        columns = ",".join(allowed_fields)
        values = ",".join(allowed_values)

        cursor.execute("UPDATE " + symbol + " SET (" + columns + ")=(" +
                       values + ") WHERE CAST(date as TEXT) = %s;", (date,))

        # commit changes to database
        self.connection.commit()

        # close the cursor when done with query
        cursor.close()
        return
    
    def bulk_update_stock(self, symbol, cols, values):
        # open this to start writing a query
        cursor = self.open_cursor()

        column_fields = []
        updates = []
        formatter = []

        for col in cols:
            if col in TABLE_FIELDS:
                column_fields.append(col)
                formatter.append('%s')

                if col != 'date':
                    updates.append(col + "=s2." + col)

        columns = ", ".join(column_fields)
        updates = ", ".join(updates)
        format_string = "(" + ", ".join(formatter) + ")"

        args_str = ','.join(cursor.mogrify(format_string, x).decode("utf-8") for x in values)

        cursor.execute("UPDATE " + symbol +
                           " as s SET " + updates +
                           " FROM (VALUES " + args_str + ") as s2("+ columns +") WHERE s2.date = s.date;")

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

    def remove_table(self, symbol) -> None:
        # open this to start writing a query
        cursor = self.open_cursor()

        cursor.execute("DROP "+ symbol +" IF EXISTS FROM information_schema.tables;")

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

    def init_table(self, table_name, symbol):
        # open this to start writing a query
        cursor = self.open_cursor()

        cursor.execute(
            "DO $$ " +
            "BEGIN " +
                "CREATE TABLE IF NOT EXISTS " + table_name + " (id BIGSERIAL NOT NULL PRIMARY KEY, date DATE, open NUMERIC(20, 10), close NUMERIC(20, 10), high NUMERIC(20, 10), low NUMERIC(20, 10), volume Bigint, sma10 NUMERIC(20, 10), sma50 NUMERIC(20, 10), sma100 NUMERIC(20, 10), sma150 NUMERIC(20, 10), sma200 NUMERIC(20, 10), volume10 Bigint, volume50 Bigint, volume100 Bigint, volume150 Bigint, volume200 Bigint, high_52_week NUMERIC(20, 10), low_52_week NUMERIC(20, 10), relative_strength NUMERIC(20, 10), relative_strength_sp500 NUMERIC(20, 10));" +
                "COMMENT ON TABLE " + table_name + " IS '" + symbol + "';" +
            "END$$"
        )

        # cursor.execute("CREATE TABLE IF NOT EXISTS " + table_name + " (id BIGSERIAL NOT NULL PRIMARY KEY, date DATE, open NUMERIC(20, 10), close NUMERIC(20, 10), high NUMERIC(20, 10), low NUMERIC(20, 10), volume Bigint, sma10 NUMERIC(20, 10), sma50 NUMERIC(20, 10), sma100 NUMERIC(20, 10), sma150 NUMERIC(20, 10), sma200 NUMERIC(20, 10), volume10 Bigint, volume50 Bigint, volume100 Bigint, volume150 Bigint, volume200 Bigint, high_52_week NUMERIC(20, 10), low_52_week NUMERIC(20, 10), relative_strength NUMERIC(20, 10), relative_strength_sp500 NUMERIC(20, 10));")
        
        # cursor.execute("COMMENT ON TABLE " + table_name + " IS '" + symbol + "';")

        # commit changes to database
        self.connection.commit()


        # close the cursor when done with query
        cursor.close()
        return
