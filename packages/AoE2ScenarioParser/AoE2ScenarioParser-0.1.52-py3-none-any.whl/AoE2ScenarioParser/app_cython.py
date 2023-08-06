import time

from AoE2ScenarioParser.local_config import folder_de
from AoE2ScenarioParser.scenarios.aoe2_scenario import AoE2Scenario

start = time.time()

filename = "CBA_Hero_v1_my"
scenario = AoE2Scenario.from_file(f"{folder_de}{filename}.aoe2scenario")
tm, um, mm, xm, pm, msm = scenario.trigger_manager, scenario.unit_manager, scenario.map_manager, scenario.xs_manager, \
    scenario.player_manager, scenario.message_manager

# print(tm.get_summary_as_string())
print(time.time() - start)

scenario.write_to_file(f"{folder_de}{filename}_written.aoe2scenario")

# No Cython:
#   ~11.6s
# Cython (Compiled: File Section - No Further Changes):
#   ~11s
# Cython (Compiled: +Struct Model - No Further Changes):
#   ~10.8s
# Cython (Compiled: +Retriever - No Further Changes):
#   ~9.7s
# Cython (Compiled: +RetrieverObjectLink - No Further Changes):
#   ~9.3s
# Cython (Compiled: +RetrieverObjectLinkGroup +RetrieverObjectLinkParent - No Further Changes):
#   ~9.1s
# Cython (Compiled: EVERYTHING - No Further Changes):
#   ~7.4s
# Cythonized incremental_generator.pyx
#   ~...s
