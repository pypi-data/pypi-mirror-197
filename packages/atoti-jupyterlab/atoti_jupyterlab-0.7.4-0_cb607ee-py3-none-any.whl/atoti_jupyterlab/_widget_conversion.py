from typing import Callable, Dict

from atoti_query import QueryResult

from ._mime_types import CONVERT_QUERY_RESULT_TO_WIDGET_MIME_TYPE

_ReprMimebundle = Callable[[QueryResult, object, object], Dict[str, object]]


def create_query_result_repr_mimebundle_method_(
    *, original_method: _ReprMimebundle
) -> _ReprMimebundle:
    def _repr_mimebundle_(  # pylint: disable=too-many-positional-parameters
        query_result: QueryResult,
        include: object,
        exclude: object,
    ) -> Dict[str, object]:
        mimebundle = dict(original_method(query_result, include, exclude))

        if (
            query_result._atoti_widget_conversion_details
            and not query_result._has_been_mutated()
        ):
            mimebundle[CONVERT_QUERY_RESULT_TO_WIDGET_MIME_TYPE] = {
                "mdx": query_result._atoti_widget_conversion_details.mdx,
                "sessionId": query_result._atoti_widget_conversion_details.session_id,
                "widgetCreationCode": query_result._atoti_widget_conversion_details.widget_creation_code,
            }

        return mimebundle

    return _repr_mimebundle_
