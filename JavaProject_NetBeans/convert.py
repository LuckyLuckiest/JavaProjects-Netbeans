"""
Original Creator: devanshkaloti
Minor changes: Hashim AbdulBasit
"""

import shutil, os

def openFile(file, permission):
    try:
        return open(file, permission)
    except FileNotFoundError as e:
        print("** File Not Found %s**" % file)
    except PermissionError:
        print("** Insufficient permissions to open file %s**\n\n" % file)
    except Exception:
        print("** Unknown Error While Opening File:  %s**\n\n" % file)

# Reset the output folder to template.
def resetFolder():
    with openFile("template/project.xml", "r") as templateProjectXML:
        with openFile("nbproject/project.xml", "w") as outputProjectXML:
            outputProjectXML.write(templateProjectXML.read())

    with openFile("template/project.properties", "r") as templateProperties:
        with openFile("nbproject/project.properties", "w") as outputProperties:
            outputProperties.write(templateProperties.read())

# Coping contents of src folder to final folder
# @param src source file path
# @param duplicated file path
def copyFolder(src, dist):
    try:
        shutil.copytree(src, dist)  # Copy files
    except FileExistsError:
        print("Error: Files already exists")
    except FileNotFoundError:
        print("Error: Folder could not be located: " + dist)
    except Exception:
        print("Error: Unknown Error")

# Get the project name, by finding last in pathname
# @param path uses the path of the source folder
def getProjectName(path):
    return str(path).split("/")[path.count("/")]

# Replace the Project Name In XML file
def replaceProjectName(src):
    file = openFile("nbproject/project.xml", "r")
    lines = file.readlines()
    file.close()

    for i, line in enumerate(lines):
        if "<name>******************</name>" in line:
            lines[i] = "<name>%s</name>\n" % getProjectName(src)

    with openFile("nbproject/project.xml", "w") as file:
        file.write(''.join(lines))

def isJavaProject(src):
    if not "src" in os.listdir(src):
        raise Exception("This file is not a java project.")

def isNetBeansProject(src):
    val = 0
    if "nbproject" in os.listdir(src):
        for file in os.listdir(src + "\\nbproject"):
            if file == "project.properties" or file == "project.xml":
                val += 1
    if val > 1:
        raise FileExistsError("Already converted to NetBeans project.")

# @param src the path of the project folder.
def project(src):
    """
    Converts one project at a specific path.
    Checks if the project was a java project.
    """
    isJavaProject(src)

    isNetBeansProject(src)

    dstPath = src + "_NB"

    replaceProjectName(src)

    copyFolder(src + "/src", dstPath + "/src")  # Copy coding
    copyFolder("nbproject", dstPath + "/nbproject")  # Copy settings

    resetFolder()

# @param src the source path of the folder containg the projects.
def folder(src):
    """
    Converts a folder filled with projects.
    """
    length = 0
    for path in os.listdir(src):
        # Check if folder
        if os.path.isdir(os.path.join(src, path)):
            try:
                project(src + "\\" + path)
                length += 1
            except FileExistsError:
                print("Already converted")
            except Exception:
                print("Not a java project...Skipping")
    print("Projects converted:", length)

# @param type gets the type if it was directly one file or a folder that contains multiple projects.
def options(type):
    """
    Gives the user to choose either a folder or a file and process the rest of the program.
    """
    path = input("Enter Path: ").strip(" ")
    if type == "fld":
        folder(path)
    elif type == "sp":
        project(path)
    else:
        print("Invalid option.\nUsing single project folder only option.\n")
        project(path)

def main():
    print("\nThis program will copy your original project and make it NetBeans Compatible.")
    print("Please make sure your programming files are located under 'src/'\n")

    print("Type 'fld' or 'sp'\n'fld' is for a folder with projects.\n'sp' is for a specific project.\n")
    type = input("Want to convert folder or specific project: ").lower()

    options(type)

    print("\nYour project(s) has been converted!\nPlease look in your source directory.")

main()
