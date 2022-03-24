import subprocess

command = r'D:/R-4.0.2/bin/Rscript'
arg = '--vanilla'
path2script = r'C:/Users/ChuaShiXian/Desktop/Bachelor of Computer Science (Information Systems)/2020-21/Semester 2 2020-21/Academic Project/Development/Eunice/app.R'

subprocess.call([command, arg, path2script], shell=True)
