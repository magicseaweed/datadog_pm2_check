# Datadog [PM2][pm2] check
A check for [pm2][pm2] processes for DataDog

### Installation

  - Copy `/checks.d/pm2.py` to `/etc/dd-agent/checks.d/pm2.py` and `conf.d/pm2.yaml` to `/etc/dd-agent/conf.d/pm2.yaml`.
  - Then restart Datadog agent:  `/etc/init.d/datadog-agent restart`

[pm2]: <http://pm2.keymetrics.io/>
