from mimeo.exceptions import (IncorrectMimeoConfig, IncorrectMimeoModel,
                              IncorrectMimeoTemplate,
                              UnsupportedOutputDirection,
                              UnsupportedOutputFormat, InvalidIndent)


class MimeoConfig:

    OUTPUT_FORMAT_KEY = "output_format"
    OUTPUT_DETAILS_KEY = "output_details"
    OUTPUT_DETAILS_DIRECTION_KEY = "direction"
    OUTPUT_DETAILS_DIRECTORY_PATH_KEY = "directory_path"
    OUTPUT_DETAILS_FILE_NAME_KEY = "file_name"
    XML_DECLARATION_KEY = "xml_declaration"
    INDENT_KEY = "indent"
    TEMPLATES_KEY = "_templates_"
    TEMPLATES_COUNT_KEY = "count"
    TEMPLATES_MODEL_KEY = "model"
    TEMPLATES_MODEL_ATTRIBUTES_KEY = "attributes"

    SUPPORTED_OUTPUT_FORMATS = ("xml",)

    def __init__(self, config: dict):
        self.output_format = MimeoConfig.__get_output_format(config)
        self.output_details = MimeoOutputDetails(self.output_format, config.get(self.OUTPUT_DETAILS_KEY, {}))
        self.xml_declaration = config.get(self.XML_DECLARATION_KEY, False)
        self.indent = MimeoConfig.__get_indent(config)
        self.templates = MimeoConfig.__get_templates(config)

    @staticmethod
    def __get_output_format(config):
        output_format = config.get(MimeoConfig.OUTPUT_FORMAT_KEY, "xml")
        if output_format in MimeoConfig.SUPPORTED_OUTPUT_FORMATS:
            return output_format
        else:
            raise UnsupportedOutputFormat(f"Provided format [{output_format}] is not supported!")

    @staticmethod
    def __get_indent(config):
        indent = config.get(MimeoConfig.INDENT_KEY, 0)
        if indent >= 0:
            return indent
        else:
            raise InvalidIndent(f"Provided indent [{indent}] is negative!")

    @staticmethod
    def __get_templates(config):
        templates = config.get(MimeoConfig.TEMPLATES_KEY)
        if templates is None:
            raise IncorrectMimeoConfig(f"No templates in the Mimeo Config: {config}")
        elif not isinstance(templates, list):
            raise IncorrectMimeoConfig(f"_templates_ property does not store an array: {config}")
        else:
            return (MimeoTemplate(template) for template in config.get(MimeoConfig.TEMPLATES_KEY))


class MimeoOutputDetails:

    FILE_DIRECTION = "file"
    STD_OUT_DIRECTION = "stdout"

    SUPPORTED_OUTPUT_DIRECTIONS = (STD_OUT_DIRECTION, FILE_DIRECTION)

    def __init__(self, output_format: str, output_details: dict):
        self.direction = MimeoOutputDetails.__get_direction(output_details)
        self.directory_path = MimeoOutputDetails.__get_directory_path(self.direction, output_details)
        self.file_name_tmplt = MimeoOutputDetails.__get_file_name_tmplt(self.direction, output_details, output_format)

    @staticmethod
    def __get_direction(output_details):
        direction = output_details.get(MimeoConfig.OUTPUT_DETAILS_DIRECTION_KEY, MimeoOutputDetails.FILE_DIRECTION)
        if direction in MimeoOutputDetails.SUPPORTED_OUTPUT_DIRECTIONS:
            return direction
        else:
            raise UnsupportedOutputDirection(f"Provided direction [{direction}] is not supported!")

    @staticmethod
    def __get_directory_path(direction: str, output_details: dict):
        if direction == MimeoOutputDetails.FILE_DIRECTION:
            return output_details.get(MimeoConfig.OUTPUT_DETAILS_DIRECTORY_PATH_KEY, "mimeo-output")

    @staticmethod
    def __get_file_name_tmplt(direction: str, output_details: dict, output_format: str):
        if direction == MimeoOutputDetails.FILE_DIRECTION:
            file_name = output_details.get(MimeoConfig.OUTPUT_DETAILS_FILE_NAME_KEY, "mimeo-output")
            return f"{file_name}-{'{}'}.{output_format}"


class MimeoTemplate:

    def __init__(self, template: dict):
        MimeoTemplate.__validate_template(template)
        self.count = template.get(MimeoConfig.TEMPLATES_COUNT_KEY)
        self.model = MimeoModel(template.get(MimeoConfig.TEMPLATES_MODEL_KEY))

    @staticmethod
    def __validate_template(template: dict):
        if MimeoConfig.TEMPLATES_COUNT_KEY not in template:
            raise IncorrectMimeoTemplate(f"No count value in the Mimeo Template: {template}")
        if MimeoConfig.TEMPLATES_MODEL_KEY not in template:
            raise IncorrectMimeoTemplate(f"No model data in the Mimeo Template: {template}")


class MimeoModel:

    def __init__(self, model: dict):
        self.attributes = model.get(MimeoConfig.TEMPLATES_MODEL_ATTRIBUTES_KEY, {})
        self.root_name = MimeoModel.__get_root_name(model)
        self.root_data = model.get(self.root_name)

    @staticmethod
    def __get_root_name(model):
        model_keys = [key for key in filter(MimeoModel.__is_not_attributes_key, iter(model))]
        if len(model_keys) == 1:
            return model_keys[0]
        if len(model_keys) == 0:
            raise IncorrectMimeoModel(f"No root data in Mimeo Model: {model}")
        elif len(model_keys) > 1:
            raise IncorrectMimeoModel(f"Multiple root data in Mimeo Model: {model}")

    @staticmethod
    def __is_not_attributes_key(dict_key):
        return dict_key != MimeoConfig.TEMPLATES_MODEL_ATTRIBUTES_KEY
