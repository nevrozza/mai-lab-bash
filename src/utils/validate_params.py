from src.core.errors import BashError


def default_validate_params(
        params: list[str],
        if_no_params,
        validate_path,
) -> list[BashError]:
    errors = []
    if not params:
        if_no_params and if_no_params()
    else:
        for path in params[:]:
            possible_error = validate_path(path)
            if isinstance(possible_error, BashError):
                errors.append(possible_error)
    return errors
