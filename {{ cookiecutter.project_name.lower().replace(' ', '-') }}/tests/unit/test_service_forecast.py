import pandas as pd
import pytest
from pandas.api.types import is_datetime64_any_dtype as is_datetime

from core import errors
from core.forecast import ForecastModelsService, AdaptiveTimeSeriesForecaster
from io.web.schemas import ColumnTypes


class TestCastColumnTypes:

    def setup_method(self):
        self.service = ForecastModelsService()

    def test_all_numeric_columns(self):
        df = pd.DataFrame({
            'num1': [1, 2, 3],
            'num2': [4.5, 5.5, 6.5]
        })
        column_types, _ = self.service._cast_column_types(df)

        assert set(column_types.numeric) == {'num1', 'num2'}
        assert not column_types.datetime
        assert not column_types.string
        assert not column_types.unknown

    def test_all_string_columns(self):
        df = pd.DataFrame({
            'str1': ['a', 'b', 'c'],
            'str2': ['d', 'e', 'f']
        })
        column_types, _ = self.service._cast_column_types(df)

        assert set(column_types.string) == {'str1', 'str2'}
        assert not column_types.numeric
        assert not column_types.datetime
        assert not column_types.unknown

    def test_mixed_columns(self):
        df = pd.DataFrame({
            'num': [1, 2, 3],
            'str_num': ['1', '2', '3'],
            'date': ['2021-01-01', '2021-01-02', '2021-01-03'],
            'str': ['a', 'b', 'c']
        })
        column_types, df_res = self.service._cast_column_types(df)

        assert set(column_types.numeric) == {'num', 'str_num'}
        assert column_types.datetime == ['date']
        assert column_types.string == ['str']
        assert not column_types.unknown
        assert is_datetime(df_res['date'])

    def test_columns_with_coercion(self):
        df = pd.DataFrame({
            'mixed_num': [1, 2, 'not a number'],
            'mixed_date': ['2021-01-01', True, '2021-01-03']
        })
        column_types, processed_df = self.service._cast_column_types(df)
        assert set(column_types.unknown) == {'mixed_num', 'mixed_date'}
        assert not column_types.datetime
        assert not column_types.string
        assert not column_types.numeric

    def test_columns_all_nones(self):
        df = pd.DataFrame({
            'mixed_num': [None, 2, None],
            'mixed_date': ['2021-01-01', None, '2021-01-03']
        })

        with pytest.raises(errors.DataIsEmpty):
            self.service._cast_column_types(df)

    def test_columns_with_nones(self):
        df = pd.DataFrame({
            'mixed_num': [1, 2, None],
            'mixed_date': ['2021-01-01', None, '2021-01-03']
        })

        column_types, processed_df = self.service._cast_column_types(df)
        assert not column_types.unknown
        assert column_types.datetime == ['mixed_date']
        assert not column_types.string
        assert column_types.numeric == ['mixed_num']

    def test_unknown_column_type(self):
        df = pd.DataFrame({
            'unknown': [1, 'STR', True]
        })
        column_types, _ = self.service._cast_column_types(df)

        assert column_types.unknown == ['unknown']
        assert not column_types.numeric
        assert not column_types.datetime
        assert not column_types.string


class TestGetForecastService:

    def setup_method(self):
        self.service = ForecastModelsService()

    def test_time_series_model_returned(self):
        column_types = ColumnTypes(datetime=['col1'], numeric=['col2'])
        result = self.service._get_forecast_service(column_types)
        assert isinstance(result, AdaptiveTimeSeriesForecaster)

    def test_features_number_error_raised(self):
        column_types = ColumnTypes(datetime=['col1'], numeric=['col2'],
                                   string=['col3'])
        with pytest.raises(errors.FeaturesNumberError):
            self.service._get_forecast_service(column_types)

    def test_string_forecast_not_available_error_raised(self):
        column_types = ColumnTypes(string=['col1'], numeric=['col2'])
        with pytest.raises(errors.StringForecastNotAvailableError):
            self.service._get_forecast_service(column_types)

    def test_wrong_column_types_error_raised(self):
        column_types = ColumnTypes(string=['col1'], unknown=['col2'])
        with pytest.raises(errors.WrongColumnTypesError):
            self.service._get_forecast_service(column_types)
