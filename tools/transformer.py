import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger=logging.getLogger(__name__)

def view_data(df: pd.DataFrame):
    print("===========HEAD==============")
    print(df.head(5))
    print("===========SHAPE==============")
    print(f"Dimension: {df.shape}")
    print("===========DESCRIBE==============")
    print(df.describe(include='all'))
    print("===========INFO==============")
    print(df.info())
    print("===========TOTAL_NULL_SUM==============")
    print(df.isna().sum())


# SILVER LAYER
def column_format(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip()
    logger.info("Columns formatted")
    return df

def clean_customer(df: pd.DataFrame) -> pd.DataFrame:
    df = column_format(df)
    df = df.drop_duplicates(keep='first')
    logger.info("Dropped duplicates")
    df['Age'] = df['Age'].fillna(df['Age'].mean())
    logger.info("Filled Age Null values to mean")
    df['Age'] = df['Age'].astype(int)
    logger.info("Changed Age dtype to int")
    df = df.dropna(subset='City')
    logger.info("Dropped Null values from City")
    df['SignupDate'] = pd.to_datetime(df['SignupDate'])
    logger.info("Formatted SignupDate to type datetime")
    return df

def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    column_format(df)
    df = df.drop_duplicates(keep='last')
    logger.info("Dropped duplicates")
    df = df.dropna(subset='OrderDate')
    logger.info("Dropped OrderDate Null values")
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    logger.info("Formatted OrderDate dtype to date")
    df['Discount'] = df['Discount'].fillna(0)
    logger.info("Filled Discount Null values with 0")
    df = df.dropna(subset='Quantity')
    df['Quantity'] = df['Quantity'].astype(int)
    logger.info("Changed dtype from float to int for Quantity column")
    df = df[df['Quantity'] > 0]
    logger.info("Dropped outlier values in Quantity column")
    df['PaymentMethod'] = df['PaymentMethod'].fillna('Cash')
    logger.info("Filled Null value from PaymentMethod to Cash")
    return df #type: ignore

def clean_payments(df: pd.DataFrame) -> pd.DataFrame:
    column_format(df)
    df = df.drop_duplicates(keep='last')
    logger.info("Dropped duplicates")
    df = df.dropna(subset='PaymentDate')
    logger.info("Dropped Null values from PaymentDate")
    df['PaymentDate'] = pd.to_datetime(df['PaymentDate'])
    logger.info("Changed PaymentDate to type date")
    return df

def clean_products(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Nothing to clean. Start working on next step")
    return df

# GOLD LAYER
def to_analytics(df_ls: dict[str, pd.DataFrame]) -> pd.DataFrame:
    logger.info("Starting transform cleaned data to ready to use data for analytics")
    customers_df = df_ls['customers.csv']
    products_df = df_ls['products.csv']
    payments_df = df_ls['payments.csv']
    orders_df = df_ls['orders.csv']
    orders_1 = pd.merge(customers_df, orders_df, on='CustomerID', how='inner')
    orders_2 = pd.merge(orders_1, products_df, on='ProductID', how='inner')
    df = pd.merge(orders_2, payments_df, on='OrderID', how='inner')
    df = df.drop(columns=['SignupDate', 'PaymentDate'])
    return df