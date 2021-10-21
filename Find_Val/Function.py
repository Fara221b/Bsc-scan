import asyncio
from bscscan import BscScan
import numpy as np
import pandas as pd
from datetime import timedelta


async def main(address,offset):
    async with BscScan('SCSKHAVMN19QAFCNSII2N6UADH89M8TAKV') as client:
        return await client.get_bep20_token_transfer_events_by_contract_address_paginated(contract_address= address, page=1,offset=offset,sort="desc")


def connect(contract_address,offset):
	return asyncio.run(main(contract_address,offset))


def find_val(data,time):
	df = pd.DataFrame(data,columns=["timeStamp","from","to","value"])
	df['DateTime'] = pd.to_datetime(df['timeStamp'], unit='s')
	
	TIME=df['DateTime'].mode()[0]
	pump_time=TIME.floor(freq = '15min')
	time0 = pump_time.floor('D')
	time1= pump_time + timedelta(minutes=time)
	
	df_before = df.loc[(df['DateTime']> time0) & (df['DateTime']< pump_time)]
	df_after = df.loc[(df['DateTime']> pump_time) & (df['DateTime']< time1)]
	
	pancake =df['from'].mode()[0]
	
	suspect_be = df_before['to'].unique()
	suspect_af = df_after[df_after['from'] != pancake]['from'].unique()

	val = np.intersect1d(suspect_af,suspect_be)
	
	return {'val':val,'suspectes':suspect_be, 'pump time':pump_time, 'Token Name':data[0]['tokenName']}


def fetch_data(contract_address,offset=1000,time=1):
	data = connect(contract_address,offset)
	return find_val(data,time)
