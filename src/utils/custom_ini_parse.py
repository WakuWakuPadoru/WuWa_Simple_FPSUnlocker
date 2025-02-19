class EngineIniParser:
    def __init__(self, filename):
        self.filename = filename
        self.config = {}
        self.paths = []  # List of paths

    def read_and_ignore_paths(self):  # Read and parse the INI file
        current_section = None
        with open(self.filename, "r") as file:
            for line in file:
                line = line.strip()  # Remove leading/trailing whitespace
                if not line or line.startswith(";") or line.startswith("#"):  # Skip empty lines and comments
                    continue
                if line.startswith("[") and line.endswith("]"):  # Section header
                    current_section = line[1:-1]  # Remove brackets
                    self.config[current_section] = {}  # Create empty dictionary for sections
                else:
                    key, value = line.split("=")  # Split key and value by "="
                    if current_section != "Core.System":  # If section is not Core.System, add key-value pair to current section
                        self.config[current_section][
                            key.strip()] = value.strip()  # Add key-value pair to current section
                    elif current_section == "Core.System":  # If section is Core.System, add paths to list
                        self.paths.append(value.strip())
        self.config.__delitem__("Core.System")  # Remove Core.System section
        return self.config

    def add_section(self, section):  # Add section to config
        if section not in self.config:
            self.config[section] = {}  # Add section to config
        else:
            return

    def add_key_value(self, section, key, value):
        if section in self.config:
            self.config[section][key] = value
        else:
            return

    def compile(self):  # Write config to INI file
        with open(self.filename, "w") as file:
            file.write("[Core.System]\n")
            for path in self.paths:
                file.write(f"paths={path}\n")
            for section, values in self.config.items():
                if values is not None and values != "" and values != {}:  # If section is not empty, write key-value pairs
                    file.write(f"\n[{section}]\n")  # Write section header
                    for key, value in values.items():  # Write key-value pairs
                        file.write(f"{key}={value}\n")  # Write key-value pairs
                else:
                    continue
        return self.config
