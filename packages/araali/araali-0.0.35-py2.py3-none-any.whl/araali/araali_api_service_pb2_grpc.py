# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import araali_api_service_pb2 as araali__api__service__pb2


class AraaliAPIStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.createTenant = channel.unary_unary(
                '/araali_api_service.AraaliAPI/createTenant',
                request_serializer=araali__api__service__pb2.CreateTenantRequest.SerializeToString,
                response_deserializer=araali__api__service__pb2.CreateTenantResponse.FromString,
                )
        self.deleteTenant = channel.unary_unary(
                '/araali_api_service.AraaliAPI/deleteTenant',
                request_serializer=araali__api__service__pb2.DeleteTenantRequest.SerializeToString,
                response_deserializer=araali__api__service__pb2.AraaliAPIResponse.FromString,
                )
        self.addUser = channel.unary_unary(
                '/araali_api_service.AraaliAPI/addUser',
                request_serializer=araali__api__service__pb2.AddUserRequest.SerializeToString,
                response_deserializer=araali__api__service__pb2.AraaliAPIResponse.FromString,
                )
        self.deleteUser = channel.unary_unary(
                '/araali_api_service.AraaliAPI/deleteUser',
                request_serializer=araali__api__service__pb2.DeleteUserRequest.SerializeToString,
                response_deserializer=araali__api__service__pb2.AraaliAPIResponse.FromString,
                )
        self.listAssets = channel.unary_unary(
                '/araali_api_service.AraaliAPI/listAssets',
                request_serializer=araali__api__service__pb2.ListAssetsRequest.SerializeToString,
                response_deserializer=araali__api__service__pb2.ListAssetsResponse.FromString,
                )
        self.listAlerts = channel.unary_unary(
                '/araali_api_service.AraaliAPI/listAlerts',
                request_serializer=araali__api__service__pb2.ListAlertsRequest.SerializeToString,
                response_deserializer=araali__api__service__pb2.ListAlertsResponse.FromString,
                )
        self.listLinks = channel.unary_unary(
                '/araali_api_service.AraaliAPI/listLinks',
                request_serializer=araali__api__service__pb2.ListLinksRequest.SerializeToString,
                response_deserializer=araali__api__service__pb2.ListLinksResponse.FromString,
                )
        self.listInsights = channel.unary_unary(
                '/araali_api_service.AraaliAPI/listInsights',
                request_serializer=araali__api__service__pb2.ListInsightsRequest.SerializeToString,
                response_deserializer=araali__api__service__pb2.ListInsightsResponse.FromString,
                )
        self.createFortifyYaml = channel.unary_unary(
                '/araali_api_service.AraaliAPI/createFortifyYaml',
                request_serializer=araali__api__service__pb2.CreateFortifyYamlRequest.SerializeToString,
                response_deserializer=araali__api__service__pb2.CreateFortifyYamlResponse.FromString,
                )
        self.listFortifyYaml = channel.unary_unary(
                '/araali_api_service.AraaliAPI/listFortifyYaml',
                request_serializer=araali__api__service__pb2.ListFortifyYamlRequest.SerializeToString,
                response_deserializer=araali__api__service__pb2.ListFortifyYamlResponse.FromString,
                )
        self.deleteFortifyYaml = channel.unary_unary(
                '/araali_api_service.AraaliAPI/deleteFortifyYaml',
                request_serializer=araali__api__service__pb2.DeleteFortifyYamlRequest.SerializeToString,
                response_deserializer=araali__api__service__pb2.AraaliAPIResponse.FromString,
                )
        self.listPolicyAndEnforcementStatus = channel.unary_unary(
                '/araali_api_service.AraaliAPI/listPolicyAndEnforcementStatus',
                request_serializer=araali__api__service__pb2.ListPolicyAndEnforcementStatusRequest.SerializeToString,
                response_deserializer=araali__api__service__pb2.ListPolicyAndEnforcementStatusResponse.FromString,
                )
        self.getFirewallConfig = channel.unary_unary(
                '/araali_api_service.AraaliAPI/getFirewallConfig',
                request_serializer=araali__api__service__pb2.GetFirewallConfigRequest.SerializeToString,
                response_deserializer=araali__api__service__pb2.FirewallConfigResponse.FromString,
                )
        self.updateFirewallConfig = channel.unary_unary(
                '/araali_api_service.AraaliAPI/updateFirewallConfig',
                request_serializer=araali__api__service__pb2.UpdateFirewallConfigRequest.SerializeToString,
                response_deserializer=araali__api__service__pb2.FirewallConfigResponse.FromString,
                )


class AraaliAPIServicer(object):
    """Missing associated documentation comment in .proto file."""

    def createTenant(self, request, context):
        """Add a tenant
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def deleteTenant(self, request, context):
        """Delete a tenant
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def addUser(self, request, context):
        """Add a user
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def deleteUser(self, request, context):
        """Delete a user
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def listAssets(self, request, context):
        """Get assets
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def listAlerts(self, request, context):
        """Get alerts
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def listLinks(self, request, context):
        """Get links within a zone/app
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def listInsights(self, request, context):
        """Get tenant wide insights
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def createFortifyYaml(self, request, context):
        """Generate k8s workload/helm values (also registers workloadID)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def listFortifyYaml(self, request, context):
        """List existing k8s workloads
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def deleteFortifyYaml(self, request, context):
        """Delete existing k8s workload
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def listPolicyAndEnforcementStatus(self, request, context):
        """Download policy and enforcement knobs as code.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getFirewallConfig(self, request, context):
        """Get existing Araali firewall config
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def updateFirewallConfig(self, request, context):
        """Update existing Araali firewall config
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AraaliAPIServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'createTenant': grpc.unary_unary_rpc_method_handler(
                    servicer.createTenant,
                    request_deserializer=araali__api__service__pb2.CreateTenantRequest.FromString,
                    response_serializer=araali__api__service__pb2.CreateTenantResponse.SerializeToString,
            ),
            'deleteTenant': grpc.unary_unary_rpc_method_handler(
                    servicer.deleteTenant,
                    request_deserializer=araali__api__service__pb2.DeleteTenantRequest.FromString,
                    response_serializer=araali__api__service__pb2.AraaliAPIResponse.SerializeToString,
            ),
            'addUser': grpc.unary_unary_rpc_method_handler(
                    servicer.addUser,
                    request_deserializer=araali__api__service__pb2.AddUserRequest.FromString,
                    response_serializer=araali__api__service__pb2.AraaliAPIResponse.SerializeToString,
            ),
            'deleteUser': grpc.unary_unary_rpc_method_handler(
                    servicer.deleteUser,
                    request_deserializer=araali__api__service__pb2.DeleteUserRequest.FromString,
                    response_serializer=araali__api__service__pb2.AraaliAPIResponse.SerializeToString,
            ),
            'listAssets': grpc.unary_unary_rpc_method_handler(
                    servicer.listAssets,
                    request_deserializer=araali__api__service__pb2.ListAssetsRequest.FromString,
                    response_serializer=araali__api__service__pb2.ListAssetsResponse.SerializeToString,
            ),
            'listAlerts': grpc.unary_unary_rpc_method_handler(
                    servicer.listAlerts,
                    request_deserializer=araali__api__service__pb2.ListAlertsRequest.FromString,
                    response_serializer=araali__api__service__pb2.ListAlertsResponse.SerializeToString,
            ),
            'listLinks': grpc.unary_unary_rpc_method_handler(
                    servicer.listLinks,
                    request_deserializer=araali__api__service__pb2.ListLinksRequest.FromString,
                    response_serializer=araali__api__service__pb2.ListLinksResponse.SerializeToString,
            ),
            'listInsights': grpc.unary_unary_rpc_method_handler(
                    servicer.listInsights,
                    request_deserializer=araali__api__service__pb2.ListInsightsRequest.FromString,
                    response_serializer=araali__api__service__pb2.ListInsightsResponse.SerializeToString,
            ),
            'createFortifyYaml': grpc.unary_unary_rpc_method_handler(
                    servicer.createFortifyYaml,
                    request_deserializer=araali__api__service__pb2.CreateFortifyYamlRequest.FromString,
                    response_serializer=araali__api__service__pb2.CreateFortifyYamlResponse.SerializeToString,
            ),
            'listFortifyYaml': grpc.unary_unary_rpc_method_handler(
                    servicer.listFortifyYaml,
                    request_deserializer=araali__api__service__pb2.ListFortifyYamlRequest.FromString,
                    response_serializer=araali__api__service__pb2.ListFortifyYamlResponse.SerializeToString,
            ),
            'deleteFortifyYaml': grpc.unary_unary_rpc_method_handler(
                    servicer.deleteFortifyYaml,
                    request_deserializer=araali__api__service__pb2.DeleteFortifyYamlRequest.FromString,
                    response_serializer=araali__api__service__pb2.AraaliAPIResponse.SerializeToString,
            ),
            'listPolicyAndEnforcementStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.listPolicyAndEnforcementStatus,
                    request_deserializer=araali__api__service__pb2.ListPolicyAndEnforcementStatusRequest.FromString,
                    response_serializer=araali__api__service__pb2.ListPolicyAndEnforcementStatusResponse.SerializeToString,
            ),
            'getFirewallConfig': grpc.unary_unary_rpc_method_handler(
                    servicer.getFirewallConfig,
                    request_deserializer=araali__api__service__pb2.GetFirewallConfigRequest.FromString,
                    response_serializer=araali__api__service__pb2.FirewallConfigResponse.SerializeToString,
            ),
            'updateFirewallConfig': grpc.unary_unary_rpc_method_handler(
                    servicer.updateFirewallConfig,
                    request_deserializer=araali__api__service__pb2.UpdateFirewallConfigRequest.FromString,
                    response_serializer=araali__api__service__pb2.FirewallConfigResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'araali_api_service.AraaliAPI', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AraaliAPI(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def createTenant(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/araali_api_service.AraaliAPI/createTenant',
            araali__api__service__pb2.CreateTenantRequest.SerializeToString,
            araali__api__service__pb2.CreateTenantResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def deleteTenant(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/araali_api_service.AraaliAPI/deleteTenant',
            araali__api__service__pb2.DeleteTenantRequest.SerializeToString,
            araali__api__service__pb2.AraaliAPIResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def addUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/araali_api_service.AraaliAPI/addUser',
            araali__api__service__pb2.AddUserRequest.SerializeToString,
            araali__api__service__pb2.AraaliAPIResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def deleteUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/araali_api_service.AraaliAPI/deleteUser',
            araali__api__service__pb2.DeleteUserRequest.SerializeToString,
            araali__api__service__pb2.AraaliAPIResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def listAssets(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/araali_api_service.AraaliAPI/listAssets',
            araali__api__service__pb2.ListAssetsRequest.SerializeToString,
            araali__api__service__pb2.ListAssetsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def listAlerts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/araali_api_service.AraaliAPI/listAlerts',
            araali__api__service__pb2.ListAlertsRequest.SerializeToString,
            araali__api__service__pb2.ListAlertsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def listLinks(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/araali_api_service.AraaliAPI/listLinks',
            araali__api__service__pb2.ListLinksRequest.SerializeToString,
            araali__api__service__pb2.ListLinksResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def listInsights(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/araali_api_service.AraaliAPI/listInsights',
            araali__api__service__pb2.ListInsightsRequest.SerializeToString,
            araali__api__service__pb2.ListInsightsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def createFortifyYaml(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/araali_api_service.AraaliAPI/createFortifyYaml',
            araali__api__service__pb2.CreateFortifyYamlRequest.SerializeToString,
            araali__api__service__pb2.CreateFortifyYamlResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def listFortifyYaml(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/araali_api_service.AraaliAPI/listFortifyYaml',
            araali__api__service__pb2.ListFortifyYamlRequest.SerializeToString,
            araali__api__service__pb2.ListFortifyYamlResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def deleteFortifyYaml(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/araali_api_service.AraaliAPI/deleteFortifyYaml',
            araali__api__service__pb2.DeleteFortifyYamlRequest.SerializeToString,
            araali__api__service__pb2.AraaliAPIResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def listPolicyAndEnforcementStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/araali_api_service.AraaliAPI/listPolicyAndEnforcementStatus',
            araali__api__service__pb2.ListPolicyAndEnforcementStatusRequest.SerializeToString,
            araali__api__service__pb2.ListPolicyAndEnforcementStatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getFirewallConfig(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/araali_api_service.AraaliAPI/getFirewallConfig',
            araali__api__service__pb2.GetFirewallConfigRequest.SerializeToString,
            araali__api__service__pb2.FirewallConfigResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def updateFirewallConfig(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/araali_api_service.AraaliAPI/updateFirewallConfig',
            araali__api__service__pb2.UpdateFirewallConfigRequest.SerializeToString,
            araali__api__service__pb2.FirewallConfigResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
