import os
from ck8s.helpers import ok, error, title

class Action(object):
  def __init__(self):
    self.CK8S_PGP_FP=os.getenv('CK8S_PGP_FP')
    self.CK8S_DEVBOX_VERSION=os.getenv('CK8S_DEVBOX_VERSION','a0.26.1-k2.20.0.2')
    self.CK8S_KUBESPRAY_REPOSITORY_PATH=os.getenv('CK8S_KUBESPRAY_REPOSITORY_PATH','/home/neo/Desktop/Elastisys/compliantkubernetes-kubespray')
    self.CK8S_CLOUD_PROVIDER=os.getenv('CK8S_CLOUD_PROVIDER','exoscale')
    self.CK8S_FLAVOR=os.getenv('CK8S_FLAVOR','dev')
    self.CK8S_OPS_REPOSITORY_PATH=os.getenv('CK8S_OPS_REPOSITORY_PATH','/home/neo/Desktop/Elastisys/ops-repo')
    self.CK8S_CONFIG_PATH=os.getenv('CK8S_CONFIG_PATH','/home/neo/Desktop/Elastisys/exo-env')
    self.CK8S_ENVIRONMENT_NAME=os.getenv('CK8S_ENVIRONMENT_NAME','aeddafali-ck8s-cluster')
 