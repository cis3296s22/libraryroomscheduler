import logging
import git
import os

def remoteRepoConfigured(repoPath: str):
  if os.path.exists(f"{repoPath}/remoteURL.txt"):
    with open(f"{repoPath}/remoteURL.txt", "r") as f:
      return f.readline().rstrip()
  return ""

class RepositoryConfigurationException(Exception):
  pass

class RepoCommunicator:

  def __init__(self, remoteRepoUrl: str, localPath: str):
    """
    Instantiates the local repository to comminucate with GitHub.
    If the local repo has not been created, it will create one.
    """
    self.remoteRepoUrl = remoteRepoUrl
    self.localPath = localPath
    self.workflowPath = localPath + "/.github/workflows"
    self.actionsPath = localPath + "/scripts"
    self.logger = logging.getLogger("appLog")

    if not os.path.exists(localPath):
    # path doesn't exist, create it
      os.mkdir(localPath)

    if os.path.exists(localPath) and os.path.isdir(localPath):
    # path exists and is a directory
      if len(os.listdir(localPath)):
      # it's not empty, set local to it
        try:
          self.repo = git.Repo(os.path.realpath(localPath))
        # if remote file doesn't exist, recreate it
        # TODO validate this with git remote instead of string passed in
          with open(f"{localPath}/remoteURL.txt", "w+") as f:
              f.write(remoteRepoUrl)
        except Exception:
          self.logger.exception("Unable to set local repo path:")
          raise RepositoryConfigurationException(f"Error setting local repo to {localPath}.")
          
      else:
      # it's empty, clone into it
        try:
          self.repo = git.Repo.clone_from(remoteRepoUrl, localPath)
          with open(f"{localPath}/remoteURL.txt", "w+") as f:
            f.write(remoteRepoUrl)

        except Exception:
          self.logger.exception("Unable to create local repository:")
          raise RepositoryConfigurationException(f"Unable to create local repository. Make sure {remoteRepoUrl} is your private repo. If it is you may need to configure SSH cloning.")
    else:
    # path exists but is not a directory
    # this "shouldn't" trigger since the dir is hardcoded
      raise RepositoryConfigurationException(f"{localPath} is not a directory.")



    # Create nested .github/workflows directories and copy in yaml file
    if not os.path.exists(self.workflowPath):
      try:
        os.makedirs(self.workflowPath)
        os.popen('cp proofOC/actions/main.yml ' + self.workflowPath)
      except Exception:
        self.logger.exception("Unable to create worklows directory.")
        raise RepositoryConfigurationException("Unable to create workflows directory.")

    
    # Create actions folder to copy the scripts into
    if not os.path.exists(self.actionsPath):
      try:
        os.makedirs(self.actionsPath)
        os.popen('cp proofOC/actions/actionScript.py ' + self.actionsPath)
        os.popen('cp proofOC/actions/TraverseSite.py ' + self.actionsPath)
        os.popen('cp proofOC/actions/requirements.txt ' + self.actionsPath)
      except Exception:
        self.logger.exception("Unable to create actions directory.")
        raise RepositoryConfigurationException("Unable to create actions directory.")



    
    


  def addFile(self, fileName):
    """
    Stages a file for commit
    """
    self.repo.index.add(fileName)

  def pushData(self):
    """
    Pushes the local repo up to GitHub
    """
    self.repo.index.commit('Update bookings.')
    try:
      self.repo.remotes.origin.push()
    except Exception:
      self.logger.exception("Unable to push to the remote repository")
      raise RepositoryConfigurationException("Unable to push to the remote repository")
