## Cardiovascular Disease Prediction  
This project focuses on developing a cardiovascular disease prediction model, which will be integrated into a React/Flask web application. The model will analyze user inputs to assess CVD risk efficiently.

## Installation Guide

There are several ways you can install the application
<!-- <details>  -->
<!-- <summary><code>There are several ways you can install the application</code></summary>  -->

1. **Clone the repository**:
    ```sh
    git clone https://github.com/carrot2803/cvd-predictor.git
    cd cvd-predictor
    ```

2. **(Optional) Create a virtual environment**:

    - Using `venv`:
        ```sh
        python -m venv venv
        source venv/bin/activate    # On Windows use `venv\Scripts\activate`
        ```
    - Using `conda`:
        ```sh
        conda create --name your-env-name python=3.x
        conda activate your-env-name
        ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

#### **Alernative**
- [Downloading repository as ZIP](https://github.com/carrot2803/cvd-predictor/archive/refs/heads/master.zip)
- Running the following command in a terminal, assuming you have [GitHub CLI](https://cli.github.com/) installed:

<!-- </details> -->

## Getting Started  

First, run `variable_layout.py` to scrape variable names from the CSV. Next, execute `convert_ascii.R` to process `LLCP2023.ASC`. Once converted, run the initial processing notebook, followed by the training notebook to begin model training.  
All raw source files will be available on SharePoint soon.

## Outstanding Todos  

- [x] Balance Data – Scrapped SMOTE bad 
- [x] Optimize Models – Tune hyperparameters for Logistic Regression, Random Forest, and XGBoost.  
- [x] Streamline Data Cleaning – Finalize categorical encoding and outlier handling.  
- [x] Automate Data Conversion – Improve .ascii to CSV pipeline, removing manual steps.  
- [ ] Ensure Data Access – Secure alternative documentation retrieval methods.  

## Package Structure

    root/                          
    ├── notebooks/
    │   └── training.ipynb
    ├── scripts/
    │   └── convert_ascii.R
    ├── data/
    │   └── raw/
    │       └── LLCP2023.ASC
    ├── .gitignore
    ├── Readme.md
    └── requirements.txt