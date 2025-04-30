## Cardiovascular Disease Prediction  
This project involves developing a cardiovascular disease prediction model, which will be integrated into a React/Flask web application. The model analyzes user inputs to efficiently assess CVD risk.

This repository contains the backend with all core data science logic. The frontend UI can be found [here](https://github.com/carrot2803/cvd-app) or in the About section.


## Installation Guide

<details> 
<summary><code>There are several ways you can install the application</code></summary> 

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
    ```sh
        gh repo clone carrot2803/reading-skills-annotator
        cd reading-skills-annotator
    ```
After obtaining the code using one of the above methods, follow steps 2 and 3 from the main installation guide to set up a virtual environment and install the required packages.

</details>

## Getting Started  

<details>
<summary><code>To begin using the project, there are three recommended options:</code></summary>

Start by running `variable_layout.py` to extract variable names from the [CDC website](https://www.cdc.gov/brfss/annual_data/2023/llcp_varlayout_23_onecolumn.html). Then, execute `convert_ascii.R` to process `LLCP2023.ASC`. Once converted, run the initial processing notebook, followed by the training notebook to begin model training.

All raw source files are available on [SharePoint](https://bit.ly/4jVDfJQ).

1. **Running the Predefined Scripts**

    - **Command-Line Script** (`main.py`):  
    Run this script from the terminal:
    ```bash
        python main.py
    ```

    - **Web Application Script** (`app.py`):  
    Launch the web interface:
    ```bash
        python app.py
    ```
    
    View the web API at: [demo link](https://cvd-predictor.azurewebsites.net)  
    View the web UI at: [demo link](https://carrot2803.github.io/cvd-app)

2. **Exploring the Jupyter Notebooks**  

    Located in the `/notebooks` folder:

    
    - `demo.ipynb`: Practical demonstration
    - `EDA.ipynb`: Exploratory data analysis
    - `initial_processing.ipynb`: Initial data cleaning steps
    - `training.ipynb`: Model training process

3. **Setting Up the CVD Predictor Manually**  

You can also create your own Python file and initialize the predictor:

```python
from CVD import CVDClassifier

# Specify your sample JSON file
sample_json = "~/~.json"

# Instantiate the CVD Classifier
cvd = CVDClassifier()

# Print the prediction and top contributing feature
print(cvd.predict(sample_json))
```

Replace `sample_json` with the path to your own JSON-formatted data. This example demonstrates how to integrate the CVD predictor into a custom setup.

</details>

## Routes

### Core Routes

1. <u>/</u> [GET]: Returns "Healthy" with the corresponding status code.  
2. <u>/predict</u> [POST]: Returns a CVD prediction and the top 5 contributing factors.

## Outstanding Todos  

- [x] Balance Data – Scrapped SMOTE bad 
- [x] Optimize Models – Tune hyperparameters for Logistic Regression, Random Forest, and XGBoost.  
- [x] Streamline Data Cleaning – Finalize categorical encoding and outlier handling.  
- [x] Automate Data Conversion – Improve .ascii to CSV pipeline, removing manual steps.  
- [ ] Ensure Data Access – Secure alternative documentation retrieval methods.  

## Package Structure

    root/
    ├── CVD/
    │   ├── models/
    │   │   └── classifier.py      # predictive model
    │   ├── utils/                 # helper functions
    │   │   └── encode.py 
    │   ├── visuals/               # model visulization 
    │   │   └── bar.py
    │   └── constants.py                     
    ├── notebooks/                 # scientific notebooks 
    │   └── training.ipynb
    ├── scripts/                   # scraping and feature selection
    │   └── convert_ascii.R
    ├── data/
    │   ├── models/                # pickled tuned models
    │   │   └── lgb_cvd.pkl
    │   ├── processed/             # pngs and html visualizations
    │   │   ├── html/
    │   │   └── imgs/
    │   ├── intermediate/          # intermidate data 
    │   │   └──heart_cdc_2023.csv
    │   └── raw/                   # unrefined data 
    │       └── LLCP2023.ASC
    ├── .gitignore
    ├── main.py                    # main script
    ├── app.py                     # rest web api
    ├── Readme.md
    └── requirements.txt  
