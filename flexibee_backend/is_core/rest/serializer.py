from django.utils.datastructures import SortedDict

from pyston.serializer import Serializer, register, ModelSerializer

from flexibee_backend.models.fields import ItemsManager
from flexibee_backend.models import FlexibeeItem


@register
class FlexibeeItemsManagerSerializer(Serializer):

    def _to_python(self, request, manager, serialization_format, **kwargs):
        return [self._to_python_chain(request, obj, serialization_format, **kwargs) for obj in manager.all()]

    def _can_transform_to_python(self, thing):
        return isinstance(thing, ItemsManager)


@register
class ItemSerializer(ModelSerializer):

    def _fields_to_python(self, request, obj, serialization_format, fieldset, requested_fieldset, **kwargs):
        resource_method_fields = self._get_resource_method_fields(self._get_model_resource(request, obj), fieldset)
        out = SortedDict()
        for field in fieldset.fields:
            subkwargs = self._copy_kwargs(self._get_model_resource(request, obj), kwargs)
            requested_field = None
            if requested_fieldset:
                requested_field = requested_fieldset.get(field.name)
            field_name = self._get_field_name(field, requested_field, subkwargs)
            if field_name in resource_method_fields:
                out[field_name] = self._method_to_python(resource_method_fields[field_name], request, obj,
                                                         serialization_format, **subkwargs)
            else:
                out[field_name] = self._to_python_chain(request, self._get_value(obj, field_name), format, **subkwargs)
        return out

    def _get_value(self, obj, field):
        return getattr(obj, field)

    def _can_transform_to_python(self, thing):
        return isinstance(thing, FlexibeeItem)
