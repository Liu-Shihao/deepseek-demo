import requests
from typing import Dict, Union

# 定义目录结构的数据类型
DirectoryStructure = Dict[str, Union[str, 'DirectoryStructure']]




def fetch_github_directory_contents(api_url: str, access_token: str = None) -> list:
    """
    从GitHub API获取目录内容

    :param api_url: GitHub API的URL
    :param access_token: GitHub API的访问令牌（可选）
    :return: 目录内容列表
    """
    headers = {}
    if access_token:
        headers['Authorization'] = f'token {access_token}'

    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch directory contents: {response.status_code} - {response.text}")

    return response.json()


def build_directory_structure(contents: list, access_token: str = None) -> DirectoryStructure:
    """
    构建目录结构

    :param contents: GitHub API返回的目录内容列表
    :param access_token: GitHub API的访问令牌（可选）
    :return: 目录结构
    """
    directory_structure: DirectoryStructure = {}

    for item in contents:
        if item['type'] == 'file':
            # 如果是文件，直接添加到目录结构中
            directory_structure[item['name']] = item['download_url']
        elif item['type'] == 'dir':
            # 如果是目录，递归获取子目录内容
            subdir_contents = fetch_github_directory_contents(item['url'], access_token)
            directory_structure[item['name']] = build_directory_structure(subdir_contents, access_token)

    return directory_structure


def generate_tree_structure(directory_structure: DirectoryStructure, prefix: str = "") -> str:
    """
    生成树状结构的字符串

    :param directory_structure: 目录结构（字典）
    :param prefix: 当前层级的前缀（用于递归）
    :return: 树状结构的字符串
    """
    tree_str = ""
    keys = list(directory_structure.keys())
    for i, key in enumerate(keys):
        if i == len(keys) - 1:
            # 当前目录或文件的最后一个条目
            tree_str += f"{prefix}└── {key}\n"
            new_prefix = prefix + "    "
        else:
            # 当前目录或文件的中间条目
            tree_str += f"{prefix}├── {key}\n"
            new_prefix = prefix + "│   "

        if isinstance(directory_structure[key], dict):
            # 如果是目录，递归生成子目录的树状结构
            tree_str += generate_tree_structure(directory_structure[key], new_prefix)
    return tree_str


def get_repo_directory_structure(repo_url: str, access_token: str = None) -> str:


    # 获取根目录内容
    contents = fetch_github_directory_contents(repo_url, access_token)

    # 构建目录结构
    directory_structure = build_directory_structure(contents, access_token)

    # 生成树状结构字符串
    return generate_tree_structure(directory_structure)


# 示例使用
repo_url = 'https://api.github.com/repos/Liu-Shihao/lucene-demo/contents'
access_token = '<TOKEN>'  # 可选，如果需要访问私有仓库
tree_str = get_repo_directory_structure(repo_url, access_token)
print(tree_str)
