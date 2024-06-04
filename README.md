# Установка и запуск игры

## Шаги по установке

1. Убедитесь, что у вас установлен Anaconda и Python.
2. Скачайте и распакуйте архив с игрой.
3. Откройте Anaconda Prompt и перейдите в директорию с игрой.
4. Создайте новое окружение и установите библиотеки:

   ```bash
   conda create --name Pentomis_env python=3.8
   conda activate Pentomis_env
   pip install -r requirements.txt
5. Перейдите в поддиректорию src

   ```bash
   cd src
## Запуск игры
1. Запустите игру командой

   ```bash
   python main.py
