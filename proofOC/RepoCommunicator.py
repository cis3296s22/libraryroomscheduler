import logging
import git
import os



def remoteRepoConfigured(repoPath: str):
  """
  Determines if we've saved repo configuration before and returns the remote URL if so

  . . .

  Parameters
  ----------
  repoPath: str
    The filepath of the local repo

  Returns
  ----------
    A string if the remote URL if found, or an empty string otherwise
  """
  if os.path.exists(f"{repoPath}/remoteURL.txt"):
    with open(f"{repoPath}/remoteURL.txt", "r") as f:
      return f.readline().rstrip()
  return ""

class RepositoryConfigurationException(Exception):
  """
  A custom exception used with the RepoCommunicator class. 
  Used to send more specific error messages back to the caller where things failed.
  """
  pass

class RepoCommunicator:
  """
  A class to represent our git repo as an object in the application
  
  . . .

  Attributes
  ----------
  remoteRepoUrl: str
    The git URL of the remote repository
  localPath: str
    The local system path needed to access the repo
  workflowPath: str
    The system path for Github workflows
  actionsPath: str
    The system path for Github actions
  logger: Logger
    A logging object to log events

  Methods
  ----------
  addFile(fileName: str)
    Stages a file for commit

  pushData()
    Pushes the local repo up to GitHub 
  """

  def __init__(self, remoteRepoUrl: str, localPath: str):
    """
    Instantiates the local repository to comminucate with GitHub.
    If the local repo has not been created, it will create one along with the necessary files.

    . . .

    Parameters
    ----------
      remoteRepoUrl: str
        The git URL of the remote repository
      localPath: str
        The local system path needed to access the repo
    """
    self.remoteRepoUrl = remoteRepoUrl
    self.localPath = localPath
    self.workflowPath = f"{localPath}/.github/workflows"
    self.actionsPath = f"{localPath}/scripts"
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

        except:
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
      except:
        self.logger.exception("Unable to create workflows directory.")
        raise RepositoryConfigurationException("Unable to create workflows directory.")

    
    # Create actions folder to copy the scripts into
    if not os.path.exists(self.actionsPath):
      try:
        os.makedirs(self.actionsPath)
      except:
        self.logger.exception("Unable to create actions directory.")
        raise RepositoryConfigurationException("Unable to create actions directory.")

    # always copy the latest files
    try:
      os.popen(f'cp {self.localPath}/../proofOC/actions/main.yml {self.workflowPath}')
      os.popen(f'cp {self.localPath}/../proofOC/actions/actionScript.py {self.actionsPath}')
      os.popen(f'cp {self.localPath}/../proofOC/actions/TraverseSite.py {self.actionsPath}')
      os.popen(f'cp {self.localPath}/../proofOC/actions/requirements.txt {self.actionsPath}')

    except:
      self.logger.exception("Error copying github action files to local repository")
      raise RepositoryConfigurationException("Error creating github action files. See app.log for more details")

    self.logger.debug("Repo created!")


  

  def addFile(self, fileName):
    """
    Stages a file for commit

    . . .

    Parameters
    ----------
    fileName: str
      The date of the file being added to the staged commit

    Returns
    ----------
    None
    """
    self.repo.index.add(fileName)

  def pushData(self):
    """
    Pushes the local repo up to GitHub

    . . .

    Parameters
    ----------
    None

    Returns
    ----------
    None
  
    """
    try:
      self.repo.index.commit('Update bookings.')
    except Exception:
      self.logger.exception("Unable to commit to the repository")
      raise RepositoryConfigurationException("Unable to commit to the repository")
    try:
      self.repo.remotes.origin.push()
    except Exception:
      self.logger.exception("Unable to push to the remote repository")
      raise RepositoryConfigurationException("Unable to push to the remote repository")
