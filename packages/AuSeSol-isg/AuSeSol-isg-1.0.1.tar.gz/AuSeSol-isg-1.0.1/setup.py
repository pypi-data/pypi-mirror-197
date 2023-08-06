from setuptools import find_packages, setup



# we use the README file to fill the "long description" variable
with open("README.md" , "r") as f:
    long_description = f.read()

setup(

    name = "AuSeSol-isg",
    version = "1.0.1",
    description=  "Package to process, train and evaluate time series related data in solar energy field",
    long_description = long_description, 
    long_description_content_type = "text/markdown",
    py_modules=["Preprocessing" , "Databases" , "Feature_Correlation" , "Plotting"], 
    package_dir = {"" : "src"},
    packages = ["isg"],
    url = "https://gitlab.com/alaan.sheikhani/isg_project", 
    aurthor = ["Alaan" , "Andres"], 
    author_email= "alaan.sheikhani@industrial-solar.de" ,
    license="MIT",
    install_requires= None, # for production dependencies (Flask, Numpy, Pandas). Version should be relaxed as possible
    extras_require = {
    "dev": ["pandas >= 1.4.0 " , "scipy >= 1.9.0" , "scikit-learn >= 1.0.0"]

    }  # dependencies for development mostly and specially for optional requirements (e.g. pytest).
     # Version should be more spesific than install_requires



)