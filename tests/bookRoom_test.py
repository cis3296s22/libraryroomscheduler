
from proofOC.bookRoom import configurePath
import os
import sys


def test_configurePath():
    assert configurePath(os.path.dirname(sys.executable)) == "local_repo"

def test_configurePathexe():
    assert configurePath("Users/ccho/Developer/libraryroomscheduler/exe/dist") == "Users/ccho/Developer/libraryroomscheduler/exe/dist/../../local_repo"
