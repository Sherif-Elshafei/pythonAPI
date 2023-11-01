import json
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()

class Traders(BaseModel):
	id: Optional[int] = None
	name : str
	age : int
	company : str

with open('traders.json', 'r') as f:
	traders = json.load(f)

@app.get('/trader/{t_id}', status_code=200)
def get_trader(t_id : int):
	trader = [t for t in traders if t['id'] == t_id] #building a python list from traders
	return trader[0] if len(trader) > 0 else {}

@app.get('/search', status_code=200)
def search_trader(age: Optional[int] = Query(None, title="Age", description="The age to filter for"),
				  name: Optional[str] = Query(None, title="Name", description="The name to filter for")):
	trader1 = [t for t in traders if t['age'] == age]

	if name is None:
		if age is None:
			return traders
		else:
			return trader1
		
	else:
		trader2=[t for t in traders if name.lower() in t['name'].lower()]
		if age is None:
			return trader2
		else:
			combined = [t for t in trader1 if t in trader2]
			return combined

@app.post('/addTrader', status_code=201)
def add_trader(trader:Traders):
	t_id = max ([t['id'] for t in traders])+1
	new_trader = {
		"id": t_id,
		"name": trader.name,
		"age": trader.age,
		"company": trader.company
	}

	traders.append(new_trader)

	with open('traders.json', 'w') as f:
		json.dump(traders,f)

	return new_trader

@app.put('/changeTrader', status_code=204)
def change_trader(trader: Traders):
	new_trader = {
		"id": trader.id,
		"name": trader.name,
		"age": trader.age,
		"company": trader.company
	}

	trader_list = [t for t in traders if t['id'] == trader.id]
	if len(trader_list) > 0:
		traders.remove(trader_list[0])
		traders.append(new_trader)
		with open('traders.json', 'w') as f:
			json.dump(traders,f)
		return new_trader
	else:
		return HTTPException(status_code=404, detail=f"Trader with id {trader.id} doesn't exist!")

@app.delete('/deleteTrader/{t_id}', status_code=204)
def delete_trader(t_id:int):
	trader = [t for t in traders if t['id'] == t_id]
	if len(trader) > 0:
		traders.remove(trader[0])
		with open('traders.json', 'w') as f:
			json.dump(traders,f)	#it will take care of duplication
	else:
		raise HTTPException(status_code=404, detail=f"There is no trader with id {t_id}.")

