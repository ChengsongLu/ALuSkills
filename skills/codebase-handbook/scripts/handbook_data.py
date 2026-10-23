"""Shared safe YAML loading and handbook path boundaries."""
from dataclasses import MISSING, fields
from pathlib import Path

try:
    import yaml
except ImportError as error:
    raise SystemExit(
        "PyYAML is required; install with python3 -m pip install -r "
        "<skill-dir>/scripts/requirements.txt"
    ) from error


class UniqueSafeLoader(yaml.SafeLoader):
    """Reject duplicate keys instead of silently discarding earlier values."""


def unique_mapping(loader, node):
    loader.flatten_mapping(node)
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if not isinstance(key, str) or key in result:
            raise ValueError(f"YAML keys must be unique strings: {key!r}")
        result[key] = loader.construct_object(value_node)
    return result


UniqueSafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)


def load_yaml(text):
    try:
        data = yaml.load(text, Loader=UniqueSafeLoader)
    except yaml.YAMLError as error:
        raise ValueError(f"invalid YAML: {error}") from error
    if not isinstance(data, dict):
        raise ValueError("YAML document must be a mapping")
    return data


def records(data, key):
    value = data.get(key, [])
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise ValueError(f"{key} must be a list of mappings")
    return value


def typed_fields(item, model, aliases=None, excluded=()):
    source_keys = {target: source for source, target in (aliases or {}).items()}
    result = {}
    for field in fields(model):
        if field.name in excluded:
            continue
        source_key = source_keys.get(field.name, field.name)
        if source_key not in item:
            if field.default is MISSING and field.default_factory is MISSING:
                raise ValueError(f"missing required field: {field.name}")
            continue
        value = item[source_key]
        kind = str(field.type)
        if kind == "list[str]":
            valid = isinstance(value, list) and all(isinstance(v, str) for v in value)
        elif kind == "int":
            valid = isinstance(value, int) and not isinstance(value, bool)
        else:
            valid = isinstance(value, str)
        if not valid:
            raise ValueError(f"invalid type for {field.name}: expected {kind}")
        result[field.name] = value
    return result


def confined_path(base: Path, relative: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"path must stay inside {base.name}: {relative}")
    resolved = (base / path).resolve()
    if not resolved.is_relative_to(base.resolve()):
        raise ValueError(f"path escapes {base.name}: {relative}")
    return resolved


def handbook_directory(root: Path) -> Path:
    handbook = root / ".codebase-handbook"
    if handbook.is_symlink():
        raise ValueError(".codebase-handbook must not be a symbolic link")
    return handbook
