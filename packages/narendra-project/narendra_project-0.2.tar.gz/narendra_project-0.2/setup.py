from setuptools import setup

setup_args=dict(
    name="narendra_project",
    version="0.2",
    description="package to upload user strategy code using command line interface",
    author="narendra",
    author_email="narendranaidu5398@gmail.com",
    packages=['narendra_project'],
    install_requires=['maskpass'],
    url="https://github.com/narendra539804/narendra_package.git"
)

def main():
    setup(**setup_args)


if __name__ == '__main__':
    main()