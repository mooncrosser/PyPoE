#!/usr/bin/env sh
pip install --user -U pip setuptools
pip install --user -U -r test_requirements.txt
pip install --user -U -e .[full]
pypoe_exporter config set out_dir ./out
mkdir /tmp/pypoe-temp
pypoe_exporter config set temp_dir /tmp/pypoe-temp
pypoe_exporter config set ggpk_path /poe
pypoe_exporter setup perform