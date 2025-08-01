#!/bin/bash
echo "🚀 Configurando entorno para app móvil..."

# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias del sistema
sudo apt install -y python3-pip python3-dev build-essential
sudo apt install -y git zip unzip libffi-dev libssl-dev
sudo apt install -y openjdk-11-jdk

# Configurar Java
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.bashrc

# Instalar dependencias Python
pip3 install --upgrade pip
pip3 install kivy buildozer cython

echo "✅ Instalación completada!"
echo "Ahora puedes ejecutar: buildozer android debug"
