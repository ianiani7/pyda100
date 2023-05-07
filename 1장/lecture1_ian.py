import pandas as pd

customer_master = pd.read_csv(r"C:\Users\InSeong\Desktop\Coding\pyda100\1장\customer_master.csv")
item_master = pd.read_csv(r"C:\Users\InSeong\Desktop\Coding\pyda100\1장\item_master.csv")
transaction_1 = pd.read_csv(r"C:\Users\InSeong\Desktop\Coding\pyda100\1장\transaction_1.csv")
transaction_2 = pd.read_csv(r"C:\Users\InSeong\Desktop\Coding\pyda100\1장\transaction_2.csv")
detail_1 = pd.read_csv(r"C:\Users\InSeong\Desktop\Coding\pyda100\1장\transaction_detail_1.csv")
detail_2 = pd.read_csv(r"C:\Users\InSeong\Desktop\Coding\pyda100\1장\transaction_detail_2.csv")

#dataframe 결합
transaction = pd.concat([transaction_1,transaction_2],ignore_index=True)
detail = pd.concat([detail_1,detail_2],ignore_index=True)
total = pd.merge(detail,transaction[['transaction_id','payment_date','customer_id']],on='transaction_id',how='left')
total = pd.merge(total,customer_master,on='customer_id')
total = pd.merge(total,item_master,on='item_id')
total['price']=total['item_price']*total['quantity']

#검산
print(transaction['price'].sum()==total['price'].sum())

#통계량 파악
total.isnull().sum()
total.describe()

#groupby
total.dtypes
total['payment_date'] = pd.to_datetime(total['payment_date'])
total['payment_month'] = total['payment_date'].dt.strftime('%y%m')
total.groupby('payment_month').sum()["price"]
total_monthly = total.groupby(['payment_month','item_name']).sum()[['price',"quantity"]]

#pivot_table: 엑셀의 피벗테이블 기능
price_monthly = pd.pivot_table(total, index = 'payment_month', columns = 'item_name', values = 'price', aggfunc = 'sum')
price_monthly.plot()
