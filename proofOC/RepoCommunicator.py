import sys
import git
import os

def remoteRepoConfigured(repoPath: str):
  if os.path.exists(f"{repoPath}/remoteURL.txt"):
    with open(f"{repoPath}/remoteURL.txt", "r") as f:
      return f.readline().rstrip()
  return ""

class RepoCommunicator:

  def __init__(self, remoteRepoUrl: str, localPath: str):
    """
    Instantiates the local repository to comminucate with GitHub.
    If the local repo has not been created, it will create one.
    """
    self.remoteRepoUrl = remoteRepoUrl
    self.localPath = localPath

    if not os.path.exists(localPath):
    # path doesn't exist, create it
      os.mkdir(localPath)

    if os.path.exists(localPath) and os.path.isdir(localPath):
    # path exists and is a directory
      if len(os.listdir(localPath)):
      # it's not empty, set local to it
        self.repo = git.Repo(os.path.realpath(localPath))
        # if remote file doesn't exist, recreate it
        # TODO validate this with git remote instead of string passed in
        with open(f"{localPath}/remoteURL.txt", "w+") as f:
            f.write(remoteRepoUrl)
      else:
      # it's empty, clone into it
        try:
          self.repo = git.Repo.clone_from(remoteRepoUrl, localPath)
          with open(f"{localPath}/remoteURL.txt", "w+") as f:
            f.write(remoteRepoUrl)

        except Exception as e:
          sys.exit(f"An error occurred in cloning the repo:\n{e}")
    else:
    # path exists but is not a directory
    # this "shouldn't" trigger since the dir is hardcoded
      sys.exit("Please provide a directory for the local repository")


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
    self.repo.remotes.origin.push()