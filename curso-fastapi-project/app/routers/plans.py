from fastapi import APIRouter
from sqlmodel import select

from models import Plan
from db import SessionDep
router = APIRouter()


@router.get('/plans', response_model=list[Plan], tags=["Plans"])
async def list_plans(session: SessionDep):
    sentence = select(Plan)
    plans_db = session.exec(sentence).all()
    return plans_db


@router.post('/plans', response_model=Plan, tags=["Plans"])
async def create_plan(plan_data:Plan, session: SessionDep):
    plan_db = Plan.model_validate(plan_data.model_dump())
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db