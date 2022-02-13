from displayer import Displayer
import pyzed.sl as sl
import keyboard as key
import numpy as np
import cv2

#disp = Displayer(1280, 720)

# Parâmetros iniciais
init_params = sl.InitParameters()
init_params.camera_resolution = sl.RESOLUTION.HD720
init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP
init_params.coordinate_units = sl.UNIT.METER

#########################################################################

# Abre a câmera
zed = sl.Camera()
err = zed.open(init_params)
if err != sl.ERROR_CODE.SUCCESS:
	print("Erro ao abrir a câmera. Verifique os parâmetros!")
	exit(-1)
#########################################################################

# Configura rastreamento de posição
tracking_parameters = sl.PositionalTrackingParameters()
err = zed.enable_positional_tracking(tracking_parameters)
if err != sl.ERROR_CODE.SUCCESS:
	print("Erro ao iniciar o rastreamento. Verifique os parâmetros!")
	exit(-1)
else:
	print("Rastreamento de posição iniciado!")
#########################################################################

# Configura o mapeamento espacial
mapping_parameters = sl.SpatialMappingParameters()
mapping_parameters.resolution_meter = 0.02 # 3 centímetros
mapping_parameters.range_meter = 10 # 10 metros
mapping_parameters.map_type = sl.SPATIAL_MAP_TYPE.FUSED_POINT_CLOUD
err = zed.enable_spatial_mapping(mapping_parameters)
if err != sl.ERROR_CODE.SUCCESS:
	print("Erro ao iniciar o mapeamento. Verifique os parâmetros!")
	exit(-1)
else:
	print("Mapeamento iniciado!")
#########################################################################

# Realizamos o processo
points = sl.FusedPointCloud()
pose = sl.Pose()
poses_hist = []
runtime_parameters = sl.RuntimeParameters()

while True:

	if key.is_pressed("Q"):
		break

	if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
		# Coleta informações
		zed.get_position(pose, sl.REFERENCE_FRAME.WORLD)

		# Calcula os parâmetros de posicionamento
		py_translation = sl.Translation()
		tx = round(pose.get_translation(py_translation).get()[0], 3)
		ty = round(pose.get_translation(py_translation).get()[1], 3)
		tz = round(pose.get_translation(py_translation).get()[2], 3)
		py_orientation = sl.Orientation()
		ox = round(pose.get_orientation(py_orientation).get()[0], 3)
		oy = round(pose.get_orientation(py_orientation).get()[1], 3)
		oz = round(pose.get_orientation(py_orientation).get()[2], 3)
		ow = round(pose.get_orientation(py_orientation).get()[3], 3)
		
		poses_hist.append([pose.timestamp.get_milliseconds(), tx, ty, tz, ox, oy, oz, ow])

	else:
		print("Erro durante medições! Terminando programa...")
		break
#########################################################################

# Extraímos o mapa e o salvamos, juntamente com as poses
zed.extract_whole_spatial_map(points)
points.save("points.obj")
np.save("poses", np.array(poses_hist))
#########################################################################

# Desliga as funções iniciadas e fecha a câmera
zed.disable_positional_tracking()
zed.disable_spatial_mapping()
zed.close()
cv2.destroyAllWindows()
#########################################################################