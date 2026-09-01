import os
import sys
import json
import urllib.request
import urllib.error
import hashlib
import shutil
import tempfile
import re

import customtkinter as ctk


GITHUB_REPO = "IIxXDragonXxII/Sigma-hub"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}"
RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main"


def get_current_version():
    version_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "version.txt")
    try:
        with open(version_file, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        with open(version_file, "w") as f:
            f.write("1.0.0")
        return "1.0.0"


def save_version(version):
    version_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "version.txt")
    with open(version_file, "w") as f:
        f.write(version)


def get_github_latest_version():
    try:
        req = urllib.request.Request(
            f"{GITHUB_API_URL}/releases/latest",
            headers={"User-Agent": "SigmaHub-Update-Checker"},
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data.get("tag_name", "v0.0.0").lstrip("v")
    except Exception as e:
        print(f"Erro ao verificar releases: {e}")
        try:
            req = urllib.request.Request(
                f"{GITHUB_API_URL}/commits/main",
                headers={"User-Agent": "SigmaHub-Update-Checker"},
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))
                return data.get("commit", {}).get("sha", "")[:8]
        except Exception as e2:
            print(f"Erro ao verificar commits: {e2}")
            return None


def check_for_updates():
    current_version = get_current_version()
    latest_version = get_github_latest_version()

    if latest_version is None:
        return False, "Não foi possível verificar atualizações"

    if latest_version > current_version:
        return True, latest_version

    return False, None


def download_update():
    try:
        latest_req = urllib.request.Request(
            f"{GITHUB_API_URL}/releases/latest",
            headers={"User-Agent": "SigmaHub-Update-Checker"},
        )
        with urllib.request.urlopen(latest_req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            assets = data.get("assets", [])

            if not assets:
                print("Nenhum asset disponível na release")
                return False

            latest_asset = assets[0]
            download_url = latest_asset["browser_download_url"]
            asset_name = latest_asset["name"]

            print(f"Baixando atualização: {asset_name}")

            with urllib.request.urlopen(download_url, timeout=30) as dl_response:
                raw_data = dl_response.read()

            extract_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "updates"
            )
            os.makedirs(extract_dir, exist_ok=True)

            tmp_path = os.path.join(extract_dir, f"_tmp_{asset_name}")
            with open(tmp_path, "wb") as f:
                f.write(raw_data)

            return tmp_path, asset_name

    except Exception as e:
        print(f"Erro ao baixar atualização: {e}")
        return False


def apply_update(download_path, asset_name):
    try:
        extract_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "updates"
        )
        os.makedirs(extract_dir, exist_ok=True)

        if download_path and os.path.exists(download_path):
            if asset_name.endswith(".zip"):
                import zipfile

                with zipfile.ZipFile(download_path, "r") as zip_ref:
                    zip_ref.extractall(extract_dir)
            else:
                shutil.copy2(download_path, extract_dir)

            print("Aplicando atualização...")
            return True
        return False
    except Exception as e:
        print(f"Erro ao aplicar atualização: {e}")
        return False


def check_assets_changed():
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    version_file = os.path.join(assets_dir, ".assets_version.json")

    try:
        with open(version_file, "r") as f:
            prev_state = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        prev_state = {"files": {}, "total": 0}

    current_files = {}
    total_size = 0

    if os.path.isdir(assets_dir):
        for root, dirs, files in os.walk(assets_dir):
            for fname in files:
                fpath = os.path.join(root, fname)
                relpath = os.path.relpath(fpath, assets_dir)
                with open(fpath, "rb") as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                current_files[relpath] = {
                    "hash": file_hash,
                    "size": os.path.getsize(fpath),
                }
                total_size += os.path.getsize(fpath)

    has_changes = False
    if prev_state.get("total") != len(current_files) or prev_state.get("total") == 0:
        has_changes = True

    for relpath, info in current_files.items():
        if relpath not in prev_state.get("files", {}):
            has_changes = True
            print(f"Novo arquivo de asset: {relpath}")
        elif prev_state["files"][relpath].get("hash") != info["hash"]:
            has_changes = True
            print(f"Arquivo alterado: {relpath}")

    new_state = {"files": current_files, "total": len(current_files)}
    with open(version_file, "w") as f:
        json.dump(new_state, f)

    return has_changes


def run_update_check(parent_window=None):
    has_update, result = check_for_updates()
    assets_changed = check_assets_changed()

    result_msg = f"Versão atual: {get_current_version()}\n"

    if assets_changed:
        result_msg += "✓ Ativos foram modificados/adicionados\n"

    if has_update:
        result_msg += f"✓ Nova versão disponível: {result}\nDeseja baixar agora?"
        return True, result_msg
    elif assets_changed:
        result_msg += "Nenhuma nova versão de código, mas há alterações nos ativos."
        return False, result_msg
    else:
        result_msg += "Você tem a versão mais recente."
        return False, result_msg
