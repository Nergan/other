from argostranslate.package import get_available_packages, get_installed_packages, update_package_index, install_from_path, uninstall
from argostranslate.translate import translate

from cmdloop import Loop
from findpath import findpath


global installed_packages, available_packages, packages_by_name, langs, from_selected, to_selected

installed_packages = get_installed_packages()
available_packages = get_available_packages()
packages_by_name = {(pkg.from_name, pkg.to_name): pkg for pkg in installed_packages}

unique_langs = set()
for pkg in installed_packages:
    unique_langs.add((pkg.from_code, pkg.from_name))
    unique_langs.add((pkg.to_code, pkg.to_name))
langs = [{'code': code, 'name': name} for code, name in unique_langs]
del unique_langs

from_selected, to_selected = None, None
for from_name, to_name in packages_by_name:
    if from_name == 'English' and to_name == 'Russian':
        from_selected = {'name': from_name, 'code': packages_by_name[from_name, to_name].from_code}
        to_selected = {'name': to_name, 'code': packages_by_name[from_name, to_name].to_code}
        break
    
paths_found = []
if from_selected and to_selected:
    paths_found.append(((from_selected['code'], to_selected['code'])))

help_msg = '''
/u /upd - update information of packages
/in /install <package 1> <package 2> ... <package n> - install packages
/un /uninstall <package 1> <package 2> ... <package n> - uninstall packages
/i /installed - show installed packages
/a /available - show available packages
/l /langs - shows available languages
/se /select <from code> <to code> - select languages (by code!)
/s /swap or ctrl + s - swap
/cls - clear console
'''
        

    
def upd():
    global available_packages
    
    try:
        update_package_index()
        available_packages = get_available_packages()
        print('package information updated')
    except:
        print('error: package information not updated')
    

def show_installed():
    print()
    for pkg in installed_packages:
        print(pkg)
    print()
    
    
def show_available():
    print()
    for pkg in available_packages:
        print(pkg)
    print()
    
    
def show_langs():    
    print()
    for lang in langs:
        print(f'{lang["code"]}\t{lang["name"]}')
    print()
    
    
def install(*pkg_names):
    global installed_packages, packages_by_name, langs
    
    if pkg_names:
        if len(pkg_names) % 3 != 0:
            print('error: you entered something wrong')
            return
        
        counter = 0
        new_pkg_names = []
        tmp = ''
        for arg in pkg_names:
            tmp += arg + ' '
            counter += 1
            if counter == 3:
               counter = 0
               new_pkg_names.append(tmp.strip())
               tmp = ''
        pkg_names = new_pkg_names
        
        for pkg_name in pkg_names:
            if pkg_name in map(str, available_packages):
                from_name, to_name = pkg_name.replace('→', '').split()
                try:
                    install_from_path(packages_by_name[from_name, to_name]).download()
                    installed_packages = get_installed_packages()
                    packages_by_name = {(pkg.from_name, pkg.to_name): pkg for pkg in installed_packages}
                    langs = set(name for key in packages_by_name for name in key)
                    print('package installed')
                except:
                    print('error: failed to install package')
            else:
                print('error: package not found')
    else:
        print('error: you have not specified any packages')
            
            
def this_uninstall(*pkg_names):    
    global installed_packages, packages_by_name, langs
    
    if pkg_names:
        if len(pkg_names) % 3 != 0:
            print('error: you entered something wrong')
            return
        
        counter = 0
        new_pkg_names = []
        tmp = ''
        for arg in pkg_names:
            tmp += arg + ' '
            counter += 1
            if counter == 3:
               counter = 0
               new_pkg_names.append(tmp.strip())
               tmp = ''
        pkg_names = new_pkg_names
        
        for pkg_name in pkg_names:
            if pkg_name in map(str, installed_packages):
                from_name, to_name = pkg_name.replace('→', '').split()
                try:
                    uninstall(packages_by_name[from_name, to_name])
                    installed_packages = get_installed_packages()
                    packages_by_name = {(pkg.from_name, pkg.to_name): pkg for pkg in installed_packages}
                    langs = set(name for key in packages_by_name for name in key)
                    print('package uninstalled')
                except:
                    print('error: failed to uninstall package')
            else:
                print('error: package not found')
    else:
        print('error: you have not specified any packages')
        
        
def select(from_code, to_code):
    codes = {lang['code'] for lang in langs}
    if from_code not in codes or to_code not in codes:
        print('error: language not found')
        return
    
    global from_selected, to_selected

    for lang in langs:
        if from_code == lang['code']:
            from_code = {'name': lang['name'], 'code': from_code}
        if to_code == lang['code']:
            to_code = {'name': lang['name'], 'code': to_code}
        if isinstance(from_code, dict) and isinstance(to_code, dict):
            break
            
    from_selected = from_code
    to_selected = to_code
            
            
def swap():
    global from_selected, to_selected
    from_selected, to_selected = to_selected, from_selected


def smart_translate(txt, frm, to):    
    if not (frm and to):
        print('error: languages ​​not selected')
        return
    
    tmp_codes = {lang['code'] for lang in langs}
    if frm not in tmp_codes and to not in tmp_codes:
        print('error: languages ​​not found')
        return
    
    counter = 0
    for path in paths_found:
        if not (path[0][0] == frm and to == path[-1][-1]):
            counter += 1
    if counter == len(paths_found):
              
        graph = {}
        for from_lang in langs:
            line = {}
            for to_lang in langs:
                line[to_lang['code']] = 0
                for pkg in installed_packages:
                    if pkg.from_code == from_lang['code'] and pkg.to_code == to_lang['code']:
                        line[to_lang['code']] = 1
                        break
            graph[from_lang['code']] = line
        
        path = findpath(frm, to, graph)
        paths_found.append(path)

        if not path:
            print('error: unable to build chain of packages for translation')
            return
        
    for from_code, to_code in path:
        txt = translate(txt, from_code, to_code)
        
    return txt


def cmd_translate(txt):
    return smart_translate(txt, from_selected['code'], to_selected['code'])


def get_placeholder():
    return f'{from_selected["name"].lower()} > {to_selected["name"].lower()}: ' if from_selected and to_selected else 'lang not selected: '
        

if __name__ == '__main__':
    loop = Loop()
    loop.add_cmd(('upd', 'u'), upd)
    loop.add_cmd(('install', 'in'), install)
    loop.add_cmd(('uninstall', 'un'), this_uninstall)
    loop.add_cmd(('installed', 'i'), show_installed)
    loop.add_cmd(('available', 'a'), show_available)
    loop.add_cmd(('langs', 'l'), show_langs)
    loop.add_cmd(('select', 'se'), select)
    loop.add_cmd(('swap', 's'), swap)
    loop.default = cmd_translate
    loop.help = help_msg
    loop.placeholder = get_placeholder
    loop.run()