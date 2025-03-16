"""
Run variable layout script first
"""

columns <- read.csv("data/2023-variable-layout.csv")

columns$File_Width <- sapply(1:nrow(columns), function(y) {
    ifelse(y < nrow(columns),
        columns$Starting_Column[y + 1] - columns$Starting_Column[y], 1
    )
})

columns <- columns[columns$File_Width > 0, ]


responses <- read.fwf("data/LLCP2023ASC/LLCP2023.ASC", widths = columns$File_Width, col.names = columns$Variable_Name)
print("read successfully")
