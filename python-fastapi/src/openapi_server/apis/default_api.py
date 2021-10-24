# coding: utf-8
import json
from typing import Dict, List  # noqa: F401

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import String

#from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.work import Work
from openapi_server.models.work_registration_result import WorkRegistrationResult

from sql_app.database import SessionLocal, engine
from sql_app.models import PipelineWork

PipelineWork.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def _jencode(d:Dict) -> String:
    return json.dumps(d, sort_keys=True, separators=(',',':'))


router = APIRouter()


@router.get(
    "/pipeline/{pipeline_id}/claim_work",
    responses={
        200: {"model": List[Work], "description": "enumerate work claimed"},
    },
    tags=["default"],
    summary="Claim work to be done by a pipeline",
)
async def pipeline_pipeline_id_claim_work_get(
    pipeline_id: str = Path(None, description="", max_length=64),
    max_items: int = Query(1, description=""),
    db: Session = Depends(get_db)
) -> List[Work]:
    results =[]
    db_work = db.query(PipelineWork).filter(PipelineWork.pipeline_id==pipeline_id).filter(PipelineWork.claimed==False).limit(max_items) #.with_for_update(nowait=True, of=PipelineWork)
    for db_workitem in db_work:
        db_workitem.claimed=True
        db.commit()
        results.append(Work(unique=json.loads(db_workitem.unique),info=json.loads(db_workitem.info)))
    return results


@router.post(
    "/pipeline/{pipeline_id}/register_work",
    responses={
        200: {"model": WorkRegistrationResult, "description": "enumerate work newly registered, pre-existing, and any failed to register"},
    },
    tags=["default"],
    summary="Registers work to be done by a pipeline",
)
async def pipeline_pipeline_id_register_work_post(
    pipeline_id: str = Path(None, description="", max_length=64),
    work: List[Work] = Body(None, description=""),
    db: Session = Depends(get_db)
) -> WorkRegistrationResult:
    results = WorkRegistrationResult()
    for workitem in work:
        print(workitem) 
        unique = _jencode(workitem.unique)
        if db.query(PipelineWork).filter(PipelineWork.pipeline_id==pipeline_id).filter(PipelineWork.unique==unique).count():
            results.preexisting.append(workitem)
        else:
            db_work=PipelineWork(pipeline_id=pipeline_id, unique=unique, info=_jencode(workitem.info))
            db.add(db_work)
            db.commit()
            results.created.append(workitem)
        # results.errored.append(workitem)
    return results
