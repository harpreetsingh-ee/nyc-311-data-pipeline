"""
Airflow Plugin: Setup Connections on Startup

This plugin automatically creates GCS and Snowflake connections
when Airflow starts up.

Airflow will automatically load plugins from the plugins/ directory.
"""

import logging
from airflow.plugins_manager import AirflowPlugin

logger = logging.getLogger(__name__)

# Setup connections on plugin load
try:
    from config.connections import setup_connections
    logger.info("Setting up Airflow connections...")
    setup_connections()
    logger.info("✓ Connections setup completed on plugin load")
except Exception as e:
    logger.error(f"✗ Failed to setup connections: {e}", exc_info=True)


class SetupConnectionsPlugin(AirflowPlugin):
    """Plugin to setup connections on Airflow startup."""

    name = "setup_connections_plugin"
