#!/bin/bash


if [[ -z "$DEFAULT_LLM_MODEL" && -n "$AVAILABLE_LLM_MODELS" && -n "$(which fzf)" ]]; then
    export DEFAULT_LLM_MODEL=`echo "$AVAILABLE_LLM_MODELS" | fzf`
fi

export DEFAULT_OLLAMA_HOST="${DEFAULT_OLLAMA_HOST:-localhost}"
export DEFAULT_OLLAMA_PORT="${DEFAULT_OLLAMA_PORT:-11434}"

export OLLAMA_HOST="${OLLAMA_HOST:-$DEFAULT_OLLAMA_HOST}"
export OLLAMA_PORT="${OLLAMA_PORT:-$DEFAULT_OLLAMA_PORT}"

export DEFAULT_LLM_BASE_URL="http://$OLLAMA_HOST:$OLLAMA_PORT"
export LLM_BASE_URL="${LLM_BASE_URL:-$DEFAULT_LLM_BASE_URL}"


stop_local_ollama() {
    sudo systemctl stop ollama
    sudo pkill -9 ollama
}

# https://superuser.com/a/1658519
forward_ssh() {
    ssh -NT -o ServerAliveInterval=60 -o ServerAliveCountMax=10 -o ExitOnForwardFailure=yes -L "$OLLAMA_PORT:localhost:$DEFAULT_OLLAMA_PORT" $@
}

connect_gpu_server() {
    if [[ "$STOP_LOCAL_OLLAMA" = 'TRUE' ]]; then
        stop_local_ollama
    fi 
    if [[ -z "$SSH_OLLAMA" ]]; then
        echo 'Environment variable $SSH_OLLAMA is not defined'
        exit 1
    fi
    forward_ssh "$SSH_OLLAMA"
}

check_ollama() {
    netstat -tulpn | grep "$OLLAMA_PORT"
}


# if [[ -n "$SSH_OLLAMA" ]]; then
#     connect_gpu_server 2>/dev/null &
# fi


