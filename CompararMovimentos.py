import cv2, time
import DetrectorPoses as pm
from scipy.spatial.distance import cosine
from fastdtw import fastdtw
 
def compare_posicao(ref_video, user_video):
	ref_cam = cv2.VideoCapture(ref_video)
	user_cam = cv2.VideoCapture(user_video) 

	fps_time = 0

	detector_1 = pm.DetectorPoses()
	detector_2 = pm.DetectorPoses()
	contador_frame = 0
	frame_atual = 0

	while (ref_cam.isOpened() or user_cam.isOpened()):
		try:
			ret_val, image_1 = user_cam.read()
			print(f"ret_val: {ret_val}")

			# Loop no vídeo se ele tiver terminado. Se o último quadro for alcançado, redefina a captura e o contador_frame
			if contador_frame == user_cam.get(cv2.CAP_PROP_FRAME_COUNT):
				contador_frame = 0 # ou o que quer que seja, desde que seja igual à próxima linha
				frame_atual = 0
				user_cam.set(cv2.CAP_PROP_POS_FRAMES, 0)

			winname = "User Video"
			cv2.namedWindow(winname)
			#cv2.moveWindow(winname, 720, -100) 
			image_1 = cv2.resize(image_1, (720,640))
			image_1 = detector_1.identificarPose(image_1)
			lmList_user = detector_1.identificarPosicao(image_1, draw=False)
			# del lmList_user[1:11]

			ret_val_1,image_2 = ref_cam.read()
			if contador_frame == ref_cam.get(cv2.CAP_PROP_FRAME_COUNT):
				contador_frame = 0
				frame_atual = 0
				ref_cam.set(cv2.CAP_PROP_POS_FRAMES, 0)

			image_2 = cv2.resize(image_2, (720,640))
			image_2 = detector_2.identificarPose(image_2)
			lmList_benchmark = detector_2.identificarPosicao(image_2, draw=False)

			contador_frame += 1


			if ret_val_1 or ret_val:
				error, _ = fastdtw(lmList_user, lmList_benchmark, dist=cosine)

				# Mostra o Erro de em %
				cv2.putText(image_1, 'Erro: {}%'.format(str(round(100*(float(error)),2))), (10, 30),
								cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

				# Se a similaridade for > 90%, tome-o como passo correto. Caso contrário, etapa incorreta.
				# Aqui da para mudar a % fazer um level facil e medio e pa 
				if error < 0.3:
					cv2.putText(image_1, "Correto ", (40, 600),
								cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
					frame_atual += 1
				else:
					cv2.putText(image_1,  "Incorreto ", (40, 600),
								cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
				cv2.putText(image_1, "FPS: %f" % (1.0 / (time.time() - fps_time)), (10, 50),
							cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

				# Exiba a precisão dinâmica do videro de ref como a % de quadros que aparecem como corretos
				if contador_frame==0:
					contador_frame = user_cam.get(cv2.CAP_PROP_FRAME_COUNT)
				cv2.putText(image_1, "Passos executados com precisão: {}%".format(str(round(100*frame_atual/contador_frame, 2))), (10, 70), 
							cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
				
				cv2.imshow('Ref Video', image_2)
				cv2.imshow('User Video', image_1)

				fps_time = time.time()
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break
			else:
				break
		except:
			pass

	ref_cam.release()
	user_cam.release()
	cv2.destroyAllWindows()

