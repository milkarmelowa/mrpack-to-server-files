import zipfile
import json
import os
import re
import shutil
def main():
    pack_chosen = choose_menu()
    # pack_chosen = 'VR Survival.mrpack' # for debugging
    result = make_lists(get_json_file(pack_chosen))
    for i in list(result.keys()):
        print(i)
    print('\n----------------------------------------\n')
    choose_method(result)

def choose_menu():
    mrpack_form = re.compile(".*\\.mrpack")
    dir_list = os.listdir('.')
    list_mrpack = list(filter(mrpack_form.match, dir_list))
    if list_mrpack==[]:
        print("No .mrpack files found, place the file in the same directory as the script")
    else:
        running = True
        while running:
            print("Detected files:")
            for i in range (len(list_mrpack)):
                print(str(i+1)+'.', list_mrpack[i])
            chosen = input('Choose pack number: ')
            while int(chosen) not in range(1, len(list_mrpack)+1):
                chosen = input('No such pack, enter new: ')
            pack_chosen = list_mrpack[int(chosen)-1]
            confirm = input('Chosen pack: ' + pack_chosen + ' [Y/n]')
            match confirm:
                case 'Y':
                    running = False
                    break
                case 'y':
                    running = False
                    break
                case '':
                    running = False
                    break
                case _:
                    running = True
                    print("cancelled\n")
    return pack_chosen

def get_json_file(pack_chosen):
    with zipfile.ZipFile(pack_chosen) as zip_file:
        with zip_file.open('modrinth.index.json') as json_file:
            file = json.load(json_file)
    return file

def make_lists(file):
    required_only_with_links = dict()
    n = 0
    for mod_file_json in file['files']:
        mod_file = mod_file_json['path']
        required_status = mod_file_json['env']['server']
        print(mod_file,end=' -- ')
        print(required_status)
        if required_status == 'required' or required_status =='optional':
            file_required = True
        else:
            file_required = False
        if file_required:
            required_only_with_links[mod_file] = file['files'][n]['downloads']
        n+=1
    return required_only_with_links

def choose_method(result):
    choice = ''
    while choice != '1' and choice != '2':
        choice = input('Make modlist locally [1]\nDownload modlist from Modrinth [2]\nSelection: ')
    if choice == '1':
        make_local(list(result.keys()))
        return None
    elif choice == '2':
        make_download(list(result.values()))
        return None
    return None

def make_local(modlist):
    non_exist_files=[] # list of missing files
    for filepath in modlist:
        if not os.path.isfile(filepath):
            non_exist_files.append(filepath)
    # If missing any files
    # TODO add partial download
    if len(non_exist_files) > 0:
        print('\nMissing files:')
        for i in non_exist_files:
            print(i)
        return None
    # No missing files
    os.makedirs('./server/mods')
    for filepath in modlist:
        shutil.copy(filepath, './server/mods')
    return None

def make_download(modlist):
    return None

if __name__ == '__main__':
    main()
