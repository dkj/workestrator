# coding: utf-8

from fastapi.testclient import TestClient

def test_pipeline_pipeline_id_claim_work_put(client: TestClient):
    """Test case for pipeline_pipeline_id_claim_work_put

    Claim work to be done by a pipeline
    """
    params = [("max_items", 1)]
    headers = {
    }
    response = client.request(
        "PUT",
        "/pipeline/{pipeline_id}/claim_work".format(pipeline_id='pipeline_id_example'),
        headers=headers,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200


def test_pipeline_pipeline_id_register_work_post(client: TestClient):
    """Test case for pipeline_pipeline_id_register_work_post

    Registers work to be done by a pipeline
    """
    work = [{"unique":{"run":1234,"lane":5,"tag_index":6},"info":{"species":"Homo sapiens","library_type":"cell partitioned RNA expression"}}]

    headers = {
    }
    response = client.request(
        "POST",
        "/pipeline/{pipeline_id}/register_work".format(pipeline_id='pipeline_id_example'),
        headers=headers,
        json=work,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200

