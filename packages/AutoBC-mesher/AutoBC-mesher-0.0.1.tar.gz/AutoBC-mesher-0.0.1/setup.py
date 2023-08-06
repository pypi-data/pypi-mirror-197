from setuptools import setup 
setup(name='AutoBC-mesher',
      version='0.0.1',
      description='This mesher generate 2d unstructured mesh with boundary condition (BC) given geometry information and BC information.',
      author='Chengrui Sun',
      author_email='chengruisun03@gmail.com',
      requires= ['numpy','matplotlib', 'scipy', 'pymesh2', 'meshio', 'argparse'], 
      packages=['AutoBC-mesher'],  
      license="apache 3.0"
      )