import argparse
from ck8s.testAction import TestAction

def create_parser():
  parser = argparse.ArgumentParser(
    description="""
    """,
    formatter_class=argparse.RawDescriptionHelpFormatter
  )

  sub_parsers = parser.add_subparsers(dest='command')

  init_parser = sub_parsers.add_parser('init', help='Initialize the config path')
  init_parser.add_argument("--generate-new-secret", help="Generate a new secret", action="store_true", default=False)

  bootstrap_parser = sub_parsers.add_parser('bootstrap', help='Bootstrap the cluster')
  bootstrap_parser.add_argument('cluster', default='sc', const='sc', nargs='?', choices=['sc', 'wc'], help='Target cluster  (default: %(default)s)')

  apps_parser = sub_parsers.add_parser('apps', help='Deploy the applications')
  apps_parser.add_argument('cluster', default='sc', const='sc', nargs='?', choices=['sc', 'wc'], help='Target cluster  (default: %(default)s)')
  apps_parser.add_argument("--sync", help="Sync", action="store_true", default=False)
  apps_parser.add_argument("--skip-template-validate", help="Skip template validate", action="store_true", default=False)

  apply_parser = sub_parsers.add_parser('apply', help='bootstrap and apps')
  apply_parser.add_argument('cluster', default='sc', const='sc', nargs='?', choices=['sc', 'wc'], help='Target cluster  (default: %(default)s)')
  apply_parser.add_argument("--sync", help="Sync", action="store_true", default=False)
  apply_parser.add_argument("--skip-template-validate", help="Skip template validate", action="store_true", default=False)

  test_parser = sub_parsers.add_parser('test', help='Test the applications')
  test_parser.add_argument('cluster', default='sc', const='sc', nargs='?', choices=['sc', 'wc'], help='Target cluster  (default: %(default)s)')
  test_component_parser = test_parser.add_subparsers(dest='component')
  test_base_parser = test_component_parser.add_parser('base', help='base tests')
  test_opensearch_parser = test_component_parser.add_parser('opensearch', help='Opensearch tests')
  test_opensearch_parser.add_argument('--cluster-health', help="Get cluster Health", action="store_true", default=False)
  test_opensearch_parser.add_argument('--snapshot-status', help="Check snapshot status", action="store_true", default=False)
  test_ingress_parser = test_component_parser.add_parser('ingress', help='ingress tests')
  test_ingress_parser.add_argument('--health', help="Check ingress health", action="store_true", default=False)

  return parser

def main():
  parser = create_parser()
  args = vars(parser.parse_args())
  
  if args['command'] == 'init':
    pass
  elif args['command'] == 'apps':
    pass
  elif args['command'] == 'apply':
    pass
  elif args['command'] == 'test':
    testAction = TestAction(args)


if __name__== "__main__":
  parser = create_parser()
  args = vars(parser.parse_args())
  # print(args)
  if args['command'] == 'init':
    pass
  elif args['command'] == 'apps':
    pass
  elif args['command'] == 'apply':
    pass
  elif args['command'] == 'test':
    testAction = TestAction(args)