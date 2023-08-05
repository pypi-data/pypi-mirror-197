from ck8s.helpers import ok, error, readKeyFromCommonConfig, title, subtitle, readKeyFromSecretsFile, warning
from ck8s.action import Action

from kubernetes import client, config

import requests
import jq

class TestAction(Action) :

  def __init__(self, args):
      super().__init__()
      self.args = args
      self.parseComponent()

  def parseComponent(self):
    cluster = self.args['cluster']
    component = self.args['component']

    config.load_kube_config(config_file="{}/.state/kube_config_{}.yaml".format(self.CK8S_CONFIG_PATH, cluster))
    appsV1 = client.AppsV1Api()
    print(self.args)
    if component is None :
      error("Please choose a component to test, list of valid components is : base, opensearch or ingress")
    elif component == 'base':
      title('Running base tests ...')
    elif component == 'opensearch':
      title('Running opensearch tests ... ')
      if self.args['cluster_health']:
        subtitle('Checking Opensearch cluster health ..')
        adminPassword = readKeyFromSecretsFile('.opensearch.adminPassword')
        opsDomain = readKeyFromCommonConfig('.global.opsDomain')

        res = requests.get("https://opensearch.{}/_cluster/health".format(opsDomain), auth=('admin', adminPassword), verify=False)
        if res.status_code != 200 :
          raise Exception(res.reason)
        else:
          cluster_status = jq.compile('.status').input(text=res.text).first()
          print(cluster_status)
          if cluster_status != "green":
            warning('Opensearch is not healthy')
          else :
            ok('[SUCCESS] Opensearch cluster is healthy')

    elif component == 'ingress':
      title('Running ingress tests')
      if self.args['health'] == True:
        subtitle('Checking ingress health ..')
        ret = appsV1.read_namespaced_daemon_set_status("ingress-nginx-controller", "ingress-nginx")
        if ret.status.number_ready != ret.status.desired_number_scheduled:
          error('[ERROR] Some ingress-nginx pods are not ready.')
        else :
          ok('[SUCCESS] All nginx pods are ready')


