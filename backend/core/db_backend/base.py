"""
Custom MySQL/MariaDB backend that allows older versions and disables RETURNING clause
"""
from django.db.backends.mysql.base import DatabaseWrapper as MySQLDatabaseWrapper
from django.db.backends.mysql.features import DatabaseFeatures as MySQLDatabaseFeatures


class DatabaseFeatures(MySQLDatabaseFeatures):
    """
    Custom features class to disable RETURNING for MariaDB 10.4
    """
    # Force disable RETURNING support
    can_return_columns_from_insert = False
    can_return_rows_from_bulk_insert = False


class DatabaseWrapper(MySQLDatabaseWrapper):
    """
    Custom database wrapper to support MariaDB 10.4 and disable RETURNING clause
    """
    features_class = DatabaseFeatures
    
    def check_database_version_supported(self):
        """
        Override to skip version check for MariaDB 10.4
        """
        # Skip the version check - we know 10.4 works for our use case
        pass

