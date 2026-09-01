import networkx as nx
from typing import Dict, List, Any

class GraphAnalyticsEngine:
    def __init__(self):
        pass

    def analyze_graph(self, nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> Dict[str, Any]:
        G = nx.Graph()

        node_map = {}
        for n in nodes:
            G.add_node(n["id"], label=n.get("label", n["id"]), type=n.get("type", "UNKNOWN"), risk_score=n.get("risk_score", 50))
            node_map[n["id"]] = n

        for e in edges:
            G.add_edge(e["source"], e["target"], relation=e.get("relation", "CONNECTED"), domain=e.get("domain", "GENERAL"))

        if G.number_of_nodes() == 0:
            return {"metrics": {}, "communities": [], "influential_entities": []}

        deg_centrality = nx.degree_centrality(G)
        try:
            bet_centrality = nx.betweenness_centrality(G)
        except Exception:
            bet_centrality = {n: 0.0 for n in G.nodes()}

        try:
            pagerank = nx.pagerank(G, max_iter=100)
        except Exception:
            pagerank = {n: 1.0 / len(G.nodes()) for n in G.nodes()}

        communities_list = []
        try:
            from networkx.algorithms.community import greedy_modularity_communities
            comms = greedy_modularity_communities(G)
            for idx, c in enumerate(comms):
                communities_list.append({
                    "community_id": f"COMM-{idx+1}",
                    "member_ids": list(c),
                    "size": len(c)
                })
        except Exception:
            communities_list = [{"community_id": "COMM-1", "member_ids": list(G.nodes()), "size": len(G.nodes())}]

        influential = []
        for n_id in G.nodes():
            node_info = node_map.get(n_id, {"label": n_id, "type": "UNKNOWN", "risk_score": 50})
            score = (deg_centrality.get(n_id, 0) * 0.4) + (bet_centrality.get(n_id, 0) * 0.4) + (pagerank.get(n_id, 0) * 0.2)
            influential.append({
                "id": n_id,
                "label": node_info.get("label", n_id),
                "type": node_info.get("type", "UNKNOWN"),
                "degree_centrality": round(deg_centrality.get(n_id, 0), 4),
                "betweenness_centrality": round(bet_centrality.get(n_id, 0), 4),
                "pagerank": round(pagerank.get(n_id, 0), 4),
                "influence_score": round(score, 4),
                "assessment": "High Network Centrality - Potential Coordination Hub (Requires Investigation)" if score > 0.08 else "Standard Network Participant"
            })

        influential.sort(key=lambda x: x["influence_score"], reverse=True)

        return {
            "node_count": G.number_of_nodes(),
            "edge_count": G.number_of_edges(),
            "communities": communities_list,
            "influential_entities": influential[:15]
        }

    def find_shortest_path(self, nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]], source_id: str, target_id: str) -> Dict[str, Any]:
        G = nx.Graph()
        for e in edges:
            G.add_edge(e["source"], e["target"], relation=e.get("relation", "CONNECTED"), domain=e.get("domain", "GENERAL"), details=e.get("details", ""))

        if not G.has_node(source_id) or not G.has_node(target_id):
            return {"found": False, "reason": "One or both nodes not present in graph canvas."}

        try:
            path = nx.shortest_path(G, source=source_id, target=target_id)
            path_edges = []
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                edge_data = G.get_edge_data(u, v)
                path_edges.append({
                    "step": i + 1,
                    "from": u,
                    "to": v,
                    "relation": edge_data.get("relation", "CONNECTED"),
                    "domain": edge_data.get("domain", "GENERAL"),
                    "details": edge_data.get("details", "")
                })

            return {
                "found": True,
                "hop_count": len(path) - 1,
                "path_node_ids": path,
                "path_steps": path_edges
            }
        except nx.NetworkXNoPath:
            return {"found": False, "reason": f"No connected path exists between {source_id} and {target_id}."}

graph_engine = GraphAnalyticsEngine()
