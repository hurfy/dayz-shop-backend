import pytest
import respx

from httpx               import Response
from re                  import match

from gateway.app.modules import SteamService
from gateway.app.errors  import SteamRequestError, SteamCheckError
from gateway.app.dto     import SteamLogin


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response_text, status_code, expected_result, expected_exception",
    [
        ("ns:http://specs.openid.net/auth/2.0\nis_valid:true" , 200, True , None),
        ("ns:http://specs.openid.net/auth/2.0\nis_valid:false", 200, False, None),
        ("Bad Body"                                           , 200, None , SteamCheckError),
        ("Request Failed"                                     , 500, None , SteamRequestError),
    ],
)
async def test_check_auth(
        steam_service     : SteamService,
        response_text     : str,
        status_code       : int,
        expected_result   : bool | None,
        expected_exception: type[Exception] | None
) -> None:
    """test_check_auth ..."""
    with respx.mock:
        respx.get(steam_service.url).mock(
            return_value=Response(status_code=status_code, text=response_text)
        )

        # Bad request or body
        if expected_exception:
            with pytest.raises(expected_exception):
                await steam_service.check_auth()

        else:
            result: bool = await steam_service.check_auth()

            assert isinstance(result, bool)
            assert result == expected_result


@pytest.mark.asyncio
async def test_get_steam_id(steam_service: SteamService, steam_id_re_pattern: str, steam_login: SteamLogin) -> None:
    """test_get_steam_id ..."""
    steam_id: str = await steam_service.get_steam_id()

    assert steam_id is not None
    assert isinstance(steam_id, str)
    assert match(steam_id_re_pattern, steam_id)

    assert steam_id == steam_login.claimed_id.split("/")[-1]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "text, expected_result, expected_exception",
    [
        ("ns:http://specs.openid.net/auth/2.0\nis_valid:true" , True , None),
        ("ns:http://specs.openid.net/auth/2.0\nis_valid:false", False, None),
        ("Bad Text"                                           , None , SteamCheckError),
    ]
)
async def test_parse_status(
        steam_service     : SteamService,
        text              : str,
        expected_result   : bool | None,
        expected_exception: type[Exception] | None
) -> None:
    """test_parse_status ..."""
    if expected_exception:
        with pytest.raises(expected_exception):
            await steam_service._parse_status(text)

    else:
        status: bool = await steam_service._parse_status(text)

        assert status is not None
        assert isinstance(status, bool)

        assert status == expected_result
