import re

P_VERSION_HAS_SPECIFIERS = re.compile('^[a-zA-Z0-9_.-]+\s*(?=(?:===|~=|==|!=|<=|>=|<|>))')
P_HAS_VERSION_SPECIFIERS = re.compile('(?:===|~=|==|!=|<=|>=|<|>)')
P_NORMALIZE = re.compile('^[a-zA-Z0-9_.-]+\s*(?=(?:===|~=|==|!=|<=|>=|<|>)?\s*;?)')
URL_VERSION_SPECIFIERS = 'https://peps.python.org/pep-0440/#version-specifiers'

P_KV_SEP = re.compile('\s*=\s*')


def ver_has_spec(name: str):
    return P_VERSION_HAS_SPECIFIERS.search(name) is not None


def has_ver_spec(name: str):
    return P_HAS_VERSION_SPECIFIERS.search(name) is not None


def get_package_name(name: str):
    return P_NORMALIZE.search(norm_name(name)).group()


def norm_name(name: str):
    return name.lower().replace('_', '-') if name else None


def norm_module(name: str):
    return name.lower().replace('-', '_') if name else None
