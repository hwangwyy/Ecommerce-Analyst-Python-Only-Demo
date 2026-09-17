import pandas as pd
import logging

from pathlib import Path
from scripts import downloader
from tools import transformer

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    raw_df_ls: dict[str, pd.DataFrame] = {} # BRONZE

    # PHASE: EXTRACT
    try:
        url = "erfan4524/e-commerce-sales-data-analysis-and-eda"
        data_path = 'data/'
        downloader.dataset_download(url, output_dir=data_path)

        for file in Path(data_path).iterdir():
            file_name = Path(file).name
            if file.is_file() and file_name.find("*.csv") and not file_name == "clean_final_data.csv":
                logger.info(f"CSV founded. Name: {file_name}.")
                raw_df_ls[file_name] = pd.read_csv(f"{data_path}/{file_name}") # type: ignore
                logger.info(f"Added {file_name} to raw_df_ls.")
    except Exception as e:
        logger.error(f"An exception occurred: {e}")

    df_ls: dict[str, pd.DataFrame] = {}

    # PHASE: TRANSFORM || SILVER
    # Cleaning phase
    for csv in raw_df_ls:
        # Customers pipeline
        if csv == "customers.csv":
            logger.info(f"Start cleaning {csv}")
            raw_df = raw_df_ls[csv]
            df_ls[csv] = transformer.clean_customer(raw_df)
        elif csv == "orders.csv":
            logger.info(f"Start cleaning {csv}")
            raw_df = raw_df_ls[csv]
            df_ls[csv] = transformer.clean_orders(raw_df)
        elif csv == "payments.csv":
            logger.info(f"Start cleaning {csv}")
            raw_df = raw_df_ls[csv]
            df_ls[csv] = transformer.clean_payments(raw_df)
        elif csv == "products.csv":
            logger.info(f"Start cleaning {csv}")
            raw_df = raw_df_ls[csv]
            df_ls[csv] = transformer.clean_products(raw_df)

    # PHASE: TRANSFORM || GOLD
    df = transformer.to_analytics(df_ls)
    # PHASE: LOAD
    path=Path('data/transformed/')
    path.mkdir(parents=True, exist_ok=True)
    df.to_csv(f'{path}/final.csv')

if __name__ == "__main__":
    main()