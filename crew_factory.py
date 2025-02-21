from crewai import Agent, Crew, Process, Task

def create_crew(crew_config: dict) -> Crew:
    """Create a crew instance based on the provided YAML configuration."""

    agents = []
    tasks = []

    # Dynamically create agents
    for agent_config in crew_config.get('agents', []):
        agent = Agent(
            name=agent_config['name'],
            role=agent_config['role'],
            goal=agent_config['goal'],
            backstory=agent_config.get('backstory', ''),
            verbose=True
        )
        agents.append(agent)

    # Dynamically create tasks
    for task_config in crew_config.get('tasks', []):
     task = Task(
        description=task_config['description'],
        expected_output=task_config.get('expected_output', "Default Expected Output")  # Add this line
    )
    tasks.append(task)

    print(agents)
    print(tasks)
    # Create and return the crew
    return Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )