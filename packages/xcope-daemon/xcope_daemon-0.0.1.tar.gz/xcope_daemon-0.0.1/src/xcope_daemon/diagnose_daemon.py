import logging
import grpc
from diagnose_daemon_pb2 import GetFeedRequest, PostFeedRequest, PostResultRequest
from config import GrpcHost, GrpcPort
from diagnose_daemon_pb2_grpc import DiagnoseDaemonStub

logger = logging.getLogger(__name__)


class DiagnoseDaemon:
    def __init__(self, taskId) -> None:
        self.taskId = taskId
        channel = grpc.insecure_channel(
            f"{GrpcHost}:{GrpcPort}")
        self.client = DiagnoseDaemonStub(channel)
        logger.info(f"Grpc channel {GrpcHost}:{GrpcPort} established.")

    def get_feed_steam(self):
        return self.client.GetFeedStream(GetFeedRequest(
            clientAddress=self.taskId
        ))

    def post_feed_result(self, feedId):
        logger.info(f"Post feed result {self.taskId}-{feedId}")
        self.client.PostFeedResult(PostFeedRequest(
            clientAddress=self.taskId,
            feedId=feedId
        ))

    def post_result(self, prediction, payload):
        self.client.PostDiagnoseResult(PostResultRequest(
            clientAddress=self.taskId,
            isError=False,
            errorMessage="",
            prediction=prediction,
            payload=payload
        ))

    def post_error(self, error_message):
        self.client.PostDiagnoseResult(PostResultRequest(
            clientAddress=self.taskId,
            isError=True,
            errorMessage=error_message
        ))
