import os
import subprocess


def trans_3dm_2_json(surface_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = 'Trans3dm2json'
    directory = os.path.join(script_dir, relative_path)
    executable_path = os.path.join(directory, 'on2json.exe')
    sat_name = surface_name + '.3dm'

    command = [executable_path, sat_name]
    print('executable_path:', executable_path)
    print('command:', command)

    subprocess.run(command, cwd=directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


if __name__ == '__main__':
    trans_3dm_2_json('grid')

