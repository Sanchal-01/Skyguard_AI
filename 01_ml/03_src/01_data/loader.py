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
    "relative_humidity",
    "wind_speed",
    "air_pressure",
    "rainfall",
    "elevation",
    "latitude",
    "longitude",
]


def load_weather_data(file_path, sort_data=False):
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

    # Sort only when explicitly requested. This is important because our anomaly dataset can contain delayed / out-of-order records.
    if sort_data:
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
        "Missing relative humidity:",
        df["relative_humidity"].isna().sum()
    )

    invalid_rh = (
        (df["relative_humidity"] < 0)
        | (df["relative_humidity"] > 100)
    ).sum()

    print("Invalid RH values:", invalid_rh)

    # These checks are only done when anomaly ground-truth
    # columns are available in the dataset.
    if "is_injected" in df.columns:
        print(
            "Injected rows:",
            df["is_injected"].sum()
        )

    if "anomaly_category" in df.columns:
        print(
            "Anomaly categories:",
            df["anomaly_category"].value_counts().to_dict()
        )

    print("================================\n")