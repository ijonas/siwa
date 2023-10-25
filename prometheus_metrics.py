from prometheus_client import (
    CollectorRegistry,
    Gauge,
)

csgo_index_gauge = Gauge('csgo_index', 'CSGO Skins Index')

registry = CollectorRegistry()
registry.register(csgo_index_gauge)
