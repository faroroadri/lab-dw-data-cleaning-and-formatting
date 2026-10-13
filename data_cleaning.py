import pandas as pd


def clean_column_names(df):
    """Standardize column names."""
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    df = df.rename(columns={"st": "state"})
    return df


def clean_invalid_values(df):
    """Standardize inconsistent values."""
    # Clean gender values
    df["gender"] = (
        df["gender"]
        .astype("string")
        .str.strip()
        .str.lower()
        .replace({
            "f": "F",
            "female": "F",
            "femal": "F",
            "m": "M",
            "male": "M"
        })
    )

    # Standardize state names
    df["state"] = df["state"].replace({
        "AZ": "Arizona",
        "Cali": "California",
        "WA": "Washington"
    })

    # Standardize education
    df["education"] = df["education"].replace({
        "Bachelors": "Bachelor"
    })

    # Remove percentage signs
    df["customer_lifetime_value"] = (
        df["customer_lifetime_value"]
        .astype("string")
        .str.replace("%", "", regex=False)
    )

    # Standardize vehicle classes
    df["vehicle_class"] = df["vehicle_class"].replace({
        "Sports Car": "Luxury",
        "Luxury SUV": "Luxury",
        "Luxury Car": "Luxury"
    })

    return df


def format_data_types(df):
    """Convert columns to appropriate data types."""
    df["customer_lifetime_value"] = pd.to_numeric(
        df["customer_lifetime_value"], errors="coerce"
    )

    df["number_of_open_complaints"] = (
        df["number_of_open_complaints"]
        .astype("string")
        .str.split("/")
        .str[1]
    )

    df["number_of_open_complaints"] = pd.to_numeric(
        df["number_of_open_complaints"], errors="coerce"
    )

    return df


def handle_missing_values(df):
    """Fill missing values with median or mode."""
    numerical_columns = df.select_dtypes(include="number").columns

    for column in numerical_columns:
        median_value = df[column].median()
        if pd.notna(median_value):
            df[column] = df[column].fillna(median_value)

    categorical_columns = df.select_dtypes(
        include=["object", "str", "category", "string"]
    ).columns

    for column in categorical_columns:
        mode_values = df[column].mode(dropna=True)

        if not mode_values.empty:
            df[column] = df[column].fillna(mode_values[0])

    return df


def convert_numeric_columns_to_integers(df):
    """Round numeric columns and convert them to integers."""
    numerical_columns = df.select_dtypes(include="number").columns

    for column in numerical_columns:
        if df[column].isnull().any():
            df[column] = df[column].fillna(0)

        df[column] = df[column].round().astype("int64")

    return df


def remove_duplicates(df):
    """Remove duplicate rows and reset the index."""
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    return df


def main(df):
    """Run all data cleaning and formatting steps."""
    df = clean_column_names(df)
    df = clean_invalid_values(df)
    df = format_data_types(df)
    df = handle_missing_values(df)
    df = convert_numeric_columns_to_integers(df)
    df = remove_duplicates(df)

    return df