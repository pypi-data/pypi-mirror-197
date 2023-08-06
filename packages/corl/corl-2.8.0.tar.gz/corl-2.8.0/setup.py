# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['corl',
 'corl.agents',
 'corl.dones',
 'corl.dones.docking_1d',
 'corl.dones.pong',
 'corl.environment',
 'corl.environment.utils',
 'corl.episode_parameter_providers',
 'corl.evaluation',
 'corl.evaluation.launchers',
 'corl.evaluation.loader',
 'corl.evaluation.metrics',
 'corl.evaluation.metrics.aggregators',
 'corl.evaluation.metrics.generators',
 'corl.evaluation.metrics.generators.meta',
 'corl.evaluation.metrics.types',
 'corl.evaluation.metrics.types.nonterminals',
 'corl.evaluation.metrics.types.terminals',
 'corl.evaluation.recording',
 'corl.evaluation.runners',
 'corl.evaluation.runners.section_factories',
 'corl.evaluation.runners.section_factories.engine',
 'corl.evaluation.runners.section_factories.engine.rllib',
 'corl.evaluation.runners.section_factories.plugins',
 'corl.evaluation.runners.section_factories.test_cases',
 'corl.evaluation.util',
 'corl.evaluation.visualization',
 'corl.experiments',
 'corl.experiments.rllib_utils',
 'corl.glues',
 'corl.glues.common',
 'corl.glues.controller_wrappers',
 'corl.libraries',
 'corl.models',
 'corl.parsers',
 'corl.parts',
 'corl.policies',
 'corl.rewards',
 'corl.rewards.docking_1d',
 'corl.simulators',
 'corl.simulators.docking_1d',
 'corl.simulators.openai_gym',
 'corl.simulators.pong',
 'corl.simulators.six_dof',
 'docs']

package_data = \
{'': ['*'],
 'corl': ['.pytest_cache/*', '.pytest_cache/v/cache/*'],
 'docs': ['css/*', 'evaluation_framework/*', 'tasks/*']}

install_requires = \
['GitPython==3.1.27',
 'deepmerge==0.3.0',
 'flatten-dict==0.4.1',
 'gym==0.23.0',
 'h5py>=3.7',
 'jsonargparse[argcomplete,signatures]==3.19.4',
 'numpy-ringbuffer>=0.2.2,<0.3.0',
 'numpy<1.24.0',
 'pydantic>=1.9.2,<2.0.0',
 'pygame>=2.1.2,<3.0.0',
 'pygifsicle>=1.0.7,<2.0.0',
 'ray[all]==2.2.0',
 'tensorboard>=2.10,<3.0',
 'tensorflow-probability==0.19.0',
 'tensorflow==2.11.0']

extras_require = \
{':python_version < "3.9"': ['graphlib-backport>=1.0.3,<2.0.0']}

entry_points = \
{'console_scripts': ['corl_eval_launch = '
                     'corl.evaluation.launchers.launch_evaluate:pre_main',
                     'corl_eval_metrics = '
                     'corl.evaluation.launchers.launch_generate_metrics:pre_main',
                     'corl_eval_pipeline = '
                     'corl.evaluation.launchers.launch_pipeline:main',
                     'corl_eval_storage = '
                     'corl.evaluation.launchers.launch_storage:pre_main',
                     'corl_eval_visualize = '
                     'corl.evaluation.launchers.launch_visualize:pre_main',
                     'corl_train = corl.train_rl:main']}

