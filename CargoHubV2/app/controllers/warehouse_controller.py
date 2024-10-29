from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="api/v2/warehouse",
    tags=["warehouses"]
)


@router.get("/")
def get_warehouses():
    NotImplementedError()
    # warehouses uit database halen en in variabele stoppen
    # de warehouses returnen


@router.post("/")
def create_warehouse(warehouse):
    # service aanroepen die de warehouse toevoegt aan db
    # resultaat van de service gaat in db_warehouse
    db_warehouse = ""
    if db_warehouse is None:
        raise HTTPException(status_code=400, detail="User already exists")
    return db_warehouse
