#-------------------------------------------------------------------------------
#
# IDAPython script to show many features extracted from debugging strings. It's
# also able to rename functions based on the guessed function name & rename
# functions based on the source code file they belong to.
#
# Copyright (c) 2018-2022, Joxean Koret
# Licensed under the GNU Affero General Public License v3.
#
#-------------------------------------------------------------------------------

import os
import sys
import re
import r2pipe
import logging

from collections import Counter

import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

import ida2r2
import ida2r2.idc as idc
import ida2r2.idautils as idautils
import ida2r2.idaapi as idaapi

LOG_FORMAT = "%(asctime)-15s [%(levelname)s] - %(message)s"
log = logging.getLogger("r2magicstrings")
c_handler = logging.StreamHandler()
formatter = logging.Formatter(LOG_FORMAT)
c_handler.setFormatter(formatter)
log.addHandler(c_handler)
log.setLevel(logging.WARN)

#-------------------------------------------------------------------------------
PROGRAM_NAME = "IMS"

#-------------------------------------------------------------------------------
SOURCE_FILES_REGEXP = r"([a-z_\/\\][a-z0-9_/\\:\-\.@]+\.(c|cc|cxx|c\+\+|cpp|h|hpp|m|rs|go|ml))($|:| )"

LANGS = {}
LANGS["C/C++"] = ["c", "cc", "cxx", "cpp", "h", "hpp"]
LANGS["C"] = ["c"]
LANGS["C++"] = ["cc", "cxx", "cpp", "hpp", "c++"]
LANGS["Obj-C"] = ["m"]
LANGS["Rust"] = ["rs"]
LANGS["Golang"] = ["go"]
LANGS["OCaml"] = ["ml"]

#-------------------------------------------------------------------------------
FUNCTION_NAMES_REGEXP = r"([a-z_][a-z0-9_]+((::)+[a-z_][a-z0-9_]+)*)"
CLASS_NAMES_REGEXP    = r"([a-z_][a-z0-9_]+(::(<[a-z0-9_]+>|~{0,1}[a-z0-9_]+))+)\({0,1}"
NOT_FUNCTION_NAMES = ["copyright", "char", "bool", "int", "unsigned", "long",
    "double", "float", "signed", "license", "version", "cannot", "error",
    "invalid", "null", "warning", "general", "argument", "written", "report",
    "failed", "assert", "object", "integer", "unknown", "localhost", "native",
    "memory", "system", "write", "read", "open", "close", "help", "exit", "test",
    "return", "libs", "home", "ambiguous", "internal", "request", "inserting",
    "deleting", "removing", "updating", "adding", "assertion", "flags",
    "overflow", "enabled", "disabled", "enable", "disable", "virtual", "client",
    "server", "switch", "while", "offset", "abort", "panic", "static", "updated",
    "pointer", "reason", "month", "year", "week", "hour", "minute", "second",
    'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
    'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
    'september', 'october', 'november', 'december', "arguments", "corrupt",
    "corrupted", "default", "success", "expecting", "missing", "phrase",
    "unrecognized", "undefined",
]

