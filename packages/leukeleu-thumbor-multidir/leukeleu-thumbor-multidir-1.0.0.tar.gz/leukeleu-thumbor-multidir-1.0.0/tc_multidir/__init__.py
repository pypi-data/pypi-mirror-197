from thumbor.config import Config

Config.define(
    "TC_MULTIDIR_PATHS",
    [],
    "The list of paths where the multidir loader will try to find images",
    "File Loader",
)
