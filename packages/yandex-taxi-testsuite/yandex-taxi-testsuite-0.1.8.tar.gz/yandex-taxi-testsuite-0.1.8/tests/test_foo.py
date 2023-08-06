import warnings


def test_foo():
    warnings.warn('sync warning')


async def test_afoo():
    warnings.warn('async warning')
