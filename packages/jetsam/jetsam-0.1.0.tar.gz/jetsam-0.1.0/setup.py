# ▓█████▄  ▄▄▄      ▓█████  ███▄ ▄███▓ ▒█████   ███▄    █  ██▓▒███████▒▓█████  ██▀███  
# ▒██▀ ██▌▒████▄    ▓█   ▀ ▓██▒▀█▀ ██▒▒██▒  ██▒ ██ ▀█   █ ▓██▒▒ ▒ ▒ ▄▀░▓█   ▀ ▓██ ▒ ██▒
# ░██   █▌▒██  ▀█▄  ▒███   ▓██    ▓██░▒██░  ██▒▓██  ▀█ ██▒▒██▒░ ▒ ▄▀▒░ ▒███   ▓██ ░▄█ ▒
# ░▓█▄   ▌░██▄▄▄▄██ ▒▓█  ▄ ▒██    ▒██ ▒██   ██░▓██▒  ▐▌██▒░██░  ▄▀▒   ░▒▓█  ▄ ▒██▀▀█▄  
# ░▒████▓  ▓█   ▓██▒░▒████▒▒██▒   ░██▒░ ████▓▒░▒██░   ▓██░░██░▒███████▒░▒████▒░██▓ ▒██▒
#  ▒▒▓  ▒  ▒▒   ▓▒█░░░ ▒░ ░░ ▒░   ░  ░░ ▒░▒░▒░ ░ ▒░   ▒ ▒ ░▓  ░▒▒ ▓░▒░▒░░ ▒░ ░░ ▒▓ ░▒▓░
#  ░ ▒  ▒   ▒   ▒▒ ░ ░ ░  ░░  ░      ░  ░ ▒ ▒░ ░ ░░   ░ ▒░ ▒ ░░░▒ ▒ ░ ▒ ░ ░  ░  ░▒ ░ ▒░
#  ░ ░  ░   ░   ▒      ░   ░      ░   ░ ░ ░ ▒     ░   ░ ░  ▒ ░░ ░ ░ ░ ░   ░     ░░   ░ 
#    ░          ░  ░   ░  ░       ░       ░ ░           ░  ░    ░ ░       ░  ░   ░     
#  ░                                                          ░                        
from setuptools import setup, Extension

with open("README.md", "r") as f:
      long_desc = f.read()

## ashore
## rigging
## jetsam

setup(name="jetsam",
      version="0.1.0",
      description="Takes a function and daemonizes it",
      long_description=long_desc,
      long_description_content_type="text/markdown",
      author="Tony B",
      author_email="tony@ballast.dev",
      license="MIT",
      license_files=["LICENSE"],
      ext_modules=[Extension(
            name="detacher", 
            sources=["src/jetsam/detach.c",
                     "src/jetsam/log.c"],
            include_dirs=["src/jetsam/"]
      )],
      package_dir={"": "src/"},
      project_urls={"source": "https://gitlab.com/ballast-dev/daemonizer"},
      python_requires=">=3.8",
)
