import pickle
import os
import sys
from progress.bar import Bar
from processor import encode_midi


def preprocess_midi(path):
    return encode_midi(path)


def preprocess_midi_files_under(midi_root, save_dir):
    midi_paths = list(find_files_by_extensions(midi_root, ['.mid', '.midi']))
    os.makedirs(save_dir, exist_ok=True)
    out_fmt = '{}-{}.data'

    stats = open("stats.txt", 'w')
    notal = 0
    sectotal = 0
    etotal = 0
    maxnote = maxe = 0
    minote = mine = 999999
    npieces = len(midi_paths)
    stats.write("File Name;Number of Events;Number of Notes;Estimated Duration\n")

    for path in Bar('Processing').iter(midi_paths):
        print(' \n', end='[{}]'.format(path.split('\\')[-1]), flush=True)

        try:
            data = preprocess_midi(path)
        except KeyboardInterrupt:
            print(' Abort')
            return
        except EOFError:
            print('EOF Error')
            return

        with open('{}/{}.pickle'.format(save_dir, path.split('//')[-1]), 'wb') as f:
            pickle.dump(data, f)

        notes = sum([e<128 for e in data])
        duration = sum([(e-255)*(e in range(256,356)) for e in data])/100
        
        stats.write(path.split('//')[-1] + ";" + str(len(data)) + ";" + str(notes) + ";" + sec2min(duration) + "\n")

        notal += notes
        etotal += len(data)
        sectotal += duration

        if notes<minote:
            minote=notes
        elif notes>maxnote:
            maxnote=notes

        if len(data)<mine:
            mine=len(data)
        elif len(data)>maxe:
            maxe=len(data)
        
    stats.write("\nNumber of Pieces;" + str(npieces) + "\n")
    stats.write("Total Events;"+ str(etotal) + "\n")
    stats.write("Max Events;"+ str(maxe) + "\n")
    stats.write("Min Events;"+ str(mine) + "\n")
    stats.write("Average Events;{:.2f}\n".format(etotal/npieces))
    stats.write("Total Notes;"+ str(notal) + "\n")
    stats.write("Max Notes;"+ str(maxnote) + "\n")
    stats.write("Min Notes;"+ str(minote) + "\n")
    stats.write("Average Notes;{:.2f}\n".format(notal/npieces)) 
    stats.write("Average Duration;" + sec2min(sectotal/npieces))
    stats.close()

def find_files_by_extensions(root, exts=[]):
    def _has_ext(name):
        if not exts:
            return True
        name = name.lower()
        for ext in exts:
            if name.endswith(ext):
                return True
        return False
    for path, _, files in os.walk(root):
        for name in files:
            if _has_ext(name):
                yield os.path.join(path, name)

def sec2min(val):
    val = round(val)
    m = int(val/60)
    s = val - m*60

    return ("{:02d}:{:02d}".format(m,s))

if __name__ == '__main__':
    preprocess_midi_files_under("dataset","processed_data")
