if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    old_cols = set(data.columns)

    data.columns = (data.columns
    .str.replace('(?<=[a-z])(?=[A-Z])', '_', regex=True)
    .str.lower()
    )

    # print number of renamed columns
    n_renamed = len(old_cols - set(data.columns))
    print(f'# of columns renamed: {n_renamed}')

    print(f'Preprocessing: rows with zero passenger: {data["passenger_count"].isin([0]).sum()}')

    # convert pickup datetime to date
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    print(f'number of unique dates: {data.lpep_pickup_date.nunique()}')

    return data.loc[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]

@test
def passenger_count_test(output, *args) -> None:
    assert output["passenger_count"].isin([0]).sum() == 0, 'There are rides with zero passenger.'

@test
def trip_distance_test(output, *args) -> None:
    assert output["trip_distance"].isin([0]).sum() == 0, 'There are rides with zero trip distance.'

@test
def col_test(output, *args) -> None:
    assert 'vendor_id' in output.columns, 'Columns are not correctly renamed.'