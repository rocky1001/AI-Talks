#!/bin/env bash

#exist pid
pid=$(pgrep "streamlit")
if [[ -n $pid ]]; then
  if kill -9 "$pid"; then
    echo "killed running app[$pid]"
  fi
fi

source activate chatgpt-st
echo 'starting streamlit app...'
nohup streamlit run ai_talks/chat.py --server.headless true >>./run.log 2>&1 &
sleep 2

pid=$(pgrep "streamlit")
if [[ -n $pid ]]; then
  echo "app started succeed"
fi
