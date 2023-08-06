import json

import mock
import responses
from click.testing import CliRunner
from responses import matchers
from gantry.cli.data_connector import (
    create,
    delete,
    list,
    list_pipelines,
    list_pipeline_operations,
    delete_pipeline,
)

UNITTEST_HOST = "http://unittest"
DATA_CONNECTOR_NAME = "test_data_connector"
DATA_CONNECTOR_1_ID = "0db220e0-f568-4295-be48-67095fa57f34"
DATA_CONNECTOR_2_ID = "9e09947e-fb18-4ce3-bd17-7c386a3c9980"
DATA_CONNECTOR_ENABLED_STATUS_CMD = "enabled"
DATA_CONNECTOR_ENABLED_STATUS = "True"
DATABASE_NAME = "test_database"
CONNECTION_TYPE = "SNOWFLAKE"
DESCRIPTION = "Data connector to log records from my snowflake database"
SECRET_NAME = "test_secret"
OPTIONS = '{"schema_name": "PUBLIC","table_name": "GANTRY_EVENTS"}'
APP_NAME = "test_app"
METADATA_ID = "09a26daf-7edb-4e94-aa57-31315ae1a31a"
PIPELINE_NAME = "test_pipeline"
PIPELINE_OPERATION_STATUS = "QUEUED"
PIPELINE_OPERATION_ID = "b4bc71af-37b7-4460-b66c-7ef078949c41"
PIPELINE_ID = "b4bc71af-37b7-4460-b66c-7ef078949c41"
PIPELINE_CONSUMER_ID = "3318762f-a684-480c-b418-d5adcdcb5dc6"
APP_VERSION = "1.0.0"


def test_create_data_connector():
    runner = CliRunner()
    cli_args = [
        "--name",
        DATA_CONNECTOR_NAME,
        "--database-name",
        DATABASE_NAME,
        "--connection-type",
        CONNECTION_TYPE,
        "--secret-name",
        SECRET_NAME,
        "--description",
        DESCRIPTION,
        "--options",
        OPTIONS,
    ]

    with responses.RequestsMock() as resp:
        resp.add(
            resp.POST,
            f"{UNITTEST_HOST}/api/v1/data-connectors/sources",
            json={
                "response": "ok",
                "data": {
                    "connection_type": CONNECTION_TYPE,
                    "created_at": "2023-01-18T00:18:01.000000",
                    "database_name": DATABASE_NAME,
                    "description": DESCRIPTION,
                    "id": DATA_CONNECTOR_1_ID,
                    "name": DATABASE_NAME,
                    "options": {"schema_name": "PUBLIC", "table_name": "GANTRY_EVENTS"},
                    "secret_name": SECRET_NAME,
                    "type": "SOURCE",
                    "updated_at": "2023-01-18T00:18:01.000000",
                },
            },
            headers={"Content-Type": "application/json"},
            match=[
                matchers.json_params_matcher(
                    {
                        "name": DATA_CONNECTOR_NAME,
                        "database_name": DATABASE_NAME,
                        "connection_type": CONNECTION_TYPE,
                        "secret_name": SECRET_NAME,
                        "description": DESCRIPTION,
                        "options": json.loads(OPTIONS),
                    }
                )
            ],
        )

        result = runner.invoke(
            create,
            cli_args,
            env={"GANTRY_API_KEY": "test", "GANTRY_LOGS_LOCATION": UNITTEST_HOST},
        )

        assert result.exit_code == 0
        assert "--> A source data connector has been created" in result.output


def test_create_data_connector_input_validation_failure():
    """
    Tests that invalid connection type throws an error
    """
    runner = CliRunner()
    cli_args = [
        "--name",
        DATA_CONNECTOR_NAME,
        "--database-name",
        DATABASE_NAME,
        "--connection-type",
        "NOT_VALID_TYPE",
        "--secret-name",
        SECRET_NAME,
        "--description",
        DESCRIPTION,
        "--options",
        OPTIONS,
    ]

    result = runner.invoke(
        create,
        cli_args,
        env={"GANTRY_API_KEY": "test", "GANTRY_LOGS_LOCATION": UNITTEST_HOST},
    )

    assert result.exit_code == 2
    assert "Error: Invalid value for '--connection-type': 'NOT_VALID_TYPE'" in result.output


@mock.patch("gantry.cli.data_connector.APIClient.request")
def test_create_data_connector_api_failure(mock_api_client: mock.Mock):
    """
    Tests that invalid connection type throws an error
    """
    mock_api_client.return_value = {"response": "error", "error": "some error"}

    runner = CliRunner()
    cli_args = [
        "--name",
        DATA_CONNECTOR_NAME,
        "--database-name",
        DATABASE_NAME,
        "--connection-type",
        CONNECTION_TYPE,
        "--secret-name",
        SECRET_NAME,
        "--description",
        DESCRIPTION,
        "--options",
        OPTIONS,
    ]

    result = runner.invoke(
        create,
        cli_args,
        env={"GANTRY_API_KEY": "test", "GANTRY_LOGS_LOCATION": UNITTEST_HOST},
    )

    assert result.exit_code == 1


