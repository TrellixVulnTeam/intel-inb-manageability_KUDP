#!/bin/bash

set -euxo pipefail

cd /vagrant/input

cp /scripts/succeed_rpm_cert.pem .

apt-get update
apt-get install -yq lxc tpm2-tools tpm2-abrmd

mkdir "install_TC"
cd "install_TC"
cp ../*.preview.tar.gz .
cp ../*-tc.sh .
rm -rf /etc/intel-manageability/public/cloudadapter-agent
mkdir -p /etc/intel-manageability/public/cloudadapter-agent
apt-get purge -y docker-ce docker-ce-cli || true
rm -rf /var/lib/apt/lists/*

# Update shell to force dpkg to use bash during installation.
echo "dash dash/sh boolean false" | debconf-set-selections
if ! dpkg-reconfigure dash -f noninteractive; then
  echo "Unable to configure environment (dash->bash)"
  exit 1
fi


tar -zxvf *.preview.tar.gz

# No DBS -- will disable a bit further down.

# workaround for docker-compose credential helper
mv /usr/bin/docker-credential-secretservice /usr/bin/docker-credential-secretservice.broken || true

dpkg -i tpm-provision*.deb
dpkg -i mqtt-*.deb
dpkg -i trtl-*.deb
dpkg -i inbc-*.deb
dpkg -i ./inbm-telemetry-agent-*.deb
dpkg -i ./inbm-configuration-agent-*.deb
dpkg -i ./inbm-dispatcher-agent-*.deb
dpkg -i ./inbm-diagnostic-agent-*.deb
dpkg -i ./inbm-cloudadapter-agent-*.deb


for i in dispatcher telemetry configuration diagnostic ; do
  sed -i 's/ERROR/DEBUG/g' /etc/intel-manageability/public/"$i"-agent/logging.ini
done

cp /scripts/iotg_inb_developer.conf /etc/intel_manageability.conf
cp /scripts/inb_fw_tool_info.conf /etc/firmware_tool_info.conf

# Disable DBS in Intel(R) In-Band Manageability config
sed -i 's/<dbs>ON<\/dbs>/<dbs>OFF<\/dbs>/g' /etc/intel_manageability.conf
sed -i 's/<dbs>WARN<\/dbs>/<dbs>OFF<\/dbs>/g' /etc/intel_manageability.conf
grep dbs /etc/intel_manageability.conf | grep OFF
echo Confirmed dbs set to OFF in /etc/intel_manageability.conf.

NO_CLOUD=1 PROVISION_TPM=auto NO_OTA_CERT=1 TELIT_HOST="localhost" bash -x /usr/bin/provision-tc

if ! timeout 5 systemctl stop inbm
then
  echo Agents took too long to stop or failed to stop.
fi

if ! timeout 5 systemctl start inbm
then
  echo Agents took too long to start or failed to start.
fi

# give agents a few seconds to stabilize
sleep 15

# show last few lines of journal for context
journalctl -a --no-pager -n 50

# check for agents being up
ps -G dispatcher-agent | grep dispatcher
ps -G telemetry-agent | grep telemetry
ps -G configuration-agent | grep configur
ps -G diagnostic-agent | grep diagnos
ps -G mqtt-broker | grep mosquitto
