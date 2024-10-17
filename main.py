from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://vectorshift-navy.vercel.app"],  # Replace with specific origins as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Define a Pydantic model for the request body
class PipelineData(BaseModel):
    nodes: List[Any]
    edges: List[Any]

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

@app.post('/pipelines/parse')
def parse_pipeline(pipeline: PipelineData):
    is_dag = check_if_dag(pipeline.nodes, pipeline.edges)
    return {"num_nodes": len(pipeline.nodes), "num_edges": len(pipeline.edges), "is_dag": is_dag}


def check_if_dag(nodes: List[Any], edges: List[Dict[str, Any]]) -> bool:
    adjacency_list = {node['id']: [] for node in nodes}
    print("adjacency_list", adjacency_list)

    # Build the adjacency list
    for edge in edges:
        adjacency_list[edge['source']].append(edge['target'])

    visited = set()
    recursion_stack = set()

    def dfs(node):
        if node in recursion_stack:
            return True  # Cycle detected
        if node in visited:
            return False  # Already processed

        # Mark the node as visited and add to recursion stack
        visited.add(node)
        recursion_stack.add(node)

        # Visit all the neighbors
        for neighbor in adjacency_list[node]:
            if dfs(neighbor):
                return True

        # Remove from recursion stack
        recursion_stack.remove(node)
        return False  # No cycle found

    # Check for cycles in the graph
    for node in nodes:
        if dfs(node['id']):
            return False  # Graph is not a DAG

    return True  # Graph is a DAG
