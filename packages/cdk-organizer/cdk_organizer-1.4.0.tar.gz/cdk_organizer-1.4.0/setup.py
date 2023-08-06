# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cdk_organizer',
 'cdk_organizer.aws',
 'cdk_organizer.decorators',
 'cdk_organizer.loaders',
 'cdk_organizer.miscellaneous',
 'cdk_organizer.miscellaneous.yaml_tags',
 'cdk_organizer.terraform']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'constructs>=10.1.49,<11.0.0',
 'dacite>=1.6.0,<2.0.0',
 'pyhumps>=3.7.2,<4.0.0']

extras_require = \
{'aws': ['aws-cdk-lib>=2.32.1,<3.0.0'], 'terraform': ['cdktf>=0.15.0,<0.16.0']}

setup_kwargs = {
    'name': 'cdk-organizer',
    'version': '1.4.0',
    'description': 'CDK Organizer',
    'long_description': '# CDK Organizer Python Library\n\nThis library contains the core features to handle CDK projects including:\n\n- Logging\n- Configuration Resolver\n- Stack Groups Loader\n- Naming Utils\n\nFull documentation: <https://cdk-organizer.github.io/>\n\n## Installation\n\n```bash\npip install cdk-organizer[terraform,aws]\n```\n\n### Extras\n\n- `terraform`: Include `cdktf` as a dependency.\n- `aws`: Include `aws-cdk-lib` as a dependency.\n\n### CDK Start Script\n\nThe content of the `app.py` file should be as follows:\n\n#### AWS CDK\n\n```python\nimport aws_cdk as cdk\nfrom cdk_organizer.miscellaneous.logging import setup_logging\nfrom cdk_organizer.stack_group import StackGroupLoader\n\napp = cdk.App()\nlogger = setup_logging(__name__, app.node.try_get_context("loglevel") or "INFO")\nloader = StackGroupLoader(app)\n\nloader.synth()\napp.synth()\n```\n\n#### CDK for Terraform\n\n```python\nfrom cdk_organizer.miscellaneous.logging import setup_logging\nfrom cdk_organizer.stack_group import StackGroupLoader\nfrom cdktf import App\n\napp = App()\nlogger = setup_logging(__name__, app.node.try_get_context("loglevel") or "INFO")\nloader = StackGroupLoader(app)\n\nloader.synth()\napp.synth()\n```\n\n## Context Variables\n\nThe following context variables are required to the CDK Organizer to work properly:\n\n- `env`\n- `region`\n\nThe variables can be set in the `cdk.json` file:\n\n```json\n{\n  ...\n  "context": {\n    ...\n    "env": "dev",\n    "region": "us-east-1"\n    ...\n  }\n  ...\n}\n```\n\nOr passed as arguments to the CDK CLI:\n\n```bash\ncdk synth --context env=dev --context region=us-east-1\n```\n\n> In the `cdktf` CLI the context variables cannot be passed as arguments, so they need to be set in the `cdk.json` file. <https://github.com/hashicorp/terraform-cdk/issues/2019>\n> The `env` variable can also be set as an environment variable `CDK_ENV`.\n\n## Project Structure\n\nTo apply the pattern purposed in this library for CDK projects, the following structure is required:\n\n```text\n.\n+-- cdk.json\n+-- app.py\n```\n\n### Stack Structure\n\nthe stack class needs to inherit from class `cdk_organizer.aws.stack.Stack` for AWS CDK and `cdk_organizer.terraform.stack.Stack` for Terraform CDK.\n\n#### AWS CDK\n\n```python\nfrom constructs import Construct\nfrom cdk_organizer.aws.stack import Stack\nfrom cdk_organizer.aws.stack_group import StackGroup\n\n\nclass MyStack(Stack):\n    def __init__(\n        self,\n        scope: Construct,\n        id: str,\n        stack_group: StackGroup,\n        **kwargs\n    ) -> None:\n        super().__init__(scope, id, stack_group, **kwargs)\n```\n\n#### Terraform CDK\n\n```python\nfrom constructs import Construct\nfrom cdk_organizer.terraform.stack import Stack\nfrom cdk_organizer.terraform.stack_group import StackGroup\n\n\nclass MyStack(Stack):\n    def __init__(\n        self,\n        scope: Construct,\n        id: str,\n        stack_group: StackGroup,\n        **kwargs\n    ) -> None:\n        super().__init__(scope, id, stack_group, **kwargs)\n```\n\n#### Using S3 Backend\n\nTo use S3 terraform backend, the following resources are required:\n\n- S3 Bucket\n- DynamoDB Table\n\nAdd the following object to the environment configuration file:\n\n```yaml\ns3_backend:\n  bucket: "<bucket-name>"\n  region: "<aws-region>"\n  dynamodb_table: "<dynamodb-table-name>"\n```\n\n### Stack Group Structure\n\nCreate a `stacks` folder in the root of the project and structure it as follows:\n\n```text\n.\n+-- cdk.json\n+-- app.py\n+-- stacks/\n| +-- <groupName>/\n|   +-- stacks.py\n```\n\nThe stack groups files follow this pattern:\n\n#### AWS CDK\n\n```python\nimport aws_cdk as cdk\nfrom dataclasses import dataclass\nfrom cdk_organizer.aws.stack_group import StackGroup\n\n@dataclass\nclass MyStackGroupConfig:\n    domain: str\n    ipv6: bool = True\n\n\nclass MyStackGroup(StackGroup[MyStackGroupConfig]):\n    def _load_stacks(self) -> None:\n        MyStack(\n            self.app,\n            self.get_stack_name(\'my-stack\'),\n            stack_group=self,\n            parameters=MyStackParameters(\n                domain=self.data.domain,\n                ipv6=self.data.ipv6\n            )\n        )\n```\n\n#### Terraform\n\n```python\nimport cdktf\nfrom dataclasses import dataclass\nfrom cdk_organizer.terraform.stack_group import StackGroup\n\n@dataclass\nclass MyStackGroupConfig:\n    domain: str\n    ipv6: bool = True\n\n\nclass MyStackGroup(StackGroup[MyStackGroupConfig]):\n    def _load_stacks(self) -> None:\n        MyStack(\n            self.app,\n            self.get_stack_name(\'my-stack\'),\n            stack_group=self,\n            parameters=MyStackParameters(\n                domain=self.data.domain,\n                ipv6=self.data.ipv6\n            )\n        )\n```\n\n#### Using Stack Attributes from Other Stack Groups\n\nIn some cases, you may want to use the attributes of another stack group. For example, refer the DNS Hosted Zone created by a shared stack group.\n\nTo resolve the group use the `self.resolve_group` function in the stack group class, like the example below:\n\n```python\nimport aws_cdk as cdk\nfrom dataclasses import dataclass\nfrom cdk_organizer.aws.stack_group import StackGroup\nfrom stacks.dns import DNSStackGroup\n\n@dataclass\nclass MyStackGroupConfig:\n    domain: str\n    ipv6: bool = True\n\n\nclass MyStackGroup(StackGroup[MyStackGroupConfig]):\n    def _load_stacks(self) -> None:\n        MyStack(\n            self.app,\n            self.get_stack_name(\'my-stack\'),\n            stack_group=self,\n            parameters=MyStackParameters(\n                domain=self.data.domain,\n                zone=self.resolve_group(DNSStackGroup).zone\n                ipv6=self.data.ipv6\n            )\n        )\n```\n\nThe function `get_stack_name` generates the stack name based on following pattern.\n\n**Pattern**: `{module_path}-{name}-{region}-{env}`\n\nConsider the following example:\n\n**module_path**: `myproject.myapp.www`\n**name**: `spa`\n**region**: `us-east-1`\n**env**: `dev`\n\nStack name will be:\n\n- `myproject-myapp-www-spa-us-east-1-dev`.\n\n### Config Structure\n\nCreate a `config` folder in the root of the project and structure it as follows:\n\n```text\n.\n+-- cdk.json\n+-- app.py\n+-- config/\n| +-- <env>/\n|   +-- config.yaml\n|   +-- <region>/\n|     +-- config.yaml\n|     +-- <groupName>/\n|         +-- config.yaml\n```\n\nThe first two levels are reserved to the environment name and the region name, the next levels needs to match the stack group structure.\n\nExample:\n\n```text\n.\n+-- cdk.json\n+-- app.py\n+-- config/\n| +-- config.yaml\n| +-- dev/\n|   +-- config.yaml\n|   +-- us-east-1/\n|     +-- config.yaml\n|     +-- app1/\n|       +-- config.yaml\n+-- stacks/\n| +-- app1/\n|   +-- stacks.py\n+-- templates/\n|   +-- stacks/\n```\n\n### Examples\n\n- [AWS CDK](https://github.com/cdk-organizer/cdk-organizer/tree/main/examples/python/aws-cdk)\n- [CDK for Terraform](https://github.com/cdk-organizer/cdk-organizer/tree/main/examples/python/cdktf)\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
