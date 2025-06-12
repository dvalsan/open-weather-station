#!/bin/bash

# Start influxdb on background
influxd &

# Wait for the startup
echo "Waiting for IngluxDB startup..."
until curl -s http://localhost:8086/ping; do
  sleep 1
done

echo "InfluxDB is available. Executing configuration..."

influx -execute "CREATE DATABASE telegraf"
influx -execute "CREATE USER telegraf WITH PASSWORD 'telegrafroot'"
influx -execute "GRANT ALL ON telegraf TO telegraf"
influx -execute "CREATE RETENTION POLICY thirty_days ON telegraf DURATION 30d REPLICATION 1 DEFAULT"

# Maintain the process active
wait
