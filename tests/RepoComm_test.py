
from git import Repo
from proofOC.RepoCommunicator import RepoCommunicator, RepositoryConfigurationException, remoteRepoConfigured
import pytest 
import os
import shutil
from stat import S_IREAD, S_IRGRP, S_IROTH
import time


mainPath="tests/local_test_repo"

@pytest.fixture()
def setUp():
    print("testing")
    yield
    deletingD = [".github/", "scripts/", ".git/","bookings.csv", "remoteURL.txt", "scripts"]
    
    for i in deletingD:
        try:
            if(i[-1]=="/"):
                shutil.rmtree(f"{mainPath}/{i}")
            else:
                os.remove(f"{mainPath}/{i}")
        except:
            pass
    
    shutil.rmtree(mainPath)
    time.sleep(5)

def createRepo(url, localPath):
    return RepoCommunicator(url, localPath)


# Create new Repo with proper paths / URL 
def test_cloneIntoS(setUp):
    try : 
        createRepo("https://github.com/ccho-0508/testLi.git", mainPath)
        assert True 
    except RepositoryConfigurationException as exc:
        assert False, f"New repo creation raised an exception {exc}"
    time.sleep(1)


# Unable to create local repository exception
def test_cloneIntoF(setUp):
    try : 
        createRepo("https://github.", mainPath)
        assert False
    except RepositoryConfigurationException as exc:
        assert True, f"New repo creation raised an exception {exc}"

# Folder already exists
def test_setLocalRepoS(setUp):
    try : 
        createRepo("https://github.com/ccho-0508/testLi.git", mainPath)
        createRepo("https://github.com/ccho-0508/newtestLi.git", mainPath)
        with open(f"{mainPath}/remoteURL.txt") as f:
            assert f.readline() == "https://github.com/ccho-0508/newtestLi.git"

    except RepositoryConfigurationException as exc:
        assert False, f"New repo creation raised an exception {exc}"


# Folder already exists
def test_setLocalRepoF(setUp):
    try : 
        createRepo("https://github.com/ccho-0508/testLi.git", mainPath)
       
        filename = f"{mainPath}/remoteURL.txt"
        os.chmod(filename, S_IREAD|S_IRGRP|S_IROTH)
        createRepo("https://github.com/ccho-0508/newtestLi.git", mainPath)
        assert False
    except RepositoryConfigurationException as exc:
        assert True, f"New repo creation raised an exception {exc}"


# Successful repo creation
def test_repoAddS(setUp):
    try : 
        repo = createRepo("https://github.com/ccho-0508/testLi.git", mainPath)
        repo.addFile("bookings.csv")
    except RepositoryConfigurationException as exc:
        assert False, f"'repo.addFile()' raised an exception {exc}"

# # Successful repo creation
def test_repoAddF(setUp):
    try : 
        repo = createRepo("https://github.com/ccho-0508/testLi.git", mainPath)
        repo.addFile("tests/bookings.csv")
    except RepositoryConfigurationException as exc:
        assert True, f"'repo.addFile()' raised an exception {exc}"

# Push repo
def test_repoPushData(setUp):
    repo = createRepo("https://github.com/ccho-0508/testLi.git", mainPath)
    try : 
        repo.pushData()
    except RepositoryConfigurationException as exc:
        assert False, f"'repo.pushData())' raised an exception {exc}"

# Push repo
def test_repoPushData(setUp):
    repo = createRepo("https://github.com/ccho-0508/testLi.git", mainPath)
    try : 
        repo.repo = None
        repo.pushData()
        assert False
    except RepositoryConfigurationException as exc:
        assert True, f"'repo.pushData())' raised an exception {exc}"
    


# remoteRepoConfigured() success
def test_remoteRepoConfigS(setUp):
    repo = createRepo("https://github.com/ccho-0508/testLi.git", mainPath)
    assert remoteRepoConfigured(mainPath) == "https://github.com/ccho-0508/testLi.git"

# remoteRepoConfigured() failure
def test_remoteRepoConfigF():
    assert remoteRepoConfigured(mainPath) == ""


def test_createFolderGithub(setUp):
    createRepo("https://github.com/ccho-0508/testLi.git", mainPath)
    shutil.rmtree(f"{mainPath}/.github")
    createRepo("https://github.com/ccho-0508/testLi.git", mainPath)
    assert os.path.exists(f"{mainPath}/.github/workflows") 
 
def test_createFolderScripts(setUp):
    createRepo("https://github.com/ccho-0508/testLi.git", mainPath)
    shutil.rmtree(f"{mainPath}/scripts")
    createRepo("https://github.com/ccho-0508/testLi.git", mainPath)
    assert os.path.exists(f"{mainPath}/scripts")

 
