"""
Custom MySQL/MariaDB backend that allows older versions and disables RETURNING clause
"""
from django.db.backends.mysql.base import DatabaseWrapper as MySQLDatabaseWrapper


class DatabaseWrapper(MySQLDatabaseWrapper):
    """
    Custom database wrapper to support MariaDB 10.4 and disable RETURNING clause
    """
    
    def check_database_version_supported(self):
        """
        Override to skip version check for MariaDB 10.4
        """
        # Skip the version check - we know 10.4 works for our use case
        pass
    
    @property
    def mysql_server_data(self):
        """
        Get server data and disable RETURNING support for MariaDB 10.4
        """
        data = super().mysql_server_data
        # Force disable RETURNING for MariaDB 10.4
        data['supports_returning'] = False
        return data
