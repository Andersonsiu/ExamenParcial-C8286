FROM ubuntu:20.04

# Evitar que se soliciten entradas de usuario durante la instalación de paquetes
ARG DEBIAN_FRONTEND=noninteractive

# Actualizar los paquetes e instalar Python 3 y pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Copiar los scripts del cliente, servidor y el script de inicio al contenedor
COPY pregunta2.py .

ENTRYPOINT ["python", "pregunta2.py"]
