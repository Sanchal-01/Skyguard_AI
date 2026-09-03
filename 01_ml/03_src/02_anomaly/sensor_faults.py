import numpy as np
import pandas as pd


def add_sudden_spike(df, row_index, column, increase):
    """
    Hum function ko 4 cheezein denge:

    df          → dataset
    row_index   → kaunsi row
    column      → kaunsa sensor
    increase    → kitna change

    Add a sudden spike to one sensor reading.
    """



    original_value = df.loc[row_index, column]     # Prior to anomaly injection save into the original
    new_value = original_value + increase         # New faulty value calculate.

    df.loc[row_index, column] = new_value        # Actual anomaly inject.

    return {
        "original_value": original_value,
        "modified_value": new_value
    }

# Function DataFrame ke saath-saath hume metadata bhi return karega. Later useful while exploring the ground truth.

"""
Example:

        add_sudden_spike(
            df,
            11300,
            "avg_temp",
            15
        )

Mandi ki selected observation ka temperature +15°C kar do.

"""


def add_stuck_at(df, row_indices, column):            # Here we would be [passing] multiple rows.... Ex: [11158, 11159, 11160, 11161, 11162]
    """
    Keep a sensor at the first observed value for several readings.
    """

    original_values = df.loc[row_indices, column].copy()   # Creating the coopy of the original value for anomaly injection

    stuck_value = original_values.iloc[0]   # First value ko sensor ke stuck value ke liye use karenge.

    df.loc[row_indices, column] = stuck_value   # Assign the ssame value to all selected readings


    return {
        "original_values": original_values.tolist(),
        "stuck_value": stuck_value
    }

# Original sequence + stuck value return.

"""
Exactly this:

            81.42
            83.77
            82.02
            83.42
            80.63

becomes:

        81.42
        81.42
        81.42
        81.42
        81.42

"""