from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from . import repository, schemas, models
from .database import get_db

router = APIRouter()


# @router.post("/runs", response_model=schemas.RunSchema)
# def create_run(
#     run: schemas.RunSchema, 
#     db: Session = Depends(get_db)
# ):
#     db_run = repository.get_run(db, run.id)
#     if db_run:
#         raise HTTPException(status_code=400, detail="Run already exists")
    
#     run_dict = run.model_dump(mode='json')
#     created = repository.create_run(db, run_dict)
#     return created


# @router.get("/runs", response_model=list[schemas.RunSchema])
# def list_runs(
#     skip: int = 0, 
#     limit: int = 100, 
#     db: Session = Depends(get_db)
# ):
#     return repository.list_runs(db, skip=skip, limit=limit)


# @router.get("/runs/{run_id}", response_model=schemas.RunSchema)
# def get_run(
#     run_id: str, 
#     db: Session = Depends(get_db)
# ):
#     db_run = repository.get_run(db, run_id)
#     if not db_run:
#         raise HTTPException(status_code=404, detail="Run not found")
#     return db_run


# @router.get("/runs/{run_id}/diff/{other_id}")
# def diff_runs(
#     run_id: str, 
#     other_id: str, 
#     db: Session = Depends(get_db)
# ):
#     run1 = repository.get_run(db, run_id)
#     run2 = repository.get_run(db, other_id)
#     if not run1 or not run2:
#         raise HTTPException(status_code=404, detail="Run not found")
#     return repository.diff_runs(run1, run2)

# @router.get("/datasets")
# def list_datasets(
#     skip: int = 0,
#     limit: int = 100,
#     db: Session = Depends(get_db)
# ):
#     """
#     Returns dataset-objects list from runs.
#     Building agregate by run.dataset.
#     """
#     runs = repository.list_runs(db,skip=skip, limit=limit)
#     datasets=[]
#     seen = set()
#     for r in runs:
#         ds = r.dataset or {}
#         ds_hash = ds.get('hash')
#         if ds_hash and ds_hash not in seen:
#             seen.add(ds_hash)
#             datasets.append(ds)
#         elif not ds_hash:
#             datasets.append(ds)
#     return datasets

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from . import repository, schemas
from .database import get_db

router = APIRouter()


@router.post("/runs", response_model=schemas.RunSchema)
def create_run(run: schemas.RunSchema, db: Session = Depends(get_db)):
    db_run = repository.get_run(db, run.id)
    if db_run:
        raise HTTPException(status_code=400, detail="Run already exists")

    run_dict = run.model_dump(mode='json')
    created = repository.create_run(db, run_dict)
    return repository.serialize_run(created)


@router.get("/runs", response_model=list[schemas.RunSchema])
def list_runs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    runs = repository.list_runs(db, skip=skip, limit=limit)
    return [repository.serialize_run(r) for r in runs]


@router.get("/runs/{run_id}", response_model=schemas.RunSchema)
def get_run(run_id: str, db: Session = Depends(get_db)):
    db_run = repository.get_run(db, run_id)
    if not db_run:
        raise HTTPException(status_code=404, detail="Run not found")
    return repository.serialize_run(db_run)


@router.get("/runs/{run_id}/diff/{other_id}")
def diff_runs(run_id: str, other_id: str, db: Session = Depends(get_db)):
    run1 = repository.get_run(db, run_id)
    run2 = repository.get_run(db, other_id)
    if not run1 or not run2:
        raise HTTPException(status_code=404, detail="Run not found")
    return repository.diff_runs(db, run1, run2)


@router.get("/datasets")
def list_datasets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    runs = repository.list_runs(db, skip=skip, limit=limit)
    datasets = []
    seen = set()
    for r in runs:
        ds = repository.serialize_run(r).get("dataset") or {}
        ds_hash = ds.get('hash')
        if ds_hash and ds_hash not in seen:
            seen.add(ds_hash)
            datasets.append(ds)
        elif not ds_hash:
            datasets.append(ds)
    return datasets
