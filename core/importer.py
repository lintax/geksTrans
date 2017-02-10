import os, fnmatch


def load_files_tree(folder, mask):
    result = []
    for path, dirs, files in os.walk(folder):
        for f in files:
            if fnmatch.fnmatch(f, mask):
                result.append(path + os.sep + f)
    return result


def load_yml_my(path, result):
    print(" loading custom {}".format(path))
    with open(path) as stream:
        for line in stream.read().splitlines():
            if ':' in line:
                # some_key_alpha_numeric:[number] "text included"
                key, right = line.strip().split(':', 1)
                if len(right) > 2:
                    _, value = right.split(' ', 1)
                    value = value.replace('"', '')
                    # print("  {} = {}".format(key, value))
                    result[key] = value


def import_tree(folder, mask):
    result = {}
    print("Loading " + mask + " from " + folder)
    files = load_files_tree(folder, mask)
    print("Matched files {}".format(files))
    for f in files:
        load_yml_my(f, result)
    print("{} phrases loaded".format(len(result)))
    return result
