[app]

# (str) Title of your application
title = Calculadora de Abono

# (str) Package name
package.name = calculadoraabono

# (str) Package domain (needed for android/ios packaging)
package.domain = org.agricultor.calculadoraabono

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (portrait, sensorPortrait, landscape, sensorLandscape)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Presplash background color (for new android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
#presplash.color = #FFFFFF

# (str) Presplash animation using Lottie format.
# see https://lottie.github.io/lottie-spec/
# Put the lottie file in source.dir and add the filename here.
#presplash.lottie = ""

# (str) Adaptive icon of the application
