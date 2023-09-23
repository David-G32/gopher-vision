import sys
from pathlib import Path
import time
import gdat

if len(sys.argv) != 3:
    raise Exception('expected "python parse-gdat.py config.yaml path/to/data.gdat"')

# find GopherCAN config in sibling directory
config_name = sys.argv[1]
config_path = Path(f'../gophercan-lib/network_autogen/configs/{config_name}').resolve()

if not config_path.is_file():
    raise Exception(f'"{config_path}" does not exist')

ipath = Path(sys.argv[2])

if not ipath.is_file():
    raise Exception(f'"{ipath}" does not exist')

if ipath.suffix != '.gdat':
    raise Exception('expected a path to a .gdat file')

print(f'loading "{config_name}"...')
parameters = gdat.load_parameters(config_path)
print(f'loaded {len(parameters)} parameters\n')

print(f'opening "{ipath}"...')
(sof, ext, data) = ipath.read_bytes().partition(b'.gdat:')
print(f'read {len(data)} bytes of data')

t0 = gdat.get_t0(sof)
print(f"t0: {time.strftime('%m/%d/%Y %H:%M:%S', t0)}\n")

# randomized data
data = gdat.generate_data(parameters, 1000)

print('parsing packets...')
(packets, errors) = gdat.parse(data)
gdat.decode_data(packets, parameters)
print(f'parsed {len(packets)} valid packets, {errors} errors\n')

print('forming channels...')
channels = gdat.get_channels(packets, parameters)
print(f'created {len(channels)} channels\n')

for ch in channels.values():
    print(f"{ch['name']}: id={ch['id']} unit={ch['unit']} "
          f"type={len(ch['type'])} points={len(ch['points'])}")