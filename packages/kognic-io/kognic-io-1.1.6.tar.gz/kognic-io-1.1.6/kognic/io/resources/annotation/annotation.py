from typing import Optional, Generator

from kognic.io.model.annotation.client_annotation import Annotation, PartialAnnotation
from kognic.io.resources.abstract import IOResource


class AnnotationResource(IOResource):

    def get_project_annotations(self,
                                project: str,
                                annotation_type: str,
                                batch: Optional[str] = None,
                                include_content: bool = True,
                                ) -> Generator[Annotation, None, None]:
        """
        Gets annotations for a project and annotation type with an optional filter for a batch.
        Annotations include annotation contents which means that this function is heavier than `get_partial_annotations`
        that only gets partial annotations.

        :param project: project to query annotations from
        :param annotation_type: annotation type to query annotation on
        :param batch: batch to filter on (optional)
        :param include_content: whether to include annotation content (default: True)
        :returns Generator[Annotation]: Generator of annotations
        """

        url = f"v1/annotations/projects/{project}/"
        if batch:
            url += f"batch/{batch}/"

        url += f"annotation-type/{annotation_type}/search"

        for js in self._paginate_get(url):
            partial_annotation = PartialAnnotation.from_json(js)
            content = self._file_client.get_json(partial_annotation.uri) if include_content else None
            yield partial_annotation.to_annotation(content)

    def get_annotation(self, input_uuid: str, annotation_type: str) -> Annotation:
        """
        Gets an annotations for an input and annotation type. A NotFound exception will be raised if there isn't any
        annotation for the given uuid and annotation type. Use `client.input.get_inputs_by_uuids` to find out whether
        the input has been configured for the annotation type or not.

        :param input_uuid: uuid of the input
        :param annotation_type: annotation type to get annotation for
        :returns Annotation: annotation with its content
        """
        json_resp = self._client.get(f"v1/annotations/inputs/{input_uuid}/annotation-type/{annotation_type}")
        annotation = Annotation.from_json(json_resp)
        return annotation
