import yaml
from pathlib import Path
from typing import Dict, Optional
from crewai import Crew, Agent, Task, Process

class CrewManager:
    def __init__(self, configs_dir: str = "configs"):
        """Initialize the CrewManager with configurations directory."""
        print("Initializing CrewManager with configs directory:", configs_dir)
        self.configs_dir = Path(configs_dir)
        self.crews: Dict[str, dict] = self._load_crew_configs()

    def _load_crew_configs(self) -> Dict[str, dict]:
        """Load all crew configurations from subdirectories in the configs directory."""
        print("Loading crew configurations from:", self.configs_dir)
        configs = {}
        if not self.configs_dir.exists():
            raise FileNotFoundError(f"Configs directory '{self.configs_dir}' not found.")

        # Iterate through subdirectories (e.g., crew1, crew2)
        for crew_folder in self.configs_dir.iterdir():
            if crew_folder.is_dir():
                config_file = crew_folder / f"{crew_folder.name}_config.yaml"
                if config_file.exists():
                    try:
                        with open(config_file, 'r') as f:
                            config = yaml.safe_load(f)
                            if 'crew_id' in config:
                                configs[config['crew_id']] = config
                    except yaml.YAMLError as e:
                        print(f"Error loading YAML file {config_file}: {e}")
                        
        # print(configs)
        return configs

    def get_crew(self, crew_id: str) -> Optional[Crew]:
        """Get a crew instance based on the crew_id."""
        print("Getting crew with ID:", crew_id)
        if crew_id not in self.crews:
            return None
        config = self.crews[crew_id]
        agents = []
        tasks = []

        # Create agents from configuration
        for agent_config in config.get('agents', []):
            agent = Agent(
                name=agent_config['name'],
                role=agent_config['role'],
                goal=agent_config['goal'],
                backstory=agent_config.get('backstory', ''),
                verbose=True
            )
            agents.append(agent)

        # Create tasks from configuration
        for task_config in config.get('tasks', []):
            task = Task(
                description=task_config['description']
            )
            tasks.append(task)

        # Create and return the crew
        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )

    def list_crews(self) -> list:
        """Return a list of available crew configurations."""
        return list(self.crews.keys())