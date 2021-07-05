from __future__ import absolute_import
from collections import defaultdict
import copy
import logging
import socket
from sys import version
from kafka.vendor import six
from kafka.client_async import KafkaClient, selectors
import kafka.errors as Errors
from kafka.errors import (
    IncompatibleBrokerVersion, KafkaConfigurationError, NotControllerError,
    UnrecognizedBrokerVersion, IllegalArgumentError
)
from kafka.metrics import MetricConfig, Metrics
from kafka.protocol.admin import (
    CreateTopicsRequest, DeleteTopicsRequest, DescribeConfigsRequest, AlterConfigsRequest, CreatePartitionsRequest,
    ListGroupsRequest, DescribeGroupsRequest, DescribeAclsRequest, CreateAclsRequest, DeleteAclsRequest)
from kafka.protocol.commit import GroupCoordinatorRequest, OffsetFetchRequest
from kafka.protocol.metadata import MetadataRequest
from kafka.structs import TopicPartition, OffsetAndMetadata
from kafka.admin.acl_resource import ACLOperation, ACLPermissionType, ACLFilter, ACL, ResourcePattern, ResourceType, \
    ACLResourcePatternType
from kafka.version import __version__

log = logging.getLogger(__name__)

class KafkaAdminClient(object):

    DEFAULT_CONFIG = {
        # client configs
        'bootstrap_servers': 'localhost:9092',
        'client_id': 'kafka-python-' + __version__,
        'request_timeout_ms': 30000,
        'connections_max_idle_ms': 9 * 60 * 1000,
        'reconnect_backoff_ms': 50,
        'reconnect_backoff_max_ms': 1000,
        'max_in_flight_requests_per_connection': 5,
        'receive_buffer_bytes': None,
        'send_buffer_bytes': None,
        'socket_options': [(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)],
        'sock_chunk_bytes': 4096,  # undocumented experimental option
        'sock_chunk_buffer_count': 1000,  # undocumented experimental option
        'retry_backoff_ms': 100,
        'metadata_max_age_ms': 300000,
        'security_protocol': 'PLAINTEXT',
        'ssl_context': None,
        'ssl_check_hostname': True,
        'ssl_cafile': None,
        'ssl_certfile': None,
        'ssl_keyfile': None,
        'ssl_password': None,
        'ssl_crlfile': None,
        'api_version': None,
        'api_version_auto_timeout_ms': 2000,
        'selector': selectors.DefaultSelector,
        'sasl_mechanism': None,
        'sasl_plain_username': None,
        'sasl_plain_password': None,
        'sasl_kerberos_service_name': 'kafka',
        'sasl_kerberos_domain_name': None,
        'sasl_oauth_token_provider': None,

        # metrics configs
        'metric_reporters': [],
        'metrics_num_samples': 2,
        'metrics_sample_window_ms': 30000,
    }

    def __init__(self, **configs):
        log.debug("Starting KafkaAdminClient with configuration: %s", configs)
        extra_configs = set(configs).difference(self.DEFAULT_CONFIG)
        if extra_configs:
            raise KafkaConfigurationError("Unrecognized configs: {}".format(extra_configs))
        self.config = copy.copy(self.DEFAULT_CONFIG)
        self.config.update(configs)

        # Configure metrics
        metrics_tags = {"client_id": self.config["client_id"]}
        metric_config = MetricConfig(samples=self.config["metrics_num_samples"],
                                     time_window_ms=self.config["metrics_sample_window_ms"],
                                     tags=metrics_tags)
        reporters = [reporter() for reporter in self.config["metric_reporters"]]
        self._metrics = Metrics(metric_config,reporters=reporters)
        self._client = KafkaClient(metrics=self._metrics,metric_group_prefix='admin',**self.config)
        self._client.check_version()

        # Get auto-discovered version from client if necessary
        if self.config["api_version"] is None:
            self.config["api_version"] = self._client.config["api_version"]
        self._closed = False
        self._refresh_controller_id()
        log.debug("KafkaAdminClient started.")

    def _matching_api_version(self, operation):
        """Find the latest version of the protocol operation supported by both
        this library and the broker.

        This resolves to the lesser of either the latest api version this
        library supports, or the max version supported by the broker.

        :param operation: A list of protocol operation versions from kafka.protocol.
        :return: The max matching version number between client and broker.
        """
        broker_api_versions = self._client.get_api_versions()
        api_key = operation[0].API_KEY
        if broker_api_versions is None or api_key not in broker_api_versions:
            raise IncompatibleBrokerVersion(
                "Kafka broker does not support the '{}' Kafka protocol."
                .format(operation[0].__name__))
        min_version, max_version = broker_api_versions[api_key]
        version = min(len(operation) - 1, max_version)
        if version < min_version:
            # max library version is less than min broker version. Currently,
            # no Kafka versions specify a min msg version. Maybe in the future?
            raise IncompatibleBrokerVersion(
                "No version of the '{}' Kafka protocol is supported by both the client and broker."
                .format(operation[0].__name__))
        return version

    def _refresh_controller_id(self):
        """Determine the Kafka cluster controller."""
        version = self._matching_api_version(MetadataRequest)
        if 1 <= version <= 6:
            request = MetadataRequest[version]()
            future = self._send_request_to_node(self._client.least_loaded_node(), request)

            self._wait_for_futures([future])

            response = future.value
            controller_id = response.controller_id
            # verify the controller is new enough to support our requests
            controller_version = self._client.check_version(controller_id)
            if controller_version < (0, 10, 0):
                raise IncompatibleBrokerVersion(
                    "The controller appears to be running Kafka {}. KafkaAdminClient requires brokers >= 0.10.0.0."
                    .format(controller_version))
            self._controller_id = controller_id
        else:
            raise UnrecognizedBrokerVersion(
                "Kafka Admin interface cannot determine the controller using MetadataRequest_v{}."
                .format(version))

    def _validate_timeout(self,timeout_ms):
        """Validate the timeout is set or use the configuration default.
        :param timeout_ms: The timeout provided by api call, in milliseconds.
        :return: The timeout to use for the operation.
        """
        return timeout_ms or self.config["request_timeout_ms"]

    def _send_request_to_node(self, node_id, request):
        """Send a Kafka protocol message to a specific broker.

        Returns a future that may be polled for status and results.

        :param node_id: The broker id to which to send the message.
        :param request: The message to send.
        :return: A future object that may be polled for status and results.
        :exception: The exception if the message could not be sent.
        """
        while not self._client.ready(node_id):
            # poll until the connection to broker is ready, otherwise send()
            # will fail with NodeNotReadyError
            self._client.poll()
        return self._client.send(node_id, request)

    def _wait_for_futures(self, futures):
        while not all(future.succeeded() for future in futures):
            for future in futures:
                self._client.poll(future=future)

                if future.failed():
                    raise future.exception

    def _send_request_to_controller(self,request):
        """Send a Kafka protocol message to the cluster controller.

        Will block until the message result is received.

        :param request: The message to send.
        :return: The Kafka protocol response for the message.
        """
        tries = 2  # in case our cached self._controller_id is outdated
        while tries:
            tries -= 1
            future = self._send_request_to_node(self._controller_id, request)

            self._wait_for_futures([future])

            response = future.value
            topic_error_tuples = (response.topic_errors if hasattr(response, 'topic_errors')
                    else response.topic_error_codes)
            for topic, error_code in map(lambda e: e[:2], topic_error_tuples):
                error_type = Errors.for_code(error_code)
                if tries and error_type is NotControllerError:
                    self._refresh_controller_id()
                    break
                elif error_type is not Errors.NoError:
                    raise error_type(
                        "Request '{}' failed with response '{}'."
                        .format(request, response))
            else:
                return response
        raise RuntimeError("This should never happen, please file a bug with full stacktrace if encountered")

    @staticmethod
    def _convert_new_topic_request(new_topic):
        return (
            new_topic.name,
            new_topic.num_partitions,
            new_topic.replication_factor,
            [
                (partition_id, replicas) for partition_id, replicas in new_topic.replica_assignments.items()
            ],
            [
                (config_key, config_value) for config_key, config_value in new_topic.topic_configs.items()
            ]
        )

    def create_topics(self,new_topics, timeout_ms=None,validate_only=None):
        """Create new topics in the cluster.
        :param new_topics: A list of NewTopic objects.
        :param timeout_ms: Milliseconds to wait for new topics to be created
            before the broker returns.
        :param validate_only: If True, don't actually create new topics.
            Not supported by all versions. Default: False
        :return: Appropriate version of CreateTopicResponse class.
        """
        version = self._matching_api_version(CreateTopicsRequest)
        timeout_ms = self._validate_timeout(timeout_ms)
        if version==0:
            if validate_only:
                raise IncompatibleBrokerVersion(
                    "validate_only requires CreateTopicsRequest >= v1, which is not supported by Kafka {}."
                    .format(self.config["api_version"])
                )
            request = CreateTopicsRequest[version](
                create_topic_requests=[self._convert_new_topic_request(new_topics) for new_topic in new_topics],
                timeout=timeout_ms,
                validate_only=validate_only
            )
        elif version <= 3:
            request = CreateTopicsRequest[version](
                create_topic_requests=[self._convert_new_topic_request(new_topic) for new_topic in new_topics],
                timeout=timeout_ms,
                validate_only=validate_only
            )
        else:
            raise NotImplementedError(
                "Support for CreateTopics v{} has not yet been added to KafkaAdminclient."
                .format(version)
            )
        # TODO convert structs to a more pythonic interface
        # TODO raise exceptions if errors
        return self._send_request_to_controller(request)

    def delete_topics(self, topics, timeout_ms=None):
        """Delete topics from the cluster.

        :param topics: A list of topic name strings.
        :param timeout_ms: Milliseconds to wait for topics to be deleted
            before the broker returns.
        :return: Appropriate version of DeleteTopicsResponse class.
        """
        version = self._matching_api_version(DeleteTopicsRequest)
        timeout_ms = self._validate_timeout(timeout_ms)
        if version <= 3:
            request = DeleteTopicsRequest[version](
                topics=topics,
                timeout=timeout_ms
            )
            response = self._send_request_to_controller(request)
        else:
            raise NotImplementedError(
                "Support for DeleteTopics v{} has not yet been added to KafkaAdminClient."
                .format(version))
        return response

    def _get_cluster_metadata(self, topics=None, auto_topic_creation=False):
        """
        topics == None means "get all topics"
        """
        version = self._matching_api_version(MetadataRequest)
        if version <= 3:
            if auto_topic_creation:
                raise IncompatibleBrokerVersion(
                    "auto_topic_creation requires MetadataRequest >= v4, which"
                    " is not supported by Kafka {}"
                    .format(self.config['api_version']))

            request = MetadataRequest[version](topics=topics)
        elif version <= 5:
            request = MetadataRequest[version](
                topics=topics,
                allow_auto_topic_creation=auto_topic_creation
            )

        future = self._send_request_to_node(
            self._client.least_loaded_node(),
            request
        )
        self._wait_for_futures([future])
        return future.value

    def list_topics(self):
        metadata = self._get_cluster_metadata(topics=None)
        obj = metadata.to_object()
        return [t["topic"] for t in obj["topics"]]
    
    def describe_topics(self, topics=None):
        metadata = self._get_cluster_metadata(topics=topics)
        obj = metadata.to_object()
        return obj["topics"]

    def describe_cluster(self):
        metadata = self._get_cluster_metadata()
        obj = metadata.to_object()
        obj.pop('topics')
        return obj

    @staticmethod
    def _convert_create_partitions_request(topic_name, new_partitions):
        return (
            topic_name,
            (
                new_partitions.total_count,
                new_partitions.new_assignments
            )
        )
    
    def create_partitions(self, topic_partitions, timeout_ms=None, validate_only=False):
        """Create additional partitions for an existing topic.

        :param topic_partitions: A map of topic name strings to NewPartition objects.
        :param timeout_ms: Milliseconds to wait for new partitions to be
            created before the broker returns.
        :param validate_only: If True, don't actually create new partitions.
            Default: False
        :return: Appropriate version of CreatePartitionsResponse class.
        """
        version = self._matching_api_version(CreatePartitionsRequest)
        timeout_ms = self._validate_timeout(timeout_ms)
        if version <= 1:
            request = CreatePartitionsRequest[version](
                topic_partitions=[self._convert_create_partitions_request(topic_name, new_partitions) for topic_name, new_partitions in topic_partitions.items()],
                timeout=timeout_ms,
                validate_only=validate_only
            )
        else:
            raise NotImplementedError(
                "Support for CreatePartitions v{} has not yet been added to KafkaAdminClient."
                .format(version))
        return self._send_request_to_controller(request)

    