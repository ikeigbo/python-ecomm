import os, time, random, requests
from fastapi import FastAPI, HTTPException

FAIL_RATE=float(os.getenv("FAIL_RATE",0))
STARTUP_DELAY=int(os.getenv("STARTUP_DELAY",0))
INVENTORY_URL=os.getenv("INVENTORY_URL","http://inventory-service:8000")

app=FastAPI(title="order-service")

@app.on_event("startup")
def startup(): time.sleep(STARTUP_DELAY)

@app.get("/health")
def health(): return {"status":"ok"}

@app.get("/ready")
def ready(): return {"ready":True}

@app.post("/orders")
def create_order(item_id:str, quantity:int):
    if random.random()<FAIL_RATE:
        raise HTTPException(500,"Injected failure")

    r=requests.post(f"{INVENTORY_URL}/reserve",
        json={"item_id":item_id,"quantity":quantity},timeout=2)

    if r.status_code!=200:
        raise HTTPException(503,"Inventory unavailable")

    return {"order_id":random.randint(1000,9999),"status":"created"}
