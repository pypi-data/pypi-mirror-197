"""
Shared functionalities for retrieving URLs' data when headers are needed
"""
import http.client
import ssl
import urllib.request

USER_AGENT = "\
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \
AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/107.0.0.0 Safari/537.36"

UA_HEADER = {"User-Agent": USER_AGENT}

_DEFAULT_CONTEXT = ssl.create_default_context()
_DEFAULT_CONTEXT.set_ciphers("DEFAULT")


def get_url_response(
    url: str,
    default_headers: bool = True,
    set_context: bool = False,
) -> http.client.HTTPResponse:
    """
    Return the response from a URL with custom headers and SSL context when opening if
    set_context is True.
    """
    if default_headers:
        headers = UA_HEADER
    else:
        headers = {}
    if set_context:
        context = _DEFAULT_CONTEXT
    else:
        context = None
    request = urllib.request.Request(url, headers=headers)
    return urllib.request.urlopen(request, context=context)  # type: ignore[no-any-return]
