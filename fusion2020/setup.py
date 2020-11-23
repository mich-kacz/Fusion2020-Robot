from setuptools import setup

package_name = 'fusion2020'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='ubuntu@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'clientudp = fusion2020.client_udp:main',
            'keyboard = fusion2020.teleop_twist_keyboard:main',
            'control = fusion2020.communication:main',
            'manual = fusion2020.manual:main',
            'auto_mode = fusion2020.auto_driving:main',
        ],
    },
)
