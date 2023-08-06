"""
Default api
"""

from shadybackend.api_tools import define_hook, defnine_API


@defnine_API(baseline={"test_arg": 1, "required_": 1})
def test_api(G, ARG):
    """
    a test api.
    """
    print(f"Fish {ARG['test_arg']}")
