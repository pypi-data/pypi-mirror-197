import os
import re
import time
from termcolor import colored

def pyForense(directory):
    print(colored('Diagnosis being carried out...', 'green'))
    time.sleep(1)
    print(colored('Desired directory or file: ' + directory, 'red'))

    installed_libraries = os.popen('pip freeze').read()
    project_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                project_files.append(os.path.join(root, file))

    dependencies = set()
    for file in project_files:
        with open(file, 'r', encoding='iso-8859-1') as f:
            content = f.read()
            libraries = re.findall(r'import\s+(\w+)|from\s+(\w+)\s+import', content)
            for library in libraries:
                for lib in library:
                    if lib:
                        dependencies.add(lib)
        if len(dependencies) > 0:
            print('|-- ' + colored(file, 'green'))
            for lib in dependencies:
                if lib + '==' not in installed_libraries:
                    print('|   --- need to installr ' + colored(lib, 'red'))
                    print(colored('command: pip3 install ' + lib, 'cyan'))
                else:
                    print('|   --- ' + colored(lib + ' Already in your system.', 'green'))
        else:
            print('|-- ' + colored(file, 'green'))

