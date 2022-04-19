import pytest
import shutil
import os

from unittest import mock, TestCase
from proofOC.RepoCommunicator import RepoCommunicator, RepositoryConfigurationException, remoteRepoConfigured

class Test_RepoCommunicator(TestCase):

  LOCAL_PATH_NAME = "local"

  @classmethod
  def setUp(self):
    pass

  @classmethod
  def tearDown(self):
    if os.path.exists(self.LOCAL_PATH_NAME) and os.path.isdir(self.LOCAL_PATH_NAME):
      shutil.rmtree(self.LOCAL_PATH_NAME)
    else: 
      os.remove(self.LOCAL_PATH_NAME)

  @mock.patch('proofOC.RepoCommunicator.git')
  def test_repo_create_from_empty(self, mock_git):
    p = mock.PropertyMock(return_value=False)
    type(mock_git.Repo.clone_from.return_value).bare = p
    repo = RepoCommunicator("remote", self.LOCAL_PATH_NAME)
    # repo object and folders were created
    assert repo.repo is not None
    assert os.path.exists(f"{self.LOCAL_PATH_NAME}/.github/workflows")
    assert os.path.exists(f"{self.LOCAL_PATH_NAME}/scripts")


  def test_repo_create_invalid_remote_fails(self):
    with pytest.raises(RepositoryConfigurationException) as test_exception:
      repo = RepoCommunicator("bad_remote", self.LOCAL_PATH_NAME)

    assert "Unable to create local repository" in str(test_exception.value)

  @mock.patch('proofOC.RepoCommunicator.git')
  def test_repo_create_existing_path(self, mock_git):
    # create directory and file from it
    os.mkdir(self.LOCAL_PATH_NAME)
    with open(f"{self.LOCAL_PATH_NAME}/remoteURL.txt", "w+") as f:
      f.write("test remoteURL")

    # create the repo now that the path exists
    p = mock.PropertyMock(return_value=False)
    type(mock_git.Repo.clone_from.return_value).bare = p
    repo = RepoCommunicator("remote", self.LOCAL_PATH_NAME)
    assert repo.repo is not None

  def test_repo_create_existing_path_fails(self):
    # create directory and file from it
    os.mkdir(self.LOCAL_PATH_NAME)
    with open(f"{self.LOCAL_PATH_NAME}/remoteURL.txt", "w+") as f:
      f.write("test remoteURL")

    with pytest.raises(RepositoryConfigurationException) as test_exception:
      repo = RepoCommunicator("bad_remote", self.LOCAL_PATH_NAME)

    assert "Error setting local repo" in str(test_exception.value)

  def test_make_repo_from_non_dir(self):
    with open(self.LOCAL_PATH_NAME, "w+") as f:
      f.write("file instead of path")

    with pytest.raises(RepositoryConfigurationException) as test_exception:
      repo = RepoCommunicator("bad_remote", self.LOCAL_PATH_NAME)

    assert "not a directory" in str(test_exception.value)