#-------------------------------------------------------------------------------
FOUND_TOKENS = {}
TOKEN_TYPES = ["NN", "NNS", "NNP", "JJ", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
def nltk_preprocess(strings):
    strings = "\n".join(map(str, list(strings)))
    tokens = re.findall(FUNCTION_NAMES_REGEXP, strings)
    l = []
    for token in tokens:
        l.append(token[0])
    word_tags = nltk.pos_tag(l)
    for word, tag in word_tags:
        try:
            FOUND_TOKENS[word.lower()].add(tag)
        except:
            FOUND_TOKENS[word.lower()] = set([tag])

#-------------------------------------------------------------------------------
def get_strings(strtypes = [0, 1]):
    strings = idautils.Strings()
    #strings.setup(strtypes = strtypes)
    return strings

#-------------------------------------------------------------------------------
def get_lang(full_path):
    _, file_ext = os.path.splitext(full_path.lower())
    file_ext    = file_ext.strip(".")
    for key in LANGS:
        if file_ext in LANGS[key]:
            return key
    return None

#-------------------------------------------------------------------------------
def add_source_file_to(d, src_langs, refs, full_path, s):
    if full_path not in d:
        d[full_path] = []

    lang = get_lang(full_path)
    if lang is not None:
        src_langs[lang] += 1

    for ref in refs:
        d[full_path].append([ref, idc.get_func_name(ref), str(s)])

    return d, src_langs

#-------------------------------------------------------------------------------
def get_source_strings(min_len = 4, strtypes = [0, 1]):
    strings = get_strings(strtypes)

    # Search string references to source files
    src_langs = Counter()
    total_files = 0
    d = {}
    for _str in strings:
        if _str and _str.length > min_len:
            ret = re.findall(SOURCE_FILES_REGEXP, str(_str), re.IGNORECASE)
            if ret and len(ret) > 0:
                log.debug("Found string referencing source code: %s", str(_str))
                refs = idautils.DataRefsTo(_str.ea)
                if len(refs) > 0:
                    total_files += 1
                    full_path    = ret[0][0]
                    log.debug("Found source file %s in %s", full_path, str(_str))
                    d, src_langs = add_source_file_to(
                        d, src_langs, refs, full_path, _str
                    )

    # Use the loaded debugging information (if any) to find source files
    for source in ida2r2.r2.log_exec_r2_cmdj("CLj"):
        log.debug("Adding source code from debug info: %s", source["file"])
        d, src_langs = add_source_file_to(
            d, src_langs, [source["addr"]], source["file"],
            "Symbol: %s" % source["file"]
        )

    nltk_preprocess(strings)
    return d, strings

#-------------------------------------------------------------------------------
def basename(path):
    pos1 = path[::-1].find("\\")
    pos2 = path[::-1].find("/")

    if pos1 == -1: pos1 = len(path)
    if pos2 == -1: pos2 = len(path)
    pos = min(pos1, pos2)

    return path[len(path)-pos:]

#-------------------------------------------------------------------------------
def get_string(ea):
    tmp = idc.get_strlit_contents(ea, strtype=0)
    if tmp is None or len(tmp) == 1:
        unicode_tmp = idc.get_strlit_contents(ea, strtype=1)
        if unicode_tmp is not None and len(unicode_tmp) > len(tmp):
            tmp = unicode_tmp

    if tmp is None:
        tmp = ""
    elif type(tmp) != str:
        tmp = tmp.decode("utf-8")
    return tmp

#-------------------------------------------------------------------------------
def seems_function_name(candidate):
    if len(candidate) >= 6 and candidate.lower() not in NOT_FUNCTION_NAMES:
        if candidate.upper() != candidate:
            return True
    return False

#-------------------------------------------------------------------------------
class CFakeString:
    def __init__(self, ea, s):
        self.ea = ea
        self.s = s

    def __str__(self):
        return str(self.s)

    def __repr__(self):
        return self.__str__()

#-------------------------------------------------------------------------------
def find_function_names(strings_list):
    rarity = {}
    func_names = {}
    raw_func_strings = {}
    class_objects = []

    class_tmp_names = []
    for ea in idautils.Functions():
        name = idc.get_func_name(ea)
        true_name = name
        if name.find("::") == -1:
            name = idc.demangle_name(name, idc.INF_SHORT_DN)
            if name is not None and name != "" and name.find("::") > -1:
                true_name = name

        if true_name.find("::") > -1:
            s = CFakeString(ea, true_name)
            class_tmp_names.append(s)

    class_tmp_names.extend(strings_list)
    for s in class_tmp_names:
        # Find class members
        class_ret = re.findall(CLASS_NAMES_REGEXP, str(s), re.IGNORECASE)
        if len(class_ret) > 0:
            for element in class_ret:
                candidate = element[0]
                if candidate.find("::") > 0:
                    tokens = candidate.split("::")
                    if tokens not in class_objects:
                        class_objects.append([s.ea, tokens])

        # Find just function names
        ret = re.findall(FUNCTION_NAMES_REGEXP, str(s), re.IGNORECASE)
        if len(ret) > 0:
            candidate = ret[0][0]
            if seems_function_name(candidate):
                log.debug("%s seems like a function name", candidate)
                ea = s.ea
                refs = idautils.DataRefsTo(ea)
                found = False
                for ref in refs:
                    func = idaapi.get_func(ref)
                    if func is not None:
                        found = True
                        key = func.start_ea

                        log.info("Candidate %s referenced by function %s", candidate, func.name)
                        if candidate not in FOUND_TOKENS:
                            continue

                        found = False
                        for tkn_type in TOKEN_TYPES:
                            if tkn_type in FOUND_TOKENS[candidate]:
                                found = True
                                break

                        if not found:
                            continue

                        try:
                            rarity[candidate].add(key)
                        except KeyError:
                            rarity[candidate] = set([key])

                        try:
                            func_names[key].add(candidate)
                        except KeyError:
                            func_names[key] = set([candidate])

                        try:
                            raw_func_strings[key].add(str(s))
                        except:
                            raw_func_strings[key] = set([str(s)])

    return func_names, raw_func_strings, rarity, class_objects


def show_function_names(strings_list):
    func_names, raw_func_strings, rarity, classes = find_function_names(strings_list)
    final_list = []
    for key in func_names:
        candidates = set()
        for candidate in func_names[key]:
            if len(rarity[candidate]) == 1:
                candidates.add(candidate)

        if len(candidates) == 1:
            raw_strings = list(raw_func_strings[key])
            raw_strings = list(map(repr, raw_strings))

            func_name = idc.get_func_name(key)

            tmp_func_name = idc.demangle_name(func_name, 0)
            if tmp_func_name is not None:
                func_name = tmp_func_name

            candidate = candidate.replace('::', '_')
            final_list.append([key, func_name, list(candidates)[0], raw_strings])

    print()
    if len(classes) > 0:
        print("[+] Discovered class objects:")
        for obj in classes:
            print("------------------------")
            print(f"Address: 0x{obj[0]:x}")
            print("Tokens:")
            for tkn in obj[1]:
                print(f"\t* {tkn}")
    else:
        print("[-] No discovered class objects.")

    if len(final_list) > 0:
        print("[+] Function name candidates:")
        for elem in final_list:
            print("------------------------")
            print(f"Function address: 0x{elem[0]:x}")
            print(f"Current function name: {elem[1]}")
            print(f"Suggested name: {elem[2]}")
            print(f"Referenced strings:")
            for ref_str in elem[3]:
                print(f"\t* {ref_str}")
    else:
        print("[-] No function name candidates.")

#-------------------------------------------------------------------------------
def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath")
    parser.add_argument("-v", action="store_true")
    parser.add_argument("-vv", action="store_true")
    args = parser.parse_args()

    if args.vv:
        log.setLevel(logging.DEBUG)
    elif args.v:
        log.setLevel(logging.INFO)

    r2 = r2pipe.open(f"ccall://{args.filepath}", flags=["-2", "-q"])
    r2.use_cache = True

    # perform analysis
    #r2.cmd("aeim")
    #r2.cmd("e anal.hasnext=true")
    r2.cmd("aaaa")
    ida2r2.r2.set_r2_instance(r2)
    info, src_strs = get_source_strings()
    show_function_names(src_strs)
    r2.quit()

if __name__ == "__main__":
    main()