def test_list_data_connectors():
    """
    Tests that correct message displays when list command returns data connectors
    """
    runner = CliRunner()

    with responses.RequestsMock() as resp:
        resp.add(
            resp.GET,
            f"{UNITTEST_HOST}/api/v1/data-connectors",
            json={
                "response": "ok",
                "data": [
                    {
                        "connection_type": CONNECTION_TYPE,
                        "created_at": "2023-01-18T00:18:01.000000",
                        "database_name": DATABASE_NAME,
                        "description": DESCRIPTION,
                        "id": DATA_CONNECTOR_1_ID,
                        "name": DATABASE_NAME,
                        "options": {"schema_name": "PUBLIC", "table_name": "GANTRY_EVENTS"},
                        "secret_name": SECRET_NAME,
                        "type": "SOURCE",
                        "updated_at": "2023-01-18T00:18:01.000000",
                    },
                    {
                        "connection_type": CONNECTION_TYPE,
                        "created_at": "2023-01-18T00:18:01.000000",
                        "database_name": DATABASE_NAME,
                        "description": DESCRIPTION,
                        "id": DATA_CONNECTOR_2_ID,
                        "name": DATABASE_NAME,
                        "options": {"schema_name": "PUBLIC", "table_name": "GANTRY_EVENTS_2"},
                        "secret_name": SECRET_NAME,
                        "type": "SOURCE",
                        "updated_at": "2023-01-18T00:18:01.000000",
                    },
                ],
            },
            headers={"Content-Type": "application/json"},
        )

        result = runner.invoke(
            list,
            env={"GANTRY_API_KEY": "test", "GANTRY_LOGS_LOCATION": UNITTEST_HOST},
        )

        assert result.exit_code == 0
        assert "--> A list of registered data connectors" in result.output
        assert DATA_CONNECTOR_1_ID in result.output
        assert DATA_CONNECTOR_2_ID in result.output


def test_delete_data_connector():
    """ """
    runner = CliRunner()
    cli_args = ["--name", DATA_CONNECTOR_NAME]

    with responses.RequestsMock() as resp:
        resp.add(
            resp.DELETE,
            f"{UNITTEST_HOST}/api/v1/data-connectors/sources/{DATA_CONNECTOR_NAME}",
            json={
                "response": "ok",
                "data": {
                    "connection_type": CONNECTION_TYPE,
                    "created_at": "2023-01-18T00:18:01.000000",
                    "database_name": DATABASE_NAME,
                    "description": DESCRIPTION,
                    "id": DATA_CONNECTOR_1_ID,
                    "name": DATABASE_NAME,
                    "options": {"schema_name": "PUBLIC", "table_name": "GANTRY_EVENTS"},
                    "secret_name": SECRET_NAME,
                    "type": "SOURCE",
                    "updated_at": "2023-01-18T00:18:01.000000",
                },
            },
            headers={"Content-Type": "application/json"},
        )

        result = runner.invoke(
            delete,
            cli_args,
            env={"GANTRY_API_KEY": "test", "GANTRY_LOGS_LOCATION": UNITTEST_HOST},
        )

        assert result.exit_code == 0
        assert "--> Deleted the source data connector" in result.output
        assert DATA_CONNECTOR_1_ID in result.output


