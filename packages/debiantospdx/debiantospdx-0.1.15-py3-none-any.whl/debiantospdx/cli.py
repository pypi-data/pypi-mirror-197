import argparse
import json
import os
import re
import subprocess
import sys
import time

from debiantospdx import deb_spdx
from debiantospdx.search import (
    print_package_info,
    print_spdx_files_info,
    take_spdx_path,
)


def make_pv_vrp_dict(pv_dict: dict[str, str], vrp_dict: dict[str, list[list[str]]]):
    """
    pv_dict と vrp_dict の作成

    Args:
        pv_dict: パッケージとバージョンの対応辞書
        vrp_dict: Virtual と Replace の辞書
    """
    dpkg_status_list = subprocess.run(
        ["dpkg-query", "-W", "-f=${Package}\t${Provides}\t${Replaces}\t${Version}\n"], capture_output=True, text=True
    ).stdout.splitlines()

    # Virtual と Replace の辞書作成
    for dpkg_s in dpkg_status_list:

        # dpkg_s_list: Package, Provides, Replaces, Version
        dpkg_s_list = dpkg_s.strip().split("\t")

        pv_dict[dpkg_s_list[0]] = dpkg_s_list[3]

        if dpkg_s_list[1]:
            add_vrp_dict(dpkg_s_list[1], dpkg_s_list[0], vrp_dict)
        if dpkg_s_list[2]:
            add_vrp_dict(dpkg_s_list[2], dpkg_s_list[0], vrp_dict)

    # 重複削除
    for key, value in vrp_dict.items():
        vrp_dict[key] = [list(j) for j in list(set([tuple(i) for i in value]))]


def add_vrp_dict(vrp_names: str, p_name: str, vrp_dict: dict[str, list[list[str]]]):
    """
    Virtual と Replace の辞書に情報を追加

    Args:
        vrp_names: 代替できるパッケージの名前の列記
        p_name: リアルなパッケージの名前
        vrp_dict: Virtual と Replace の辞書
    """
    vrp_name_list = vrp_names.split(", ")
    for vrp_name in vrp_name_list:
        # vrp_name_split: [Virtual or Replace Package, (比較演算子, Version)]
        vrp_name_split = [i for i in re.split(" |\\(|\\)|\\[.*?\\]", vrp_name) if i]

        if vrp_name_split[0] in vrp_dict:
            vrp_dict[vrp_name_split[0]].append([p_name] + vrp_name_split[1:])
        else:
            vrp_dict[vrp_name_split[0]] = [[p_name] + vrp_name_split[1:]]


def main(package, person, organization, all_analyze, path, search, mode, dep_mode, printinfo) -> None:
    time_start = time.perf_counter()

    pv_dict: dict[str, str] = {}  # {p_name: version}
    # {vrp_name: [[p_name, c_operator, version]]}
    vrp_dict: dict[str, list[list[str]]] = {}

    make_pv_vrp_dict(pv_dict, vrp_dict)  # type: ignore

    # ディレクトリ記憶
    cwd = os.getcwd()

    os.chdir(path)

    # #####CHANGE##### #
    import shutil

    set_command_dict: dict[str, dict[str, int]] = {}
    for p_name in pv_dict:
        os.mkdir(p_name)
        os.chdir(p_name)
        set_command_dict[p_name] = {}
        deb_class = deb_spdx.DebSpdx(
            pv_dict, vrp_dict, p_name, person, organization, [], 0, set_command_dict[p_name], 0, 0
        )
        deb_class.init_treated_list()
        deb_class.run()
        os.chdir("../")
        shutil.rmtree(p_name)
        if set_command_dict[p_name]:
            maxdepth = max(set_command_dict[p_name].values())
        else:
            maxdepth = 1
        for p in pv_dict:
            if p not in set_command_dict[p_name]:
                set_command_dict[p_name][p] = maxdepth
    else:
        with open("command_dict.json", "w") as f:
            json.dump(set_command_dict, f, indent=4)

    os.chdir(cwd)

    time_finish = time.perf_counter()

    print("\ndebiantospdx finish")
    print("time: ", time_finish - time_start)


# 引数の処理 （エントリーポイント）
def entry():
    parser = argparse.ArgumentParser(
        prog="debiantospdx",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""Add directory path and some option.

    Analysis mode has 4 options
        0: Do not analyze files
        1: Analyze the file, but do not analyze licenses
        2: Analyze licenses of copyright file only
        3: Analyze licenses of all files""",
    )
    # 必須の位置引数
    parser.add_argument("path", type=str, help="Path of directory where SPDX files are located")

    # オプション引数 変数名は長い方になる（p, oは省略形）
    parser.add_argument("-p", "--person", nargs="+", type=str, help="The person that created the SPDX file")
    parser.add_argument("-pe", type=str, help="Person's email")
    parser.add_argument("-o", "--organization", nargs="+", type=str, help="The organization that created the SPDX file")
    parser.add_argument("-oe", type=str, help="Organization's email")

    parser.add_argument(
        "-m",
        "--mode",
        default=2,
        type=int,
        help="Analysis mode for the specified package or all packages (default = 2)",
    )
    parser.add_argument(
        "-d",
        "--dep_mode",
        default=1,
        type=int,
        help="Analysis mode for the dependent packages (default = 1)",
    )

    # 排他的で必須なオプション引数
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--package", type=str, help="Analyze specified package")
    group.add_argument("--all", action="store_true", help="Analyze all Debian packages")
    group.add_argument("--search", type=str, help="Print package information from SPDX files")
    group.add_argument("--printinfo", action="store_true", help="Print SPDX files' information")

    args = parser.parse_args()

    args_person = None
    args_organization = None
    if ((args.package is not None) or args.all) and ((args.person is None) and (args.organization is None)):
        raise Exception("Enter Creator Name: person or organization")

    if args.person is not None:
        args_person = " ".join(args.person) + " (" + args.pe + ")"
    if args.organization is not None:
        args_organization = " ".join(args.organization) + " (" + args.oe + ")"

    if not (0 <= args.mode <= 3 and 0 <= args.dep_mode <= 3):
        raise ValueError("Undefined mode")

    main(
        path=args.path,
        person=args_person,
        organization=args_organization,
        mode=args.mode,
        dep_mode=args.dep_mode,
        package=args.package,
        all_analyze=args.all,
        search=args.search,
        printinfo=args.printinfo,
    )
