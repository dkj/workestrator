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
from openapi_server.models.work_update_result import  WorkUpdateResult

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


@router.put(
    "/pipeline/{pipeline_id}/claim_work",
    responses={
        200: {"model": List[Work], "description": "enumerate work claimed"},
    },
    tags=["default"],
    summary="Claim work to be done by a pipeline",
)
async def pipeline_pipeline_id_claim_work_put(
    pipeline_id: str = Path(None, description="", max_length=64),
    max_items: int = Query(1, description=""),
    db: Session = Depends(get_db)
) -> List[Work]:
    results =[]
    db_work = db.query(PipelineWork).filter(PipelineWork.pipeline_id==pipeline_id).filter(PipelineWork.state=="PENDING").limit(max_items) #.with_for_update(nowait=True, of=PipelineWork)
    for db_workitem in db_work:
        db_workitem.state="CLAIMED"
        db.commit()
        results.append(Work(unique=json.loads(db_workitem.unique),info=json.loads(db_workitem.info),state=db_workitem.state))
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
        unique = _jencode(workitem.unique)
        db_workitem = db.query(PipelineWork).filter(PipelineWork.pipeline_id==pipeline_id).filter(PipelineWork.unique==unique).filter(PipelineWork.state!="ANNULLED").one_or_none()
        if db_workitem:
            results.preexisting.append(Work(unique=json.loads(db_workitem.unique),info=json.loads(db_workitem.info),state=db_workitem.state))
        else:
            db_workitem=PipelineWork(pipeline_id=pipeline_id, unique=unique, info=_jencode(workitem.info))
            db.add(db_workitem)
            db.commit()
            results.created.append(Work(unique=json.loads(db_workitem.unique),info=json.loads(db_workitem.info),state=db_workitem.state))
        # results.errored.append(workitem) # TODO catch errors per item and put here...
    return results

@router.put(
    "/pipeline/{pipeline_id}/update_work",
    responses={
        200: {"model": WorkUpdateResult, "description": "enumerate work updated, any failures to update"},
    },
    tags=["default"],
    summary="Updates state, or info, of work done by a pipeline",
)
async def pipeline_pipeline_id_update_work_put(
    pipeline_id: str = Path(None, description="", max_length=64),
    work: List[Work] = Body(None, description=""),
    db: Session = Depends(get_db)
) -> WorkUpdateResult:
    results = WorkUpdateResult()
    for workitem in work:
        unique = _jencode(workitem.unique)
        db_workitem = db.query(PipelineWork).filter(PipelineWork.pipeline_id==pipeline_id).filter(PipelineWork.unique==unique).filter(PipelineWork.state!="ANNULLED").one_or_none()
        if db_workitem:
            if workitem.state:
              db_workitem.state = workitem.state
            if workitem.info:
              db_workitem.info = _jencode(workitem.info)
            db.commit()
            results.updated.append(Work(unique=json.loads(db_workitem.unique),info=json.loads(db_workitem.info),state=db_workitem.state))
        else:
            results.errored.append(workitem)
        # results.errored.append(workitem)  # TODO catch errors per item and put here...
    return results
