import pandas
import io
import datetime


class DataFrameToolkit:

    @classmethod
    def convert_to_csv(cls, df: pandas.DataFrame) -> bytes:
        """
        Convert the DataFrame to a strongly formatted CSV.
        :param df: pandas DataFrame compatible with Wizata standards.
        :return: bytes containing the full CSV file.
        """
        b_buf = io.BytesIO()

        df.to_csv(b_buf,
                  date_format="%Y-%m-%d-%H-%M-%S-%f",
                  sep=",",
                  decimal=".",
                  encoding="utf-8")

        b_buf.seek(0)
        return b_buf.read()

    @classmethod
    def read_from_csv(cls, b_data: bytes) -> pandas.DataFrame:
        """
        Convert the bytes to a pandas.DataFrame.
        :param b_data: bytes representing a CSV file.
        :return: pandas DataFrame formatted.
        """
        b_buf = io.BytesIO(b_data)

        date_parser = lambda x: datetime.datetime.strptime(x, "%Y-%m-%d-%H-%M-%S-%f")
        df = pandas.read_csv(b_buf,
                             index_col='Timestamp',
                             parse_dates=['Timestamp'],
                             date_parser=date_parser,
                             sep=",",
                             decimal=".",
                             encoding="utf-8")

        return df

    @classmethod
    def convert_from_json(cls, json):
        df = pandas.DataFrame.from_dict(json, orient='columns')
        df = df.set_index('timestamp')
        return df

    @classmethod
    def convert_to_json(cls, df: pandas.DataFrame):
        df_json = {"timestamp": list(df.index)}
        for col in list(df.columns):
            if col != 'Timestamp':
                df_json[col] = list(df[col].values.astype(float))
            else:
                df_json[col] = list(df[col].values)
        return df_json
