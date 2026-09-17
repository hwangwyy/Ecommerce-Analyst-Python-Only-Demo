# Python Only ETL pipeline project using pandas, dataset from kaggle.
This project relies heavily on the pandas library to Extract, Transform and Load data.
Note: The juptyter notebook itself is just for reporting analytical data that have been processed.
How the project works:
1. Ingest the dataset using kagglehub. Download the dataset.
2. Add all the raw dataset to one raw_df_ls.
3. Start the transforming stage using pandas in transformer package.
4. Save the data as a csv local file for analytic purpose.
# How to run project
Install dependencies
```python
pip install -r requirements.txt
```
Run the main pipeline
```python
python main.py
```
Or using python3:
```python
python3 main.py
```
