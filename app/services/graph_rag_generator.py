from collections import defaultdict
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def build_adjacency_list(graph: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[str]]:
    """Build an adjacency list from the graph edges."""
    adj = defaultdict(list)
    for edge in graph.get('edges', []):
        source = edge['source']
        target = edge['target']
        adj[source].append(target)
    return adj

def dfs_paths(adj: Dict[str, List[str]], start_node_id: str, max_depth: int = 3) -> List[List[str]]:
    """Depth-first search to find all paths up to a maximum depth."""
    paths = []

    def dfs(current_path: List[str], depth: int):
        if depth > max_depth:
            return
        paths.append(list(current_path))
        current_node = current_path[-1]
        for neighbor in adj.get(current_node, []):
            if neighbor not in current_path:  # Avoid cycles
                dfs(current_path + [neighbor], depth + 1)

    dfs([start_node_id], 0)
    return paths

def score_path(path: List[str], node_dict: Dict[str, Dict[str, Any]]) -> float:
    """Score a path by averaging the rerank_scores of nodes."""
    scores = [node_dict[node_id].get('rerank_score', 0.5) for node_id in path]
    return sum(scores) / len(scores) if scores else 0.0

def select_best_chain(graph: Dict[str, List[Dict[str, Any]]], top_k_start_nodes: int = 5, max_depth: int = 3) -> List[str]:
    """
    Select the best reasoning chain path from the graph based on rerank scores.
    """
    if not graph.get('nodes') or not graph.get('edges'):
        logger.warning("Empty graph provided to select_best_chain.")
        return []

    adj = build_adjacency_list(graph)
    node_dict = {node['id']: node for node in graph['nodes']}

    # Select top-k highest rerank_score nodes as starting points
    start_nodes = sorted(graph['nodes'], key=lambda x: x.get('rerank_score', 0), reverse=True)[:top_k_start_nodes]

    best_path = []
    best_score = -1.0

    for start_node in start_nodes:
        paths = dfs_paths(adj, start_node['id'], max_depth=max_depth)
        for path in paths:
            if len(path) > 1:  # Must be at least a chain, not a single node
                path_score = score_path(path, node_dict)
                if path_score > best_score:
                    best_score = path_score
                    best_path = path

    if not best_path:
        logger.warning("No valid reasoning chain found. Consider adjusting top_k_start_nodes or max_depth.")

    return best_path

def build_prompt_from_chain(path: List[str], graph: Dict[str, List[Dict[str, Any]]], user_query: str) -> str:
    """Build a prompt for LLM from a selected reasoning chain."""
    node_dict = {node['id']: node for node in graph['nodes']}
    context_parts = []

    for node_id in path:
        node = node_dict.get(node_id)
        if node:
            part = f"[{node['type'].upper()}] {node['description']}"
            context_parts.append(part)

    context = "\n".join(context_parts)

    prompt = (
        f"You are a legal assistant. Given the following reasoning chain and the user query, "
        f"please provide a concise, logical, and professional answer.\n\n"
        f"Reasoning Chain Context:\n{context}\n\n"
        f"User Query: {user_query}\n\n"
        f"Answer:"
    )

    return prompt

