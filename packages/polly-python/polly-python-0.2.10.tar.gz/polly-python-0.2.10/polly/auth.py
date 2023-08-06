import requests
import json
from polly.__init__ import __version__ as current_version
from polly.session import PollySession
from requests.adapters import HTTPAdapter, Retry
from polly import helpers
from polly import constants as const
from polly.help import example, doc

link_doc = "https://docs.elucidata.io/OmixAtlas/Polly%20Python.html"
retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])


class UnauthorizedException(Exception):
    """

    :meta private:
    """

    def __str__(self):
        return f"Authorization failed as credentials not found. Please use Polly.auth(token) as shown here  ---- {link_doc}"


class Polly:
    """
    This class for authorization to use Polly on any local or cloud platform. To authenticate usage of Polly, \
the following function can be used.
    """

    default_session = None
    example = classmethod(example)
    doc = classmethod(doc)
    auth_flag = False  # Flag that represents session set or not

    @classmethod
    def auth(cls, token, env="", default_env="polly"):
        """
        Function for authorize usage of Polly on terminal or notebook.

        ``Args:``
            |  ``token (str):`` token copy from Polly front-end.


        ``Returns:``
            |  If token is not correct, it will give an error, else it will clear the authentication for user to\
 get started with polly-python.

        ``Error:``
            |  ``UnauthorizedException:`` when the token is expired.

        To use auth function import class Polly.

        .. code::


                from polly.auth import Polly
                Polly.auth(token)
        """
        # check if COMPUTE_ENV_VARIABLE present or not
        # if COMPUTE_ENV_VARIABLE, give priority
        env = helpers.get_platform_value_from_env(
            const.COMPUTE_ENV_VARIABLE, default_env, env
        )
        cls.default_session = PollySession(token, env=env)
        cls.default_session.mount(
            "https://",
            HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=retries),
        )
        cls._version_check()

    @classmethod
    def get_session(cls, token=None, env="polly"):
        """
        Function to get session from polly.

        ``Args:``
            |  ``token (str):`` token copy from polly.

        ``Returns:``
            |  if token is not satisfied it will throw UnauthorizedException.
            |  else it will return a polly.session object.

        ``Error:``
            |  ``UnauthorizedException:`` when the token is expired.

        To use get_sesion function import class Polly.


        .. code::


                from polly.auth import Polly
                session = Polly.get_session(token)

        """
        if token:
            cls.auth(token, env=env)
        else:
            if not cls.default_session:
                raise UnauthorizedException
        base_url = f"https://v2.api.{cls.default_session.env}.elucidata.io"
        cls.default_session.user_details = helpers.get_user_details(
            cls.default_session, base_url
        )
        return cls.default_session

    @classmethod
    def _version_check(cls):
        # check if session is already set, if not then only execute
        if not cls.auth_flag:
            polly_python_pypi_url = const.POLLY_PYTHON_PYPI_URL
            # GET Request to PYPI endpoint for fetching info about polly-py release versions
            try:
                text = requests.get(polly_python_pypi_url).content
                data = json.loads(text)
                versions_list = list(data.get("releases").keys())
                versions_list.sort(reverse=True)
                # Selecting the latest polly-py version from the list
                latest_version = versions_list[0]
                if latest_version != current_version:
                    print(
                        f"You're currently using an outdated version of polly-python '{current_version}'. \
Please update using the command \
'pip install polly-python=={latest_version}' to upgrade to the newest version '{latest_version}'"
                    )
            except Exception:
                # Exception to not interrupt the session build
                pass
            # set flag to true which means session has been set once
            cls.auth_flag = True
