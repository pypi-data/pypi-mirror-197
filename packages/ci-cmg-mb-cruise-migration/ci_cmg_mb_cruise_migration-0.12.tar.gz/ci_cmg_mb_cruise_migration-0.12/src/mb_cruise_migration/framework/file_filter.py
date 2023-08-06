from src.mb_cruise_migration.logging.migration_log import MigrationLog
from src.mb_cruise_migration.models.mb.mb_ngdcid_and_file import MbFile
from src.mb_cruise_migration.migration_properties import MigrationProperties
from src.mb_cruise_migration.utility.common import strip_none


class FileFilter(object):
    @classmethod
    def filter(cls, files: [MbFile]):
        files = [file for file in files if not cls.__is_invalid_file(file)]
        files = [file for file in files if cls.__is_being_migrated(file)]

        return strip_none(files)

    @classmethod
    def __is_invalid_file(cls, file: MbFile):
        parsed_file = file.parsed_file
        if parsed_file.is_empty():
            MigrationLog.log_skipped_file(file)
            return True
        if parsed_file.is_wcd():
            MigrationLog.log_skipped_file(file)
            return True
        if parsed_file.is_xtf():
            MigrationLog.log_skipped_file(file)
            return True
        if parsed_file.is_singlebeam():
            MigrationLog.log_skipped_file(file)
            return True
        if parsed_file.is_canadian_data():
            MigrationLog.log_skipped_file(file)
            return True

        return False

    @classmethod
    def __is_being_migrated(cls, file: MbFile):
        parsed_file = file.parsed_file
        if parsed_file.is_survey_metadata():
            return MigrationProperties.migrate.survey_metadata
        if parsed_file.has_extraneous():
            return MigrationProperties.migrate.extraneous
        if parsed_file.has_leg():
            return MigrationProperties.migrate.legs
        if parsed_file.has_zone():
            return MigrationProperties.migrate.zones
        if parsed_file.has_region():
            return MigrationProperties.migrate.regions
        if parsed_file.is_standard():
            return MigrationProperties.migrate.standard

        raise ValueError("no valid file category identified")
