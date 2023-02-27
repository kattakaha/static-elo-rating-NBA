import os
import string

import termcolor


def get_template_dir_path():
    """テンプレートファイルのディレクトリパスを返します
    Returns:
        str: テンプレートファイルのディレクトリパスを返します
    """
    template_dir_path = None
    try:
        import settings

        if settings.TEMPLATE_PATH:
            template_dir_path = settings.TEMPLATE_PATH
    except ImportError:
        pass

    if not template_dir_path:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        template_dir_path = os.path.join(base_dir, "templates")

    return template_dir_path


class NoTemplateError(Exception):
    """テンプレートが存在しないエラー"""


def find_template(temp_file):
    """テンプレートファイルのパスを作成
    Args:
        temp_file (str): テンプレートファイルのファイル名
    Returns:
        temp_file_path: テンプレートファイルのパス
    Raises:
        NoTemplateError: temp_fileが存在しない場合のエラー
    """
    template_dir_path = get_template_dir_path()
    temp_file_path = os.path.join(template_dir_path, temp_file)
    if not os.path.exists(temp_file_path):
        raise NoTemplateError("Could not find {}".format(temp_file))

    return temp_file_path


def get_template(temp_file_path, color=None):
    """テンプレートファイルを返します
    Args:
        temp_file_path (str): テンプレートファイルのパス
        color ([type], optional): ターミナルで出力する色を制御します
            詳しい情報はこちらをご覧ください.
                https://pypi.python.org/pypi/termcolor
    Returns:
        string.Template: テンプレートの文字列を返します.
    """

    template = find_template(temp_file_path)
    with open(template, "r") as template_file:
        # 読み込み
        contents = template_file.read()
        # 改行を除去
        contents = contents.rstrip(os.linesep)
        contents = "{splitter}{sep}{contents}{sep}{splitter}{sep}".format(
            contents=contents, splitter="-" * 60, sep=os.linesep
        )
        contents = termcolor.colored(contents, color)
        # .substituteで辞書型でcontentsの変数情報を与える必要がある
        return string.Template(contents)


def rating_info(team, rating, delta):
    """レイティング更新情報を返す"""

    def get_color(delta):
        if delta > 0:
            return "red"
        else:
            return "blue"

    def get_sign(delta):
        if delta > 0:
            return "+"
        else:
            return ""

    color = get_color(delta)
    sign = get_sign(delta)
    delta = termcolor.colored(sign + str(delta), color)
    contents = "{team}{sep}{rating}{sep}{delta}{linesep}".format(
        team=team, rating=str(rating), delta=delta, sep=", ", linesep="\n"
    )

    return contents


def _debug_template(template_filename="debug.txt", contents=None, color="green"):
    """テンプレートファイルをプリントデバッグします
    Args:
        template_filename (str): テンプレートファイルのファイル名
        contents (dict): テンプレートファイルのコンテンツを辞書形式で受け取る
        color ([type], optional): ターミナルで出力する色を制御します
            詳しい情報はこちらをご覧ください.
                https://pypi.python.org/pypi/termcolor
    """
    filepath = find_template(template_filename)
    template = get_template(template_filename, color)
    if not contents:
        contents = {"filepath": filepath}
    print(template.substitute(contents))
