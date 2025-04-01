import polars as pl


class PreProcesser:
    def merge_columns(self, df: pl.DataFrame) -> pl.DataFrame:
        df: pl.DataFrame = df.with_columns(
            pl.when(
                (pl.col("BlindOrVisionDifficulty") == 1)
                | (pl.col("DeafOrHardOfHearing") == 1)
            )
            .then(1)
            .when(
                (pl.col("BlindOrVisionDifficulty") == 2)
                | (pl.col("DeafOrHardOfHearing") == 2)
            )
            .then(0)
            .otherwise(None)
            .cast(pl.Int8)
            .alias("Sensory Impairments")
        )
        df: pl.DataFrame = df.drop(["BlindOrVisionDifficulty", "DeafOrHardOfHearing"])

        df: pl.DataFrame = df.with_columns(
            pl.when((pl.col("FluVaxLast12") == 1) | (pl.col("PneumoVaxEver") == 1))
            .then(1)
            .when((pl.col("FluVaxLast12") == 2) | (pl.col("PneumoVaxEver") == 2))
            .then(0)
            .otherwise(None)
            .cast(pl.Int8)
            .alias("Vaccinated")
        )

        df: pl.DataFrame = df.drop(["FluVaxLast12", "PneumoVaxEver"])
        df: pl.DataFrame = df.with_columns(
            pl.when(
                (pl.col("DifficultyWalking") == 1)
                | (pl.col("DifficultyDressingBathing") == 1)
                | (pl.col("DifficultyErrands") == 1)
            )
            .then(1)
            .when(
                (pl.col("DifficultyWalking") == 2)
                | (pl.col("DifficultyDressingBathing") == 2)
                | (pl.col("DifficultyErrands") == 2)
            )
            .then(0)
            .otherwise(None)
            .cast(pl.Int8)
            .alias("Mobility")
        )
        df: pl.DataFrame = df.drop(
            ["DifficultyWalking", "DifficultyDressingBathing", "DifficultyErrands"]
        )

        df: pl.DataFrame = df.with_columns(
            pl.when(pl.col("SmokerStatus") == 9)
            .then(None)
            .otherwise(pl.col("SmokerStatus"))
            .alias("SmokerStatus")
        )

        df: pl.DataFrame = df.with_columns(
            pl.when(pl.col("HaveHighCholesterol") == 1)
            .then(1)
            .when((pl.col("HaveHighCholesterol") == 2))
            .then(0)
            .otherwise(None)
            .cast(pl.Int8)
            .alias("HaveHighCholesterol")
        )

        return df

    def encode_columns(self, df: pl.DataFrame) -> pl.DataFrame:
        LAST_CHECKUP: dict[int, str] = {
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            7: None,
            8: None,
            9: None,
        }
        df = df.drop_nulls(
            [
                "GeneralHealth",
                "PhysicalHealthDays",
                "MentalHealthDays",
                "HadSkinCancer",
                "HadArthritis",
                "HadDiabetes",
            ]
        )
        df = df.with_columns(
            pl.col("Sex").map_elements(
                lambda x: 0 if x == 2 else x, return_dtype=pl.Int8
            ),
            pl.col("GeneralHealth").map_elements(
                lambda x: None if x == 7 or x == 9 else x, return_dtype=pl.Int8
            ),
            pl.col("PhysicalHealthDays").map_elements(
                lambda x: None if x > 30 else x, return_dtype=pl.Int8
            ),
            pl.col("MentalHealthDays").map_elements(
                lambda x: None if x > 30 else x, return_dtype=pl.Int8
            ),
            pl.col("LastCheckupTime").map_elements(
                LAST_CHECKUP.get, return_dtype=pl.Int8
            ),
            pl.col("PhysicalActivities").map_elements(
                lambda x: None if x == 7 or x == 9 else x, return_dtype=pl.Int8
            ),
            pl.col("HadAsthma").map_elements(
                lambda x: None if x == 7 or x == 9 else x, return_dtype=pl.Int8
            ),
            pl.col("HadSkinCancer").map_elements(
                lambda x: None if x == 7 or x == 9 else x, return_dtype=pl.Int8
            ),
            pl.col("HadCOPD").map_elements(
                lambda x: None if x == 7 or x == 9 else x, return_dtype=pl.Int8
            ),
            pl.col("HadDepressiveDisorder").map_elements(
                lambda x: None if x == 7 or x == 9 else x, return_dtype=pl.Int8
            ),
            pl.col("HadKidneyDisease").map_elements(
                lambda x: None if x == 7 or x == 9 else x, return_dtype=pl.Int8
            ),
            pl.col("HadArthritis").map_elements(
                lambda x: None if x == 7 or x == 9 else x, return_dtype=pl.Int8
            ),
            pl.col("HadDiabetes").map_elements(
                lambda x: None if x == 7 or x == 9 else x, return_dtype=pl.Int8
            ),
            pl.col("AgeCategory").map_elements(
                lambda x: None if x == 14 else x, return_dtype=pl.Int8
            ),
            pl.col("AlcoholDrinkers").map_elements(
                lambda x: None if x == 7 or x == 9 else x, return_dtype=pl.Int8
            ),
            pl.col("HeightInMeters") / 100,
            pl.col("WeightInKilograms") / 100,
            pl.col("BMI") / 100,
        )
        return df

    def merge_cvd(self, df: pl.DataFrame) -> pl.DataFrame:
        df: pl.DataFrame = df.with_columns(
            pl.when(
                (pl.col("HadHeartAttack") == 1)
                | (pl.col("HadAngina") == 1)
                | (pl.col("HadStroke") == 1)
            )
            .then(1)
            .when(
                (pl.col("HadHeartAttack") == 2)
                | (pl.col("HadAngina") == 2)
                | (pl.col("HadStroke") == 2)
            )
            .then(0)
            .otherwise(None)
            .cast(pl.Int8)
            .alias("CVD")
        )

        return df.drop(["HadHeartAttack", "HadAngina", "HadStroke"])
