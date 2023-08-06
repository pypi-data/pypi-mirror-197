import oracledb

from src.mb_cruise_migration.migration_properties import MigrationProperties

class BatchError(object):
    def __init__(self, error, offset):
        self.error = error
        self.offset = offset


class CruiseConnection(object):
    def __init__(self):
        self.config = MigrationProperties.cruise_db_config
        self.dsn_string = oracledb.makedsn(self.config.server, self.config.port, sid=self.config.sid, service_name=self.config.service)

    def __get_connection(self):
        try:
            return oracledb.connect(
                user=self.config.user,
                password=self.config.password,
                dsn=self.dsn_string,
                threaded=True
            )
        except Exception as e:
            print("WARNING DB failed to connect. Script closing", e)
            raise e

    def executemany(self, command, data=None):
        with self.__get_connection() as connection:
            try:
                cursor = connection.cursor()
                cursor.executemany(command, data, batcherrors=True)
                errors: [BatchError] = []
                for error in cursor.getbatcherrors():
                    errors.append(BatchError(error.message, error.offset))
                connection.commit()
                return errors
            except:
                connection.rollback()
            raise
