class QueryBuilder(object):
    def __init__(self, schema):
        self.schema = schema + "."

    def select_table_size(self, table: str):
        return f"SELECT COUNT(*) FROM {self.schema}{table}"

    def select_all(self, table: str):
        return f"SELECT * FROM {self.schema}{table}"

    def select_all_where_fields_match(self, table: str, search_fields: dict):
        field_names = list(dict.keys(search_fields))
        search_values = list(dict.values(search_fields))

        query = f"SELECT * FROM {self.schema}{table} WHERE " + self.build_field_query_string(field_names)

        return query, search_values

    def select_some(self, table: str, wanted_fields: list):
        wanted_fields = ", ".join(wanted_fields)

        return f"SELECT {wanted_fields} FROM {self.schema}{table}"

    def select_some_constrained_by_field_values(self, table: str, wanted_fields: list, search_fields):
        field_names = list(dict.keys(search_fields))
        search_values = list(dict.values(search_fields))

        wanted_fields = ", ".join(wanted_fields)
        query = f"SELECT {wanted_fields} FROM {self.schema}{table} WHERE " + self.build_field_query_string(field_names)

        return query, search_values

    def select_survey_shape(self, table, ngdc_id):
        query = f"SELECT SDO_UTIL.TO_WKBGEOMETRY(SHAPE) as SHAPE FROM {self.schema}{table} WHERE NGDC_ID=:NGDC_ID"
        search_values = {'NGDC_ID': ngdc_id}

        return query, search_values

    def select_file_shape(self, table, data_file):
        query = f"SELECT SDO_UTIL.TO_WKBGEOMETRY(SHAPE) as SHAPE FROM {self.schema}{table} WHERE DATA_FILE=:DATA_FILE"
        search_values = {'DATA_FILE': data_file}
        return query, search_values

    @staticmethod
    def select_subset(view: str, skip: int, limit: int):
        return f"SELECT * FROM ({view}) ORDER BY NGDC_ID OFFSET {skip} ROWS FETCH NEXT {limit} ROWS ONLY"

    def insert(self, table: str, fields: dict):
        field_names = list(fields.keys())
        values = list(fields.values())

        bind_variables = self.build_bind_variables_string(field_names)
        field_names = self.build_fields_string(field_names)

        query = f"INSERT INTO {self.schema}{table} ({field_names}) VALUES ({bind_variables})"

        return query, values

    def insert_statement(self, table: str, fields: list):

        bind_variables = self.build_bind_variables_string(fields)
        field_names = self.build_fields_string(fields)

        return f"INSERT INTO {self.schema}{table} ({field_names}) VALUES ({bind_variables})"

    def delete_all_rows(self, table: str):
        return f"DELETE FROM {self.schema}{table}"

    @staticmethod
    def build_fields_string(keys: list):
        return ", ".join(keys)

    @staticmethod
    def build_bind_variables_string(keys):
        return ":" + ", :".join(keys)

    @staticmethod
    def build_field_query_string(field_names: list):
        fields = ""
        for i, arg in enumerate(field_names):
            fields += f"{arg}=:{arg}"  # :{arg} is the bind variable
            if i < len(field_names) - 1:
                fields += f" and "
        return fields

    # LACKING BIND VARIABLE USAGE OR OTHERWISE NEEDS TO BE DEPRECATED:

    def select_mbinfo_file_formats(self):
        return f"SELECT * FROM {self.schema}MBINFO_FORMATS"

    def select_survey_reference(self, ngdc_id):
        return f"SELECT DOWNLOAD_URL FROM {self.schema}SURVEY_REFERENCE WHERE NGDC_ID = {ngdc_id}"

    def select_survey_files(self, ngdc_id):
        return f"SELECT * FROM {self.schema}NGDCID_AND_FILE WHERE NGDC_ID = {ngdc_id}"

    def select_mbinfo_for_file(self, data_file):
        return f"SELECT * FROM {self.schema}MBINFO_FILE_TSQL WHERE DATA_FILE = {data_file}"

    # LEGACY BELOW #####################################################################################################
    @staticmethod
    def build_select(table, conditions):
        """Takes in 'table' and 'conditions' to build a select command for the given conditions (fields) within the given table.
            Called within select() function below in order to build the final query."""

        command = f"select * from {table} where "
        for i, c in enumerate(conditions):
            # command += f"{c}=:{c}" #:{} is a bind variable
            command += f"{c}=:{c}"
            if i < len(conditions) - 1:
                command += f" and "

        return command

    @staticmethod
    def build_select_file_level(table, conditions):
        """Same as build_select() function above but specifically for MB.NGDCID_AND_FILE"""
        # Conditions example: [NGDC_ID: 39339, DATA_FILE: %em111%]
        command = f"select * from {table} where {conditions[0]} =: {conditions[0]}"

        return command

    def select(self, table, constraints, data):
        """Builds select query using the given table, constraints (field names), and data (field values)."""

        q_command = self.build_select(table, constraints)
        q_data = self.extract_dictionary_subset(data, constraints)

        # Queries the MB Database here using the fetch_all() function and places results in q_result
        q_result = self.db.fetch_all(q_command, q_data)

        # returns results of query
        return q_result

    @staticmethod
    def select_file_level(self, table, constraints, data):
        """Same as select() function above but specifically for MB.NGDCID_AND_FILE"""
        q_command = self.build_select_file_level(table, constraints)

        # Reassign proper names to constraints before sending to subset_dict
        q_data = self.extract_dictionary_subset(data, constraints)
        q_result = self.db.fetch_all(q_command, q_data)

        return q_result

    # def get_url(self, ngdc_id):
    #     """This function retrieves the DOWNLOAD_URL from the MB.SURVEY_REFERENCE Table.
    #         DOWNLOAD_URL is currently the only data being migrated from MB.SURVEY_REFERENCE"""
    #     get_url = 'SELECT DOWNLOAD_URL FROM MB.SURVEY_REFERENCE WHERE NGDC_ID =:NGDC_ID'
    #
    #     data = {'NGDC_ID': ngdc_id}
    #
    #     url = self.db.fetch_one(get_url, data)
    #
    #     return url['DOWNLOAD_URL']

    @staticmethod
    def extract_dictionary_subset(dictionary: dict, subset_keys: list) -> dict:
        return {key: dictionary[key] for key in subset_keys if key in dictionary.keys()}
