from rest_framework import serializers

from orchestra.api import router
from orchestra.utils import running_syncdb

from .models import Resource, ResourceData


class ResourceSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')
    
    class Meta:
        model = ResourceData
        fields = ('name', 'used', 'allocated')
        read_only_fields = ('used',)
    
    def get_name(self, instance):
        return instance.resource.name
    
    def get_identity(self, data):
        return data.get('name')


# Monkey-patching section

if not running_syncdb():
    # TODO why this is even loaded during syncdb?
    # Create nested serializers on target models
    for ct, resources in Resource.objects.group_by('content_type').iteritems():
        model = ct.model_class()
        try:
            router.insert(model, 'resources', ResourceSerializer, required=False, many=True, source='resource_set')
        except KeyError:
            continue
        
        def validate_resources(self, attrs, source, _resources=resources):
            """ Creates missing resources """
            posted = attrs.get(source, [])
            result = []
            resources = list(_resources)
            for data in posted:
                resource = data.resource
                if resource not in resources:
                    msg = "Unknown or duplicated resource '%s'." % resource
                    raise serializers.ValidationError(msg)
                resources.remove(resource)
                if not resource.ondemand and not data.allocated:
                    data.allocated = resource.default_allocation
                result.append(data)
            for resource in resources:
                data = ResourceData(resource=resource)
                if not resource.ondemand:
                    data.allocated = resource.default_allocation
                result.append(data)
            attrs[source] = result
            return attrs
        viewset = router.get_viewset(model)
        viewset.serializer_class.validate_resources = validate_resources
        
        old_metadata = viewset.metadata
        def metadata(self, request, resources=resources):
            """ Provides available resources description """
            ret = old_metadata(self, request)
            ret['available_resources'] = [
                {
                    'name': resource.name,
                    'ondemand': resource.ondemand,
                    'default_allocation': resource.default_allocation
                } for resource in resources
            ]
            return ret
        viewset.metadata = metadata
