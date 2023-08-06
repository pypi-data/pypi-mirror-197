from typing import TYPE_CHECKING,TypeVar as _TypeVar


# ---------------------------------------------------------------------------- #
#                               TYPE DECLARATIONS                              #
# ---------------------------------------------------------------------------- #

_main_type = None
_result_type = None

if TYPE_CHECKING:

    import main as _m
    _main_type = _TypeVar('_main_type', bound=_m.Main)

    from copper_rabbit.support.Result import Result as _DjKQ
    _result_type = _TypeVar('_result_type', bound=_DjKQ)

