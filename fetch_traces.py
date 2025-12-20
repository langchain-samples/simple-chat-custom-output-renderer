#!/usr/bin/env python3
"""
Fetch traces from LangSmith to analyze data structure
"""

import os
import json
from langsmith import Client

def fetch_traces(project_name=None, limit=5):
    """
    Fetch recent traces from LangSmith

    Args:
        project_name: Name of the LangSmith project (optional)
        limit: Number of traces to fetch
    """
    # Initialize LangSmith client
    # It will use LANGSMITH_API_KEY from environment
    client = Client()

    print(f"🔍 Fetching traces from LangSmith...")
    print(f"{'='*60}")

    # List all projects first
    print("\n📁 Available Projects:")
    try:
        projects = list(client.list_projects())
        if not projects:
            print("No projects found.")
            return

        for i, project in enumerate(projects[:10], 1):
            print(f"{i}. {project.name} (ID: {project.id})")

        # Use specified project or default to first one
        if project_name:
            target_project = next((p for p in projects if p.name == project_name), None)
            if not target_project:
                print(f"\n❌ Project '{project_name}' not found. Using first project instead.")
                target_project = projects[0]
        else:
            target_project = projects[0]

        print(f"\n🎯 Using project: {target_project.name}")
        print(f"{'='*60}")

    except Exception as e:
        print(f"Error listing projects: {e}")
        return

    # Fetch runs from the project
    try:
        runs = list(client.list_runs(
            project_name=target_project.name,
            limit=limit,
            is_root=True  # Only get root runs, not nested ones
        ))

        if not runs:
            print(f"\n❌ No runs found in project '{target_project.name}'")
            return

        print(f"\n✅ Found {len(runs)} runs\n")

        # Save traces to file for analysis
        traces_data = []

        for i, run in enumerate(runs, 1):
            print(f"\n{'─'*60}")
            print(f"Run #{i}: {run.name}")
            print(f"{'─'*60}")
            print(f"ID: {run.id}")
            print(f"Status: {run.status}")
            print(f"Run Type: {run.run_type}")
            print(f"Start Time: {run.start_time}")
            print(f"End Time: {run.end_time}")

            # Print inputs
            if run.inputs:
                print(f"\n📥 Inputs:")
                print(json.dumps(run.inputs, indent=2))

            # Print outputs
            if run.outputs:
                print(f"\n📤 Outputs:")
                print(json.dumps(run.outputs, indent=2))

            # Print error if any
            if run.error:
                print(f"\n❌ Error:")
                print(run.error)

            # Collect data for saving
            trace_data = {
                "id": str(run.id),
                "name": run.name,
                "run_type": run.run_type,
                "status": run.status,
                "inputs": run.inputs,
                "outputs": run.outputs,
                "error": run.error,
                "start_time": str(run.start_time) if run.start_time else None,
                "end_time": str(run.end_time) if run.end_time else None,
                "metadata": run.extra.get("metadata") if run.extra else None,
            }
            traces_data.append(trace_data)

        # Save to file
        output_file = "sample_traces.json"
        with open(output_file, 'w') as f:
            json.dump(traces_data, f, indent=2)

        print(f"\n{'='*60}")
        print(f"✅ Saved {len(traces_data)} traces to {output_file}")
        print(f"{'='*60}")

        return traces_data

    except Exception as e:
        print(f"\n❌ Error fetching runs: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    import sys

    # Check for API key
    if not os.getenv("LANGSMITH_API_KEY"):
        print("❌ LANGSMITH_API_KEY environment variable not set!")
        print("\nSet it with:")
        print("  export LANGSMITH_API_KEY='your-api-key'")
        sys.exit(1)

    # Get project name from command line if provided
    project_name = sys.argv[1] if len(sys.argv) > 1 else None
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    fetch_traces(project_name=project_name, limit=limit)
