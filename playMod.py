import pyaudio
import wave
import os.path
import threading

def play(audio,stop_event):
        if not audio:
            print("there is no audio file")
        else:
            if os.path.isfile(audio):
                p = pyaudio.PyAudio()
                FORMAT = pyaudio.paInt16
                CHANNELS = 2
                RATE = 44100
                canal = -1
                for i in range(p.get_device_count()):
                    info = p.get_device_info_by_index(i)
                    if('CABLE Input (VB-Audio Virtual' in info['name']):
                        canal=i
                        break

                wf = wave.open(audio, 'rb')

                # Abrir un flujo de audio para reproducción
                stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                                channels=wf.getnchannels(),
                                rate=wf.getframerate(),
                                output=True,
                                output_device_index=canal) # checar luego

                # Leer datos de audio del archivo
                data = wf.readframes(1024)

                # Reproducir audio mientras haya datos en el archivo
                try:
                    while data:
                        stream.write(data)
                        data = wf.readframes(1024)
                        # print(stop)
                        if stop_event.is_set():
                            break
                except KeyboardInterrupt:
                    print("Captura de audio detenida.")
                stream.stop_stream()
                stream.close()
                p.terminate()
            else:
                print("name invalid")