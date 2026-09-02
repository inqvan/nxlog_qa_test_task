from pathlib import Path


def write_environment_file(directory: Path, properties: dict[str, str]) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    file_path = directory / "environment.properties"

    existing_properties: dict[str, str] = {}
    if file_path.exists():
        for line in file_path.read_text().splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                existing_properties[key] = value

    merged_properties = {**existing_properties, **properties}
    file_path.write_text("".join(f"{key}={value}\n" for key, value in merged_properties.items()))
    return file_path
