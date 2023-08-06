######################################
#  DEFAULT es7s configuration file   #
#  DO NOT EDIT                       #
#  Run 'es7s config edit' to set up  #
######################################

[general]
syntax-version = 2.0
theme-color = blue

[provider]
battery = on
cpu = on
disk = on
datetime = on
docker = on
fan = on
memory = on
network-country = on
network-latency = on
temperature = on
timestamp = on
weather = on

[provider.network-latency]
host = 1.1.1.1
port = 53

[provider.timestamp]
url = https://dlup.link/temp/nalog.mtime

[provider.weather]
location = MSK

[monitor]
debug = off
force-cache = off

[monitor.combined]
layout1 =
    es7s.cli.monitor_combined.SPACE
    es7s.cli.monitor_disk_usage.DiskUsageMonitor
    es7s.cli.monitor_memory.MemoryMonitor
    es7s.cli.monitor_cpu_load.CpuLoadMonitor

    es7s.cli.monitor_combined.EDGE_LEFT
    es7s.cli.monitor_combined.SPACE
    es7s.cli.monitor_temperature.TemperatureMonitor
    es7s.cli.monitor_combined.SPACE
    es7s.cli.monitor_docker.DockerMonitor

    es7s.cli.monitor_combined.SPACE
    es7s.cli.monitor_network_latency.NetworkLatencyMonitor
    es7s.cli.monitor_combined.SPACE
    es7s.cli.monitor_network_country.NetworkCountryMonitor
    es7s.cli.monitor_combined.SPACE
    es7s.cli.monitor_timestamp.TimestampMonitor
    es7s.cli.monitor_combined.SPACE
    es7s.cli.monitor_weather.WeatherMonitor

    es7s.cli.monitor_combined.SPACE_2
    es7s.cli.monitor_datetime.DatetimeMonitor
    es7s.cli.monitor_combined.SPACE_2
    es7s.cli.monitor_battery.BatteryMonitor

layout2 =
    es7s.cli.monitor_combined.EDGE_LEFT
    es7s.cli.monitor_cpu_freq.CpuFreqMonitor
    es7s.cli.monitor_combined.SPACE_2
    es7s.cli.monitor_cpu_load_avg.CpuLoadAvgMonitor
    es7s.cli.monitor_combined.SPACE
    es7s.cli.monitor_fan_speed.FanSpeedMonitor

[monitor.datetime]
display-year = off
display-seconds = off

[monitor.memory]
swap-warn-threshold = 0.7

[monitor.weather]
weather-icon-set-id = 0
weather-icon-max-width = 2
wind-speed-warn-threshold = 10.0