def test_list_pipelines_given_appname_status():
    """
    Tests that correct message displays when list command returns pipelines
    """
    runner = CliRunner()
    cli_args = ["--app-name", APP_NAME, "--status", DATA_CONNECTOR_ENABLED_STATUS_CMD]
    url = (
        f"{UNITTEST_HOST}/api/v1/data-connectors/pipelines?app_name={APP_NAME}"
        f"&enabled_status={DATA_CONNECTOR_ENABLED_STATUS}"
    )
    with responses.RequestsMock() as resp:
        resp.add(
            resp.GET,
            url,
            json={
                "response": "ok",
                "data": {
                    "consumer_id": PIPELINE_CONSUMER_ID,
                    "consumer_type": "GANTRY_EVENTLOGGER",
                    "created_at": "2023-02-11 01:04:57.293993",
                    "disabled_at": None,
                    "id": PIPELINE_ID,
                    "metadata_id": METADATA_ID,
                    "name": "2218762f-a684-480c-b418-d5adcdcb5dc6'",
                    "options": {
                        "sink_options": {
                            "join_key": "C",
                            "model_name": "c532db16-445f-419c-bab1-6082aa691bed",
                            "organization_id": "75c22adf-0494-4a6c-94f6-2e66aa3cd390",
                            "sink_path": "a:/b",
                            "version": "1.0.0",
                        },
                        "source_options": {
                            "feedbacks": [],
                            "global_tags": {"environment": "dev"},
                            "inputs": ["A"],
                            "join_key": "C",
                            "outputs": ["B"],
                            "row_level_tags": ["E"],
                            "timestamp": "D",
                        },
                    },
                    "type": "glueetl",
                    "updated_at": "2023-02-11 01:04:57.293993",
                },
            },
        )

        result = runner.invoke(
            list_pipelines,
            cli_args,
            env={
                "GANTRY_API_KEY": "test",
                "GANTRY_LOGS_LOCATION": UNITTEST_HOST,
                "GANTRY_DATASET_WORKING_DIR": "/tmp",
            },
        )
        assert result.exit_code == 0
        response = (
            f"--> The following pipelines are given for {APP_NAME} "
            f"and {DATA_CONNECTOR_ENABLED_STATUS_CMD}"
        )
        assert response in result.output

        assert (PIPELINE_ID) in result.output
        assert (PIPELINE_CONSUMER_ID) in result.output


def test_list_pipeline_ops_given_appname_status():
    """
    Tests that correct message displays when list command returns pipeline operations
    """
    runner = CliRunner()
    cli_args = [
        "--pipeline-name",
        PIPELINE_NAME,
        "--app-name",
        APP_NAME,
        "--status",
        PIPELINE_OPERATION_STATUS,
    ]

    url = (
        f"{UNITTEST_HOST}/api/v1/data-connectors/pipeline-operations?app_name={APP_NAME}"
        f"&pipeline_name={PIPELINE_NAME}&status={PIPELINE_OPERATION_STATUS}"
    )
    with responses.RequestsMock() as resp:
        resp.add(
            resp.GET,
            url,
            json={
                "response": "ok",
                "data": {
                    "consumer_operation_id": "5c327f88-a9a8-11ed-b6e2-6e131c5595a6",
                    "created_at": "Sat, 11 Feb 2023 01:06:48 GMT",
                    "id": PIPELINE_OPERATION_ID,
                    "metadata_id": METADATA_ID,
                    "options": None,
                    "pipeline_id": PIPELINE_ID,
                    "status": "QUEUED",
                    "trigger_id": None,
                    "trigger_type": "DIRECT",
                    "updated_at": "Sat, 11 Feb 2023 01:06:48 GMT",
                },
            },
        )

        result = runner.invoke(
            list_pipeline_operations,
            cli_args,
            env={
                "GANTRY_API_KEY": "test",
                "GANTRY_LOGS_LOCATION": UNITTEST_HOST,
                "GANTRY_DATASET_WORKING_DIR": "/tmp",
            },
        )
        assert result.exit_code == 0
        response = (
            f"--> The following pipeline operations are given for APP={APP_NAME} "
            f"and PIPELINE={PIPELINE_NAME} and STATUS={PIPELINE_OPERATION_STATUS}"
        )
        assert response in result.output
        assert METADATA_ID in result.output
        assert PIPELINE_OPERATION_ID in result.output
        assert PIPELINE_ID in result.output


def test_delete_pipeline():
    """Deletes a data connector pipeline given app_name and pipeline_name"""
    runner = CliRunner()
    cli_args = [
        "--pipeline-name",
        PIPELINE_NAME,
        "--app-name",
        APP_NAME,
        "--app-version",
        APP_VERSION,
    ]

    url = (
        f"{UNITTEST_HOST}/api/v1/data-connectors/pipelines?pipeline_name={PIPELINE_NAME}"
        f"&app_name={APP_NAME}&app_version={APP_VERSION}"
    )
    with responses.RequestsMock() as resp:
        resp.add(
            resp.DELETE,
            url,
            json={
                "response": "ok",
                "data": {
                    "id": PIPELINE_ID,
                    "created_at": "2023-02-16 01:01:01.999999",
                    "disabled_at": None,
                    "updated_at": "2023-02-16 01:01:01.999999",
                    "name": PIPELINE_NAME,
                    "options": {
                        "feedbacks": [],
                        "inputs": ["A"],
                        "outputs": ["B"],
                    },
                },
            },
            headers={"Content-Type": "application/json"},
        )

        result = runner.invoke(
            delete_pipeline,
            cli_args,
            env={"GANTRY_API_KEY": "test", "GANTRY_LOGS_LOCATION": UNITTEST_HOST},
        )

        assert result.exit_code == 0
        assert "--> Deleted the pipeline" in result.output
        assert PIPELINE_ID in result.output
        assert PIPELINE_NAME in result.output
