
import os
import uuid

from docker_utils import is_docker


if is_docker():
    GrpcHost = "host.docker.internal"
else:
    GrpcHost = "localhost"


GrpcPort = 29689

# style like azure pipeline enviroment variables.
ArtifactStagingDirectory = "/a"
BinariesDirectory = "/b"
SourcesDirectory = "/s"

ArtifactInputDirectory = "/a/input"
ArtifactOutputDirectory = "/a/output"
ArtifactArgumentsDirectory = "/a/arguments"

GrpcHost = os.getenv('GrpcHost', GrpcHost)
GrpcPort = int(os.getenv('GrpcPort', str(GrpcPort)))
ArtifactStagingDirectory = os.getenv(
    'ArtifactStagingDirectory', ArtifactStagingDirectory)
BinariesDirectory = os.getenv(
    'BinariesDirectory', BinariesDirectory)
SourcesDirectory = os.getenv(
    'SourcesDirectory', SourcesDirectory)

ArtifactInputDirectory = os.getenv(
    'ArtifactInputDirectory', ArtifactInputDirectory
)

ArtifactOutputDirectory = os.getenv(
    'ArtifactOutputDirectory', ArtifactOutputDirectory
)

ArtifactArgumentsDirectory = os.getenv(
    'ArtifactArgumentsDirectory', ArtifactArgumentsDirectory
)


TaskId = os.getenv('TaskId', '')
