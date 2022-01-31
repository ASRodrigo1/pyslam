import numpy as np

def remove_objects(frame: np.ndarray, result: list, objects_indexes: list) -> np.ndarray:
    """
    Receives a list of object names to remove from a frame
    """
    
    width, height, _ = np.shape(frame)
    
    for i in range(width):
        for j in range(height):
            if result[0][i][j] not in objects_indexes:
                frame[i][j] = [0, 0, 0]
    
    return frame

def coords_to_remove(frame: np.ndarray, result: list, objects_indexes: list) -> list:
	"""
	Receives a mask and return coordinates where we should not have key points
	"""

	response = []

	width, height, _ = np.shape(frame)

	for i in range(width):
		for j in range(height):
			if result[0][i][j] in objects_indexes:
				response.append((i, j))

	return response