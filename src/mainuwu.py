from utils.custom_ini_parse import *

try:

    configIni = EngineIniParser(filename="Engine.ini")
    print(configIni.read_and_ignore_paths())
    configIni.add_section("/Script/Engine.RendererRTXSettings")
    configIni.add_key_value("/Script/Engine.RendererRTXSettings", "owo", "uwu")
    configIni.compile()

except Exception as e:
    print(e)

    # [ / Script / Engine.RendererRTXSettings]
    # r.raytracing = 1
    # r.raytracing.limitdevice = 0
    # r.raytracing.enableingame = 1
    # r.raytracing.enableondemand = 1
    # r.raytracing.enableineditor = 1
