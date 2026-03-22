from __future__ import annotations


class IikoApiError(Exception):
    def __init__(
        self,
        *,
        status_code: int,
        correlation_id: str | None = None,
        error: str | None = None,
        error_description: str | None = None,
        error_field: str | None = None,
    ) -> None:
        self.status_code = status_code
        self.correlation_id = correlation_id
        self.error = error
        self.error_description = error_description
        self.error_field = error_field

        description = error_description or error or "Unknown iiko API error"
        super().__init__(f"iiko API error {status_code}: {description}")
