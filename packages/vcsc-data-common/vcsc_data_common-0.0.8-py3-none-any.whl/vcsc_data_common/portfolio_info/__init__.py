from sqlalchemy import create_engine
import pandas as pd


class PortfolioInfo:
    def __init__(self, paper_trading_db_host: str, paper_trading_db_port: int, paper_trading_db_username: str,
                 paper_trading_db_password: str, paper_trading_db_name: str):
        self.paper_trading_db_host = paper_trading_db_host
        self.paper_trading_db_port = paper_trading_db_port
        self.paper_trading_db_username = paper_trading_db_username
        self.paper_trading_db_password = paper_trading_db_password
        self.paper_trading_db_name = paper_trading_db_name

        paper_trading_db_connection_str = f'postgresql://{paper_trading_db_username}:{paper_trading_db_password}@{paper_trading_db_host}:{paper_trading_db_port}/{paper_trading_db_name}'
        self.paper_trading_db_connection = create_engine(
            paper_trading_db_connection_str).connect()

    def get_all_portfolio(self):
        return pd.read_sql(f"""  

            with stock_portfolio as (
                select t3.id as "portfolioId",t1.username,t1.symbol,COALESCE("latestMatchPrice",0) as "latestMatchPrice","totalAmount","availableAmount", "averageMatchedPrice","targetPercent"
                from "portfolio" t1
                left join "symbol_info" t2 on t1.symbol = t2.symbol
                left join "cash" t3 on t1.username = t3.username
                WHERE t1.symbol != 'CASH'
            )
            , cash_portfolio as (
                select t1."id" as "portfolioId",t1.username,'CASH' as symbol, 0::double precision as "latestMatchPrice",
                "currentCash" + "blockedCash" as "totalAmount", "currentCash" + "blockedCash" as "availableAmount",
                0::double precision as "averageMatchedPrice",t2."targetPercent"
                from "cash" t1 
                left join 
                (SELECT * FROM "portfolio" WHERE symbol = 'CASH') t2 on t1.username = t2.username
            )

            select * from stock_portfolio 
            union all
            select * from cash_portfolio

        """, con=self.paper_trading_db_connection)

    def update_target_percent_portfolio(self, portfolio_data: dict):

        for key in portfolio_data:
            target_percent = portfolio_data[key]

            self.paper_trading_db_connection.execute(
                f""" UPDATE portfolio set "targetPercent" = {target_percent}  WHERE symbol = '{key}' """)
