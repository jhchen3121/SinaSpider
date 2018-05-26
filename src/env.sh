PROJ_DIR=`pwd`
VENV=${PROJ_DIR}/.env
PROJ_NAME=sinaspider

if [ ! -e ${VENV} ];then
    virtualenv --never-download --prompt "(${PROJ_NAME})" ${VENV} -p $(type -p python)
fi

source ${VENV}/bin/activate

export PYTHONPATH=${PROJ_DIR}:${PROJ_DIR}/modules

export PROJ_NAME
export PROJ_DIR

