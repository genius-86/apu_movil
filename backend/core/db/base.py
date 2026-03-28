from django.db.backends.mysql.base import DatabaseWrapper as MysqlWrapper

class DatabaseWrapper(MysqlWrapper):
    def check_database_version_supported(self):
        """
        Bypass MariaDB version check. 
        Django 5+ requires MariaDB 10.5+, but XAMPP provides 10.4.
        """
        pass
