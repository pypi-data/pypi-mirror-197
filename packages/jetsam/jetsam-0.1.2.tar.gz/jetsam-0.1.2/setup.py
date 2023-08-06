#  ▐▄▄▄▄▄▄ .▄▄▄▄▄.▄▄ ·  ▄▄▄· • ▌ ▄ ·. 
#   ·██▀▄.▀·•██  ▐█ ▀. ▐█ ▀█ ·██ ▐███▪
# ▪▄ ██▐▀▀▪▄ ▐█.▪▄▀▀▀█▄▄█▀▀█ ▐█ ▌▐▌▐█·
# ▐▌▐█▌▐█▄▄▌ ▐█▌·▐█▄▪▐█▐█ ▪▐▌██ ██▌▐█▌
#  ▀▀▀• ▀▀▀  ▀▀▀  ▀▀▀▀  ▀  ▀ ▀▀  █▪▀▀▀
from setuptools import setup, Extension

with open("README.md", "r") as f:
      long_desc = f.read()

setup(name="jetsam",
      version="0.1.2",
      description="Daemonizes functions: eject and forget!",
      long_description=long_desc,
      long_description_content_type="text/markdown",
      author="Tony B",
      author_email="tony@ballast.dev",
      license="MIT",
      license_files=["LICENSE"],
      ext_modules=[Extension(
            name="detacher", 
            sources=["src/detach.c", "src/log.c"],
            include_dirs=["src/"]  # this is broken, need MANIFEST.in
      )],
      package_dir={"": "src/"},
      # since package_dir is set, no automatic discovery 
      py_modules=["jetsam"],
      project_urls={"Source Code": "https://gitlab.com/ballast-dev/jetsam"},
      python_requires=">=3.8",
)
