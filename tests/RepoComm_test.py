
from git import Repo
from proofOC.RepoCommunicator import RepoCommunicator, RepositoryConfigurationException, remoteRepoConfigured
import pytest 
import os
import shutil




@pytest.fixture()
def setUp():
    print("testing...")
    yield 
    shutil.rmtree('tests/local_test_repo')


def createRepo(url, localPath):
    return RepoCommunicator(url, localPath)

# Create new Repo with proper paths / URL 
def test_cloneIntoS(setUp):
    try : 
        createRepo("https://github.com/ccho-0508/testLi.git", "tests/local_test_repo")
        assert True 
    except RepositoryConfigurationException as exc:
        assert False, f"New repo creation raised an exception {exc}"


# Unable to create local repository exception
def test_cloneIntoF(setUp):
    try : 
        createRepo("https://github.", "tests/local_test_repo")
        assert False
    except RepositoryConfigurationException as exc:
        assert True, f"New repo creation raised an exception {exc}"

# Folder already exists
def test_setLocalRepo(setUp):
    try : 
        createRepo("https://github.com/ccho-0508/testLi.git", "tests/local_test_repo")
        createRepo("https://github.com/ccho-0508/newtestLi.git", "tests/local_test_repo")
        with open("tests/local_test_repo/remoteURL.txt") as f:
            assert f.readline() == "https://github.com/ccho-0508/newtestLi.git"
        # assert True 
    except RepositoryConfigurationException as exc:
        assert False, f"New repo creation raised an exception {exc}"

# Successful repo creation
def test_repoAddS(setUp):
    try : 
        repo = createRepo("https://github.com/ccho-0508/testLi.git", "tests/local_test_repo")
        repo.addFile("bookings.csv")
    except RepositoryConfigurationException as exc:
        assert False, f"'repo.addFile()' raised an exception {exc}"

# Successful repo creation
def test_repoAddF(setUp):
    try : 
        repo = createRepo("https://github.com/ccho-0508/testLi.git", "tests/local_test_repo")
        repo.addFile("tests/bookings.csv")
    except RepositoryConfigurationException as exc:
        assert True, f"'repo.addFile()' raised an exception {exc}"

# Push repo
def test_repoPushData(setUp):
    repo = createRepo("https://github.com/ccho-0508/testLi.git", "tests/local_test_repo")
    try : 
        repo.pushData()
    except RepositoryConfigurationException as exc:
        assert False, f"'repo.pushData())' raised an exception {exc}"
    

# remoteRepoConfigured() success
def test_remoteRepoConfigS(setUp):
    repo = createRepo("https://github.com/ccho-0508/testLi.git", "tests/local_test_repo")
    assert remoteRepoConfigured("tests/local_test_repo") == "https://github.com/ccho-0508/testLi.git"

# remoteRepoConfigured() failure
def test_remoteRepoConfigF():
    assert remoteRepoConfigured("tests/local_test_repo") == ""


def test_createFolderGithub(setUp):
    # try:
    createRepo("https://github.com/ccho-0508/testLi.git", "tests/local_test_repo")
    shutil.rmtree('tests/local_test_repo/.github')
    createRepo("https://github.com/ccho-0508/testLi.git", "tests/local_test_repo")

    assert os.path.exists('tests/local_test_repo/.github/workflows') 
 
def test_createFolderScripts(setUp):
    # try:
    createRepo("https://github.com/ccho-0508/testLi.git", "tests/local_test_repo")
    os.remove("tests/local_test_repo/scripts/actionScript.py")
    os.remove("tests/local_test_repo/scripts/requirements.txt")
    os.remove("tests/local_test_repo/scripts/TraverseSite.py")
    
    # shutil.rmtree('tests/local_test_repo/scripts')
    createRepo("https://github.com/ccho-0508/testLi.git", "tests/local_test_repo")

    assert os.path.exists('tests/local_test_repo/scripts')







    
