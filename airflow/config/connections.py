"""
Airflow Connections Setup

Programmatically create and configure connections for GCS and Snowflake.
This runs on Airflow startup to ensure connections are properly configured.

Uses constants from include.constants for connection IDs.
Credentials are read from environment variables for security.
"""

import os
import logging
from airflow.models import Connection
from airflow.utils.db import merge_conn
from typing import Optional
from include.constants import (
    GCS_CONN_ID,
    GCP_PROJECT_ID,
    SNOWFLAKE_CONN_ID,
    SNOWFLAKE_ACCOUNT,
    SNOWFLAKE_USER,
    SNOWFLAKE_DATABASE,
    SNOWFLAKE_SCHEMA,
    SNOWFLAKE_WAREHOUSE,
    SNOWFLAKE_ROLE,
)

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manage Airflow connections programmatically."""

    @staticmethod
    def create_gcs_connection(
        conn_id: Optional[str] = None,
        project_id: Optional[str] = None,
        private_key_content: Optional[str] = None,
    ) -> Connection:
        """
        Create a Google Cloud Storage (GCS) connection using service account key.

        Args:
            conn_id: Connection ID (uses GCS_CONN_ID from constants if not provided)
            project_id: GCP project ID (uses GCP_PROJECT_ID from constants if not provided)
            private_key_content: Service account key in JSON format (SENSITIVE - from env only)

        Returns:
            Connection object

        Configuration: include/constants.py
        Sensitive: GCS_PRIVATE_KEY_CONTENT (from environment variable only)

        Note:
            Service account key should be provided as JSON string in environment variable.
            Example: GCS_PRIVATE_KEY_CONTENT='{"type": "service_account", "project_id": "...", ...}'
        """
        conn_id = conn_id or GCS_CONN_ID
        project_id = project_id or GCP_PROJECT_ID
        private_key_content = private_key_content or os.getenv("GCS_PRIVATE_KEY_CONTENT")

        if not private_key_content:
            logger.warning(
                f"GCS connection '{conn_id}' not created: "
                "private_key_content not provided"
            )
            return None

        # Build extra JSON with service account key
        extra = {
            "extra__google_cloud_platform__project_id": project_id,
            "extra__google_cloud_platform__keyfile_dict": private_key_content,
        }

        conn = Connection(
            conn_id=conn_id,
            conn_type="google_cloud_platform",
            host="",
            login="",
            port=None,
            schema="",
            extra=extra,
            description="Google Cloud Storage connection (service account key)",
        )

        logger.info(f"Created GCS connection: {conn_id}")
        return conn

    @staticmethod
    def create_snowflake_connection(
        conn_id: Optional[str] = None,
        account: Optional[str] = None,
        user: Optional[str] = None,
        private_key_content: Optional[str] = None,
        database: Optional[str] = None,
        schema: Optional[str] = None,
        warehouse: Optional[str] = None,
        role: Optional[str] = None,
    ) -> Connection:
        """
        Create a Snowflake connection using private key authentication.

        Args:
            conn_id: Connection ID (uses SNOWFLAKE_CONN_ID from constants if not provided)
            account: Snowflake account (uses SNOWFLAKE_ACCOUNT from constants if not provided)
            user: Snowflake username (uses SNOWFLAKE_USER from constants if not provided)
            private_key_content: Private key content in PEM format (SENSITIVE - from env only)
            database: Database (uses SNOWFLAKE_DATABASE from constants if not provided)
            schema: Schema (uses SNOWFLAKE_SCHEMA from constants if not provided)
            warehouse: Warehouse (uses SNOWFLAKE_WAREHOUSE from constants if not provided)
            role: Role (uses SNOWFLAKE_ROLE from constants if not provided)

        Returns:
            Connection object

        Configuration: include/constants.py
        Sensitive: SNOWFLAKE_PRIVATE_KEY_CONTENT (from environment variable only)
        """
        # Get from environment if not provided
        conn_id = conn_id or SNOWFLAKE_CONN_ID
        account = account or os.getenv("SNOWFLAKE_ACCOUNT")
        user = user or os.getenv("SNOWFLAKE_USER")
        private_key_content = private_key_content or os.getenv("SNOWFLAKE_PRIVATE_KEY_CONTENT")
        database = database or SNOWFLAKE_DATABASE
        schema = schema or SNOWFLAKE_SCHEMA
        warehouse = warehouse or SNOWFLAKE_WAREHOUSE
        role = role or SNOWFLAKE_ROLE

        if not all([account, user, private_key_content]):
            logger.warning(
                f"Snowflake connection '{conn_id}' not created: "
                "Missing account, user, or private_key_content"
            )
            return None

        # Build extra JSON with private key authentication
        extra = {
            "account": account,
            "warehouse": warehouse,
            "database": database,
            "schema": schema,
            "private_key_content": private_key_content,
        }

        if role:
            extra["role"] = role

        conn = Connection(
            conn_id=conn_id,
            conn_type="snowflake",
            host=account,
            login=user,
            port=443,
            schema=schema,
            extra=extra,
            description="Snowflake connection (private key auth)",
        )

        logger.info(f"Created Snowflake connection: {conn_id}")
        return conn

    @staticmethod
    def upsert_connection(conn: Connection) -> None:
        """
        Create or update a connection.

        Args:
            conn: Connection object
        """
        if not conn:
            return

        try:
            merge_conn(conn)
            logger.info(f"✓ Connection '{conn.conn_id}' configured")
        except Exception as e:
            logger.error(f"Failed to create connection '{conn.conn_id}': {e}")


def setup_connections() -> None:
    """
    Setup all required connections.
    Call this from an Airflow hook or startup script.

    Uses connection IDs from include.constants and credentials from environment variables.
    """
    logger.info("Setting up Airflow connections...")

    # GCS Connection
    gcs_conn = ConnectionManager.create_gcs_connection(
        conn_id=GCS_CONN_ID,
        project_id=GCP_PROJECT_ID,
        private_key_content=os.getenv("GCS_PRIVATE_KEY_CONTENT"),  # Sensitive: from env only
    )
    ConnectionManager.upsert_connection(gcs_conn)

    # Snowflake Connection
    sf_conn = ConnectionManager.create_snowflake_connection(
        conn_id=SNOWFLAKE_CONN_ID,
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        private_key_content=os.getenv("SNOWFLAKE_PRIVATE_KEY_CONTENT"),  # Sensitive: from env only
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
        warehouse=SNOWFLAKE_WAREHOUSE,
        role=SNOWFLAKE_ROLE,
    )
    ConnectionManager.upsert_connection(sf_conn)

    logger.info("✓ All connections configured")


# Optional: Auto-setup on import
# Uncomment to automatically create connections when this module is imported
# This can be done in airflow/config/__init__.py
# try:
#     setup_connections()
# except Exception as e:
#     logger.warning(f"Connection setup failed: {e}")
