#from mutagen.mp3 import MP3

def getMs(pos,bpm_array_pos,bpm_array_val,resolution,arredondar = False):
    cur_ms = 0
    for i, value in enumerate(bpm_array_pos):
        bpm = bpm_array_val[i] / 1000
        if (i < len(bpm_array_pos)-1 and pos >= bpm_array_pos[i+1]): # note on later bpm
            cur_ms += (((bpm_array_pos[i+1]-bpm_array_pos[i]) / resolution) / bpm * 60)
        else:
            cur_ms += (((pos-bpm_array_pos[i]) / resolution) / bpm * 60)
            if (arredondar): cur_ms = round(cur_ms * 24) / 24 # round to 24 bps
            return cur_ms

print("Arraste o arquivo .chart para esta janela e aperte Enter:")
file_input = input()
if file_input.startswith("\""): file_input = file_input[1:-1]
file1 = open(file_input, 'r', encoding='utf-8')
#print("Arraste o arquivo .mp3 para esta janela e aperte Enter:")
#mp3_input = input()
#if mp3_input.startswith("\""): mp3_input = mp3_input[1:-1]
#audio = MP3(mp3_input)
arredondar = False
print("Você gostaria de arredondar a chart pra 24 bps? (s/N):")
if (input().lower().strip().startswith("s")): arredondar = True
chart = "ExpertSingle"
print("Qual dificuldade/instrumento da chart gostaria de converter? (Deixe vazio para ExpertSingle):")
chart_input = input()
if (chart_input.strip() != ""): chart = chart_input
Lines = file1.readlines()
file1.close()
sections = {}
section_name = ""
bpm_array_pos = []
bpm_array_val = []
star_power = {}
# read chart
for line in Lines:
    if line.startswith('[') or line.startswith('\ufeff['):
        section_name = line[1:-2]
        if line.startswith('\ufeff['): section_name = line[2:-2]
    if '=' in line:
        split = line.split('=')
        if section_name not in sections and section_name != "SyncTrack": sections[section_name] = {}
        split_key = split[0].strip()
        split_value = split[1].strip()
        if section_name == "Song":
            if split_value.startswith("\""): split_value = split_value[1:-1]
            sections[section_name][split_key] = split_value
        elif section_name == "SyncTrack":
            if "TS" not in split_value: # ignore time sig
                #sections[section_name][split_key] = split_value[2:].strip()
                bpm_array_pos.append(int(split_key))
                bpm_array_val.append(int(split_value[2:].strip()))
        elif section_name == chart: # ignore sections; these should be tracks
            # TODO: parse SP, ignore taps, convert opens to greens
            if split_key not in sections[section_name]: sections[section_name][split_key] = []
            sections[section_name][split_key].append(split_value)
            if (split_value.startswith("S 2")):
                sp_split = split_value.split(' ')
                star_power[split_key] = sp_split[2]
# start writing sng

offset = float(sections["Song"]["Offset"])
resolution = int(sections["Song"]["Resolution"])
diff = "EXPERT"
if ("Hard" in chart): diff = "HARD"
elif ("Medium" in chart): diff = "MEDIUM"
elif ("Easy" in chart): diff = "EASY"
length = list(sections[chart].keys())[-1]
last_note_dur = 0
for dur in sections[chart][length]:
    if (not dur.startswith("N 5") and not dur.startswith("N 6")):
        end_tick = int(length)
        if (dur.startswith("N")): end_tick = int(length) + (int(dur.split(' ')[2]))
        pos = round(getMs(int(end_tick),bpm_array_pos,bpm_array_val,resolution,arredondar) + offset + 3, 3)
        if pos > last_note_dur: last_note_dur = pos
length = last_note_dur

bps = "24.0"

out = """<?xml version="1.0"?>
<Song>
    <Properties>
        <Version>0.1</Version>
        <Title>""" + sections["Song"]["Name"] + """</Title>
        <Artist>""" + sections["Song"]["Artist"] + """</Artist>
        <Album>No Album Set</Album>
        <Year>0</Year>
        <BeatsPerSecond>""" + bps + """</BeatsPerSecond>
        <BeatOffset>0.0</BeatOffset>
        <HammerOnTime>0.25</HammerOnTime>
        <PullOffTime>0.25</PullOffTime>
        <Difficulty>""" + diff + """</Difficulty>
        <AllowableErrorTime>0.05</AllowableErrorTime>
        <Length>""" + str(length) + """</Length>
        <MusicFileName>""" + sections["Song"]["MusicStream"] + """</MusicFileName>
        <MusicDirectoryHint>./</MusicDirectoryHint>
    </Properties>

    <Data>
"""

# note data
for key, value in sections[chart].items():
    for note_str in value:
        if (note_str.startswith("N") and not note_str.startswith("N 5") and not note_str.startswith("N 6")):
            split = note_str.split(' ')
            note = split[1]
            if note == '7':
                note = '0'
                print("open note at tick " + key + "; converting to green")
            start_tick = int(key)
            end_tick = start_tick + (int(split[2]))
            pos = getMs(start_tick,bpm_array_pos,bpm_array_val,resolution,arredondar)
            duration = getMs(end_tick,bpm_array_pos,bpm_array_val,resolution,arredondar) - pos
            if duration < 0.25: duration = 0.0 # reduzir sustain menor q 6 frames
            # star power
            special = 0
            for key2, value2 in star_power.items():
                sp_start_tick = int(key2)
                if sp_start_tick > start_tick: continue
                if start_tick >= sp_start_tick and start_tick < sp_start_tick + int(value2): special = 1
            out += "        <Note time=\"" + str(round(pos + offset, 6)) + "\" duration=\"" + str(round(duration, 6)) + "\" track=\"" + note + "\" special=\"" + str(special) + "\" />\n"

# sng end
out += """    </Data>
</Song>"""
out_path = file_input + '.' + chart + '.sng'
text_file = open(out_path, "w", encoding='utf-8')
n = text_file.write(out)
text_file.close()
print("Salvo em " + out_path + "; aperte Enter para sair!")
input()
