from pathlib import Path
import pandas as pd


# These are the columns we expect in our AWS dataset
EXPECTED_COLUMNS = [
    "cluster",
    "station_name",
    "state",
    "district",
    "date_of_record",
    "avg_temp",
    "min_temp",
    "max_temp",
    "humidity",
    "relative_humidity_pct",
    "dew_point_c",
    "absolute_humidity_g_m3",
    "wind_speed",
    "air_pressure",
    "rainfall",
    "elevation",
    "latitude",
    "longitude",
]


def load_weather_data(file_path):
    """Load the AWS CSV and do some basic checks."""

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(file_path)

    # Check whether all required columns are present
    missing_columns = [
        column for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"These columns are missing: {missing_columns}"
        )

    # Convert the date column into proper datetime format
    df["date_of_record"] = pd.to_datetime(
        df["date_of_record"],
        errors="coerce"
    )

    if df["date_of_record"].isna().any():
        raise ValueError("Some dates could not be converted.")

    # Keep each station's data in chronological order
    df = df.sort_values(
        ["station_name", "date_of_record"]
    ).reset_index(drop=True)

    return df


def check_data(df):
    """Print a few basic checks about the dataset."""

    print("\n========== DATA CHECK ==========")

    print("Rows:", len(df))
    print("Columns:", len(df.columns))
    print("Stations:", df["station_name"].nunique())

    print(
        "Date range:",
        df["date_of_record"].min().date(),
        "to",
        df["date_of_record"].max().date()
    )

    print("Duplicate rows:", df.duplicated().sum())

    duplicate_station_dates = df.duplicated(
        subset=["station_name", "date_of_record"]
    ).sum()

    print(
        "Duplicate station-date pairs:",
        duplicate_station_dates
    )

    print(
        "Missing humidity:",
        df["humidity"].isna().sum()
    )

    print(
        "Missing relative humidity:",
        df["relative_humidity_pct"].isna().sum()
    )

    invalid_rh = (
        (df["relative_humidity_pct"] < 0)
        | (df["relative_humidity_pct"] > 100)
    ).sum()

    print("Invalid RH values:", invalid_rh)

    print("================================\n")