import os
import shutil
import time
import zipfile
import json
import yaml
import toml
from configparser import ConfigParser

import requests
from github import Github


def update(package_name, repo_name, version_key='Version', config_exts=['.txt', '.yml', '.json', '.tmol','.ini']):
    print("Current working directory:", os.getcwd())

    """
    Downloads the latest release of a package from a GitHub repository and replaces the old files with the new ones.

    :param package_name: The name of the package to update.
    :param repo_name: The name of the GitHub repository to check for updates.
    :param version_key: The key in the package configuration file that contains the current version.
    :param config_exts: A list of file extensions for the package configuration file.
    """
    # get the package configuration
    config_file = None
    for ext in config_exts:
        if os.path.exists(os.path.join(os.path.expanduser("~"), f"{package_name}{ext}")):
            config_file = os.path.join(os.path.expanduser("~"), f"{package_name}{ext}")
            break
    print(os.path.abspath(os.path.join(os.path.expanduser("~"), f"{package_name}{ext}")))
    if not config_file:
        raise FileNotFoundError(f"Configuration file not found: {','.join(config_exts)}")

    config_type = os.path.splitext(config_file)[1].lower()[1:]
    config = ConfigParser()

    if config_type == 'ini':
        config.read(config_file)
    elif config_type == 'json':
        with open(config_file) as f:
            config.read_string(json.dumps(json.load(f)))
    elif config_type == 'yml' or config_type == 'yaml':
        with open(config_file) as f:
            config.read_string(json.dumps(yaml.safe_load(f)))
    elif config_type == 'tmol':
        with open(config_file) as f:
            config.read_string(toml.dumps(toml.load(f)))
    else:
        raise ValueError(f"Unsupported config file type: {config_type}")

    # create a Github instance
    g = Github()

    # get the repository by name and owner
    repo = g.get_repo(repo_name)

    # get the latest release tag with prefix "v"
    latest_tag = None
    for tag in repo.get_tags():
        if tag.name.startswith("v"):
            commit = tag.commit
            if not latest_tag or commit.committer.created_at > latest_tag.commit.committer.created_at:
                latest_tag = tag

    if not latest_tag:
        print("Latest tag not found")
    else:
        print(f"Latest tag found: {latest_tag.name}")
        # get the latest release associated with the tag
        latest_release = None
        for release in repo.get_releases():
            if release.tag_name == latest_tag.name:
                latest_release = release
                break

        if not latest_release:
            print("Latest release not found")
        elif latest_tag.name == config.get(version_key, ''):
            print("Already up-to-date")
        else:
            # download the latest release asset
            download_url = latest_release.zipball_url
            r = requests.get(download_url)
            with open("new_files.zip", "wb") as f:
                f.write(r.content)

            print("Downloaded the latest release asset")

            # extract the contents of the zip file
            with zipfile.ZipFile("new_files.zip", "r") as zip_ref:
                zip_ref.extractall("new_files")

            print("Extracted the contents of the zip file")

            # delete the zip file
            os.remove("new_files.zip")

            print("Deleted the zip file")

            # replace old files with new ones
            package_dir = os.path.dirname(os.path.abspath(config_file))
            old_files_dir = os.path.join(package_dir, "old_files")
            new_files_dir = os.path.join(package_dir, "new_files")
            if os.path.exists(old_files_dir):
                shutil.rmtree(old_files_dir)
            shutil.move(new_files_dir, old_files_dir)

            print("Replaced old files with new ones")

            # update the version in the config file
            config.set(version_key, latest_tag.name)
            with open(config_file, "w") as config_file:
                config.write(config_file)

            print("Updated the version in the config file")

            print("Downloaded and installed the latest version")

            time.sleep(1)