import polars as pl


def encode_data(df: pl.DataFrame) -> pl.DataFrame:
    SMOKER: dict[int, int] = {1: 1, 2: 1, 3: 0, 4: 0}
    BIN: dict[int, int] = {1: 1, 2: 0}
    ASTHMA: dict[int, int] = {1: 0, 2: 1}  # asthma is for performance

    return df.with_columns(
        pl.col("SmokerStatus").map_elements(SMOKER.get, return_dtype=pl.Int8),
        pl.col("AlcoholDrinkers").map_elements(BIN.get, return_dtype=pl.Int8),
        pl.col("HadKidneyDisease").map_elements(BIN.get, return_dtype=pl.Int8),
        pl.col("HadDepressiveDisorder").map_elements(BIN.get, return_dtype=pl.Int8),
        pl.col("HadCOPD").map_elements(BIN.get, return_dtype=pl.Int8),
        pl.col("HadSkinCancer").map_elements(BIN.get, return_dtype=pl.Int8),
        pl.col("HadAsthma").map_elements(ASTHMA.get, return_dtype=pl.Int8),
        pl.col("PhysicalActivities").map_elements(ASTHMA.get, return_dtype=pl.Int8),
        (pl.col("WeightInKilograms") / (pl.col("HeightInMeters") ** 2)).alias("BMI"),
    )
