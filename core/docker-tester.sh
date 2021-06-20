#!/usr/bin/env bash

DOCKER_GROUP=$(ls -la /var/run/docker.sock | awk '{print $4}')
if [[ -z $DOCKER_GROUP ]]; then
    echo "Not exists docker group"
    exit 1
fi

DOCKER_GID=$(echo $DOCKER_GROUP | grep -E '^[0-9]+$')
if [[ -n $DOCKER_GID ]]; then
    DOCKER_GROUP=docker
    groupadd --gid $DOCKER_GID $DOCKER_GROUP
else
    groupadd $DOCKER_GROUP
fi

TEST_USER_NAME=tester

useradd --groups $DOCKER_GROUP $TEST_USER_NAME
su $TEST_USER_NAME << EOF
export RECC_TESTER=${RECC_TESTER:-True}

echo "[Environment variables]"
echo "- USER: \$USER"
echo "- HOME: \$HOME"
echo "- SHELL: \$SHELL"
echo "- RECC_TESTER: \$RECC_TESTER"

./ci.sh
EOF
