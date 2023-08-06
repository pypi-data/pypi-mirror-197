#  ▐▄▄▄▄▄▄ .▄▄▄▄▄.▄▄ ·  ▄▄▄· • ▌ ▄ ·. 
#   ·██▀▄.▀·•██  ▐█ ▀. ▐█ ▀█ ·██ ▐███▪
# ▪▄ ██▐▀▀▪▄ ▐█.▪▄▀▀▀█▄▄█▀▀█ ▐█ ▌▐▌▐█·
# ▐▌▐█▌▐█▄▄▌ ▐█▌·▐█▄▪▐█▐█ ▪▐▌██ ██▌▐█▌
#  ▀▀▀• ▀▀▀  ▀▀▀  ▀▀▀▀  ▀  ▀ ▀▀  █▪▀▀▀
from setuptools import setup, Extension

with open("README.md", "r") as f:
      long_desc = f.read()

setup(name="jetsam",
      version="0.1.1",
      description="Daemonizes functions: eject and forget!",
      long_description=long_desc,
      long_description_content_type="text/markdown",
      author="Tony B",
      author_email="tony@ballast.dev",
      license="MIT",
      license_files=["LICENSE"],
      ext_modules=[Extension(
            "detacher", 
            ["src/jetsam/detach.c", "src/jetsam/log.c"],
      )],
      package_dir={"": "src/"},
      py_modules=["jetsam"],
      project_urls={"Source Code": "https://gitlab.com/ballast-dev/jetsam"},
      python_requires=">=3.8",
)
