import skutterbug


class EndpointNotFound(Exception):
    """Webmention endpoint could not be found."""


def send(source: skutterbug.url, target: skutterbug.url) -> dict:
    """
    Send a webmention to each of `targets` on behalf of `source`.

    """
    # TODO ask archive.org to cache; archive=False
    # TODO re-queue failures w/ a logarithmic backoff
    source = skutterbug.url(source)
    target = skutterbug.url(target)
    cache = skutterbug.cache()
    endpoint = cache[target].discover_link("webmention")
    if not endpoint:
        raise EndpointNotFound(target)
    return cache[endpoint].post(data={"source": source, "target": target}).json
    # TODO check if received and/or displayed
    # TODO !!! endpoint.post(payload)
    # TODO web.tx.db.update("mentions", what="data = ?", where="mention_id = ?",
    # TODO              vals=[mention, mention_id])