setup_kwargs = {
    'name': 'corl',
    'version': '2.8.0',
    'description': 'Core ACT3 Reinforcement Learning (RL) Library - Core framework and base implementations of common things such as controllers, glues, observes, sensors, evaluation, and ect',
    'long_description': "**The following Site/Repository is currently under construction. We are still porting items and updating instructions for github site/CICD.**\n\n# Autonomy Capability Team (ACT3) Home Page https://www.afrl.af.mil/ACT3/\n\nThe Air Force Research Laboratory’s (AFRL) Autonomy Capability Team (ACT3) is an AI Special Operations organization whose mission is to Operationalize AI at Scale for the Air Force. Commissioned by the AFRL Commander, ACT3 leverages an innovative ‘start-up’ business model as an alternative approach to the traditional AFRL Technical Directorate R&D model by combining the blue sky vision of an academic institution; the flexibility of an AI startup; and the discipline of a production development company. ACT3 integrates the world’s best under one roof. The goal of the ACT3 business model is to define the shortest path to successful transition of solutions using AFRL’s internal expertise and collaborations with the best academic and commercial AI researchers in the world. Successful implementation may mean new technology or new implementation of existing technology.\n\n# ACT3 RL Core\n\n***Core act3 reinforcement learning library*** - The Core Reinforcement Learning library is intended to enable scalable deep reinforcement learning experimentation in a manner extensible to new simulations and new ways for the learning agents to interact with them. The hope is that this makes RL research easier by removing lock-in to particular simulations.\n\nThe work is released under the follow APRS approval.\n\n|    Date    |     Release Number     | Description                                                      |\n| :--------: | :--------------------: | :--------------------------------------------------------------- |\n| 2022-05-20 |     AFRL-2022-2455     | Initial release of [ACT3 CoRL](https://github.com/act3-ace/CoRL) |\n| 2023-03-02 | APRS-RYZ-2023-01-00006 | Second release of [ACT3 CoRL](https://github.com/act3-ace/CoRL)  |\n\nRelated Publications:\n- https://breakingdefense.com/2023/01/inside-the-special-f-16-the-air-force-is-using-to-test-out-ai/\n- https://www.wpafb.af.mil/News/Article-Display/Article/3244878/afrl-aftc-collaborate-on-future-technology-via-weeklong-autonomy-summit/\n- https://aerospaceamerica.aiaa.org/year-in-review/demonstrating-and-testing-artificial-intelligence-applications-in-aerospace/\n\nDocumentation \n- https://act3-ace.github.io/CoRL/\n\n![image](https://user-images.githubusercontent.com/102970755/193952349-108c1acd-ce58-4908-a043-28c2a53c85fa.png)\n\n- Framework Overview - Hyper configurable environment enabling rapid exploration and integration pathways\n   - **A framework for developing highly-configurable environments and agents**\n     - Develop core components in python\n     - Configure experiments/agents in json/yml\n     - Provides tooling to help validate configuration files and give useful feedback when files are misconfigured\n   - **Designed with integration in mind**\n   - **Dramatically reduce development time to put trained agents into an integration or using a different simulation** \n     - Can work with any training framework\n     - Currently limited to Ray/RLLIB due to multi-agent requirement\n   - **Environment pre-written, users implement plugins**\n     - Simulator\n     - Platforms & Platform Parts\n     - Glues\n     - Rewards\n     - Dones\n- Validators - **Configuration guarantees for enabling validation of user configuration going into the major components** \n  - All major CoRL python components have a validator\n  - Validators are python dataclasses implemented through the pydantic library\n  - Validators check and validate user configuration arguments going into the major components\n    - If a component successfully initializes, the validators guarantee the developer that the data listed in the validator is available to them\n    - If a component doesn’t initialize, a nice helpful error message is automatically produced by pydantic\n  - Adds a pseudo static typing to python classes\n- Episode Parameter Provider (EPP) - **Domain Randomization & Curriculum Learning at Environment, Platform, and Agent based on training**\n  - An important tool for RL environments is the ability to randomize as much as possible\n    - Starting conditions / goal location / etc.\n    - This leads to more general agents who are more robust to noise when solving a task\n  - Another tool sometimes used in RL is curriculum learning (CL)\n    - Starting from an easier problem and gradually making the environment match the required specifications can significantly speed up training\n  - CoRL Agents and the environment all have an epp, which provides simulator or user defined parameters to be used during a specific episode\n    - Simulator classes know what parameters they expect to setup an episode\n    - Configuration parameters to the various functors can all be provided from an EPP\n  - An EPP can also update parameters over the course of training\n    - Make a goal parameter harder based on the agents win rate\n    - Open the environment up to wider bounds once the agent initially starts to learn\n- Simulator Class - **Extensible interface for transitioning between Dubins and other simulator backends**\n  - Responsible for setting up the world for a agents to manipulate\n    - Setting up and configuring the simulation \n    - Creating the simulation platforms\n    - Placing those platforms in the world\n  - Responsible for knowing how to advance the simulation when requested\n    - The simulation returns a simulation state when reset or advanced that rewards or done conditions can use\n    - This state contains at least both the time and the list of simulation platforms\n    - Responsible for saving any information about the current training episode\n      - Saving video/logs\n- Simulator Platforms + parts - **Extensible base interface for parts to be added to planforms with an integration focus.**\n  - Simulation platforms represent some object that can be manipulated in the simulation\n    - Car/plane/robot/etc.\n  - Have a config file to allow modes of configuration\n  - Each platform has a set of parts attached to it\n  - Parts take simulation specific code and wrap it in an interface that allows agents to read from and write to them\n    - Parts do nothing unless a user configures a connection between the agent and a part using a glue (to be explained)\n   - Parts could include things such as a throttle, a game button, a steering wheel, etc.\n   - Parts are registered to a simulator using a string `Sensor_Throttle`, `Controller_Throttle`, etc.\n- Glues - **Connecting layers to allow exposing observable state to rewards, termination/goal criteria, and agents**\n  - A stateful functor\n  - Responsible for producing actions and observations for the agent\n  - May directly read/write to parts or other glues\n  - Glues reading/writing to each other is called “wrapping”\n  - Glues implement the composable and reusable behavior useful for developers\n    - Common glues turn any sensor part into an obs and apply actions to any controller part\n    - Wrapper glues can implement behaviors such as framestacking, delta actions\n  - May not directly read from the simulation, only interface through parts\x0b\n- Rewards, Dones (Goal & Termination) - **Composable functors common interface for sharing rewards and termination criteria in a stateful manner**\n  - Composable state functors\n  - Rewards generate the current step reward for the agent\n  - Dones evaluate if the episode should stop on the current timestep\n    - These done’s can be triggered for either success or failure\n  - Both Done and Reward Functors can view the entire simulation state to reward agents\n  - Done conditions typically add to the state when they trigger to signify what type of Done they are\n    - WIN/LOSE/DRAW\n    - Rewards are processed after Done conditions during an\x0bupdate, so rewards can read these labels\n  - There can be an arbitrary number of reward or done functors for an agent\n- Agent + Experiment Class\n   - Agent Class\n      - Responsible for holding all of the Done/Reward/Glue functors for a given agent\n      - Can be many agent classes per platform\n         - When one agent class on a platform reaches a done, all on that platform do\n      - Different subclasses may process information in different ways or do different things\n   - Experiment Class\n      - Responsible for setting up an experiment and running it\n      - Configures and creates the environment\n      - Creates and configures the agent classes\n      - Use of this class allows for any arbitrary RL training framework to be used as the backend for training\n- CoRL Integration and Simulator Swapping\n   - In CoRL all simulation specific components must be registered and retrieved from a plug-in library\n   - As long as a specific simulator has all of the parts registered to it that an agent needs, CoRL can swap the simulator and parts out from under an agent seamlessly\n   - As long as the parts for the two simulators have the same properties (in terms of sensed value bounds or controller inputs) there is no difference to the agent between the two and the regular environment can be used for integration\n   - Besides integration this also allows for cross simulation evaluation or training of an agent to be resumed in another simulator\n\n\n## Benifits\n- **CoRL helps make RL environment development significantly easier**\n- **CoRL provides hyper configurable environments/agents and experiments**\n- **Instead of a new file every time a new observation is added, now just add a few lines of config**\n- **Makes it possible to reuse glues/dones/rewards between different tasks if they are general**\n- **Provides tools to use both domain randomization and curriculum learning through EPP**\n- **An integration first focus means that integrating agents to the real world or different simulators is significantly easier**\n\n\n## Install\n### Install the source - Miniconda - local host:\n\n- [Miniconda Install Instruction](https://docs.conda.io/en/latest/miniconda.html)\n\n```bash\n# Create a virtual environment to install/run code\nconda create -n CoRL python==3.10.4 \n# Activate the virtual environment\nconda activate CoRL\n# install poetry\npip install poetry\n# Install the CoRL dependencies\npoetry install\n# Pre-commit setup\npre-commit install\n```\n\n### How to install pip package\n\n## Build\n\n### How to build the wheel file\n\nThe following project supports building python packages via `Poetry`. \n\n```bash\n# Create a virtual environment to install/run code\nconda create -n CoRL python==3.10.4 \n# Activate the virtual environment\nconda activate CoRL\n# install poetry\npip install poetry\n# Build the CoRL package\npoetry build\n```\n\n### How to build the documentations - Local\n\nThe follow project is setup to use [MKDOCS](https://www.mkdocs.org/) which is a fast, simple and downright gorgeous static site generator that's geared towards building project documentation. Documentation source files are written in Markdown, and configured with a single YAML configuration file.\n\nTo build the documentation:\n```\nmkdocs build\n```\n\nTo serve the documentation:\n```\nmkdocs serve\n```\n\n## How to build the Docker containers\n\nThe following project support development via Docker containers in VSCode. This is not strictly required but does provide the mode conveniet way to get started. ***Note:*** fuller documentation is available in the documentation folder or online docs. \n\n- ***Setup the user env file:*** in code directory run the following script  --> `./scripts/setup_env_docker.sh`\n- ***Build the Docker containers using compose:*** run the following command \n  - GITHUB --> `docker-compose -f docker-compose-github.yml build`\n  - ACT3 --> `docker-compose -f docker-compose.yml build`\n\n### Docker-Compose Utilities\n\n#### Test UTILITIES with DOCKER\n  \n- ***docs:*** run the following command\n  - GITHUB --> `docker-compose -f docker-compose-github.yml up docs`\n  - ACT3 --> `docker-compose -f docker-compose.yml up docs`\n- ***pre-commit:*** run the following command\n  - GITHUB --> `docker-compose -f docker-compose-github.yml up pre-commit`\n  - ACT3 --> `docker-compose -f docker-compose.yml up pre-commit`\n- ***pytest:*** run the following command\n  - GITHUB --> `docker-compose -f docker-compose-github.yml up pytest`\n  - ACT3 --> `docker-compose -f docker-compose.yml up pytest`\n#### POETRY UTILITIES with DOCKER\n\n- ***Generate Poetry Lock File:*** run the following command\n  - GITHUB --> `docker-compose -f docker-compose-github.yml up poetry-lock`\n  - ACT3 --> `docker-compose -f docker-compose.yml up poetry-lock`\n- ***Generate Poetry Update Lock File:*** run the following command\n  - GITHUB --> `docker-compose -f docker-compose-github.yml up poetry-update`\n  - ACT3 --> `docker-compose -f docker-compose.yml up poetry-update`\n- ***Generate Poetry Create Dist:*** run the following command\n  - GITHUB --> `docker-compose -f docker-compose-github.yml up poetry-build-dist`\n  - ACT3 --> `docker-compose -f docker-compose.yml up poetry-build-dist`\n## Running base examples\n\n```bash\n    python -m corl.train_rl --cfg config/experiments/cartpole_v1.yml\n```\n\n# Initial Contributors\n\nInitial contributors include scientists and engineers associated with the [Air Force Research Laboratory (AFRL)](https://www.afrl.af.mil/), [Autonomy Capability Team 3 (ACT3)](https://www.afrl.af.mil/ACT3/), and the [Aerospace Systems Directorate (RQ)](https://www.afrl.af.mil/RQ/):\n\n- Autonomous Air Combat Operations (AACO) Team\n  - Terry Wilson(PM/PI)\n  - Karl Salva (System Integration)\n  - James Patrick (Modeling & Simulation)\n  - Benjamin Heiner (AI Behavior Training Lead)\n  - Training Team\n    - Cameron Long (ML Training)\n    - Steve Fierro (ML Training / System Integration)\n    - Brian Stieber (ML Training)\n    - Joshua Blackburn (ML Training / System Integration)\n    - Madison Blake (ML Infrastructure and Evaluation)\n- Safe Autonomy\n  - Kerianne Hobbs\n  - John McCarroll\n  - Umberto Ravaioli\n  - Jamie Cunningham\n  - Kyle Dunlap\n  - Nate Hamilton\n- Fundemental Research\n  - Jared Culbertson\n  - Hamilton Clouse\n  - Justin Merrick\n  - Ian Cannon\n  - Ian Leong\n  - Vardaan Gangal\n\n# Designation Indicator\n\n- Controlled by: Air Force Research Laboratory (AFRL)\n- Controlled by: AFRL Autonomy Capability Team (ACT3)\n- LDC/Distribution Statement: DIST-A\n- POCs:\n    - terry.wilson.11@us.af.mil (AFRL ACT3)\n    - bejamin.heiner@us.af.mil (AFRL ACT3)\n    - kerianne.hobbs@us.af.mil (AFRL ACT3)\n\n    \n# Notices and Warnings\n\n\n# Citing CORL\n\nIf you use CORL in your work, please use the following bibtex\n\n```bibtex\n@inproceedings{\n  title={{CoRL}: Environment Creation and Management Focused on System Integration},\n  author={Justin D. Merrick, Benjamin K. Heiner, Cameron Long, Brian Stieber, Steve Fierro, Vardaan Gangal, Madison Blake, Joshua Blackburn},\n  year={2023},\n  url={https://arxiv.org/abs/2303.02182}\n}\n```\n\n**White Paper ->** CoRL: Environment Creation and Management Focused on System Integration\n\n**Authors ->** Justin D. Merrick, Benjamin K. Heiner, Cameron Long, Brian Stieber, Steve Fierro, Vardaan Gangal, Madison Blake, Joshua Blackburn\n\n**Abstract ->** Existing reinforcement learning environment libraries use monolithic environment classes, provide shallow methods for altering agent observation and action spaces, and/or are tied to a specific simulation environment. The Core Reinforcement Learning library (CoRL) is a modular, composable, and hyper-configurable environment creation tool. It allows minute control over agent observations, rewards, and done conditions through the use of easy-to-read configuration files, pydantic validators, and a functor design pattern. Using integration pathways allows agents to be quickly implemented in new simulation environments, encourages rapid exploration, and enables transition of knowledge from low-fidelity to high-fidelity simulations. Natively multi-agent design and integration with Ray/RLLib (Liang et al., 2018) at release allow for easy scalability of agent complexity and computing power. The code is publicly released and available at this https URL.\n\n",
    'author': 'Benjamin K Heiner',
    'author_email': 'benjamin.heiner@us.af.mil',
    'maintainer': 'Benjamin K Heiner',
    'maintainer_email': 'benjamin.heiner@us.af.mil',
    'url': 'https://github.com/act3-ace/CoRL',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
