from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


def normalize_url(database_uri: str) -> str:
    parsed_uri = urlparse(database_uri)
    query_params = parse_qs(parsed_uri.query)
    if 'reinitialize' in query_params:
        del query_params['reinitialize']

    normalized_uri = parsed_uri._replace(query=urlencode(query_params, doseq=True))
    return urlunparse(normalized_uri)