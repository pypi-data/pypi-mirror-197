def get_job_run_url(host: str, job_id: str, run_id: str) -> str:
    """
    Return Databricks Job Run URL.
    :param host: Databricks host
    :param job_id: Databricks Workflow Job Identifier
    :param run_id: Databricks Workflow Job Run Identifier

    :return: URL which the user can click to visualise the job in the Databricks UI.
    """
    return f"https://{host}/#job/{job_id}/run/{run_id}"