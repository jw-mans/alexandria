from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from . import repository, schemas, models
from .database import get_db

router = APIRouter()


@router.post("/runs", response_model=schemas.RunSchema)
def create_run(run: schemas.RunSchema, db: Session = Depends(get_db)):
    print(f"BACKEND: Received run {run.id}")
    print(f"   Parameters: {run.parameters}")
    print(f"   Metrics: {run.metrics}")
    db_run = repository.get_run(db, run.id)
    if db_run:
        raise HTTPException(status_code=400, detail="Run already exists")
    return repository.create_run(db, run)


@router.get("/runs", response_model=list[schemas.RunSchema])
def list_runs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return repository.list_runs(db, skip=skip, limit=limit)


@router.get("/runs/{run_id}", response_model=schemas.RunSchema)
def get_run(run_id: str, db: Session = Depends(get_db)):
    db_run = repository.get_run(db, run_id)
    if not db_run:
        raise HTTPException(status_code=404, detail="Run not found")
    return db_run


@router.get("/runs/{run_id}/diff/{other_id}")
def diff_runs(run_id: str, other_id: str, db: Session = Depends(get_db)):
    run1 = repository.get_run(db, run_id)
    run2 = repository.get_run(db, other_id)
    if not run1 or not run2:
        raise HTTPException(status_code=404, detail="Run not found")
    return repository.diff_runs(run1, run2)
