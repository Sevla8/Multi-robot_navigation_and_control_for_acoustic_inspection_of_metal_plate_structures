#!/usr/bin/env bash

while true
do
	./run_tests_investigate.sh &
	pid=$!
	sleep 600
	pkill -P $pid
done