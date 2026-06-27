"""Transaction network graph operations for fraud detection."""
import networkx as nx
from collections import Counter
from datetime import datetime, timedelta
from django.db.models import Count
from django.utils import timezone
from .models import Transaction


def build_user_transaction_graph(user_id, days_back=90):
    """Build a network graph of user's transactions for fraud analysis."""
    cutoff_date = timezone.now() - timedelta(days=days_back)
    transactions = Transaction.objects.filter(
        user_id=user_id,
        created_at__gte=cutoff_date
    ).select_related('user').order_by('created_at')
    
    if not transactions.exists():
        return None, {
            'total_transactions': 0,
            'has_transactions': False,
            'graph_quality': 'insufficient_data'
        }
    
    G = nx.Graph()
    
    for i, transaction in enumerate(transactions):
        G.add_node(i, **{
            'transaction_id': transaction.id,
            'amount': float(transaction.amount),
            'location': transaction.location,
            'transaction_type': transaction.transaction_type,
            'timestamp': transaction.created_at,
            'risk_level': transaction.risk_level,
            'fraud_probability': transaction.fraud_probability,
            'hour_of_day': transaction.created_at.hour,
            'is_weekend': transaction.created_at.weekday() >= 5,
        })
    
    # Add edges based on time proximity (transactions within 2 hours)
    nodes = list(G.nodes())
    for i, node1 in enumerate(nodes):
        node1_time = G.nodes[node1]['timestamp']
        
        for j, node2 in enumerate(nodes[i+1:], i+1):
            node2_time = G.nodes[node2]['timestamp']
            time_diff = abs((node2_time - node1_time).total_seconds())
            
            if time_diff <= 7200:  # 2 hours in seconds
                edge_weight = max(0, 1 - (time_diff / 7200))
                
                amount1 = G.nodes[node1]['amount']
                amount2 = G.nodes[node2]['amount']
                amount_ratio = min(amount1, amount2) / max(amount1, amount2) if max(amount1, amount2) > 0 else 0
                
                type_match = G.nodes[node1]['transaction_type'] == G.nodes[node2]['transaction_type']
                
                edge_strength = (edge_weight * 0.4) + (amount_ratio * 0.3) + (type_match * 0.3)
                
                if edge_strength > 0.3:
                    G.add_edge(node1, node2, weight=edge_strength, time_diff=time_diff)
    
    stats = calculate_graph_statistics(G)
    
    return G, stats


def calculate_graph_statistics(G):
    """Calculate statistics for a transaction network graph."""
    if len(G.nodes()) == 0:
        return {
            'total_nodes': 0,
            'total_edges': 0,
            'density': 0,
            'average_clustering': 0,
            'average_path_length': 0,
            'is_connected': False,
            'num_components': 0,
            'graph_quality': 'empty'
        }
    
    stats = {
        'total_nodes': len(G.nodes()),
        'total_edges': len(G.edges()),
        'density': nx.density(G),
        'average_clustering': nx.average_clustering(G),
        'is_connected': nx.is_connected(G),
        'num_components': nx.number_connected_components(G),
    }
    
    if stats['is_connected'] and stats['total_nodes'] > 1:
        try:
            stats['average_path_length'] = nx.average_shortest_path_length(G)
        except nx.NetworkXError:
            stats['average_path_length'] = 0
    else:
        stats['average_path_length'] = 0
    
    degrees = [G.degree(node) for node in G.nodes()]
    stats['average_degree'] = sum(degrees) / len(degrees) if degrees else 0
    stats['max_degree'] = max(degrees) if degrees else 0
    
    weights = [G.edges[u, v]['weight'] for u, v in G.edges()]
    if weights:
        stats['average_edge_weight'] = sum(weights) / len(weights)
        stats['strong_edges'] = sum(1 for w in weights if w > 0.7)
        stats['weak_edges'] = sum(1 for w in weights if w <= 0.7)
    else:
        stats['average_edge_weight'] = 0
        stats['strong_edges'] = 0
        stats['weak_edges'] = 0
    
    hours = [G.nodes[node]['hour_of_day'] for node in G.nodes()]
    if hours:
        stats['hourly_distribution'] = Counter(hours)
    
    if stats['total_nodes'] < 5:
        stats['graph_quality'] = 'insufficient_data'
    elif stats['density'] < 0.1:
        stats['graph_quality'] = 'sparse'
    elif stats['density'] < 0.5:
        stats['graph_quality'] = 'moderate'
    else:
        stats['graph_quality'] = 'dense'
    
    return stats


def detect_network_anomalies(G):
    """Detect anomalous patterns in the transaction network."""
    anomalies = []
    
    if not G or len(G.nodes()) == 0:
        return anomalies
    
    degrees = dict(G.degree())
    if degrees:
        max_degree = max(degrees.values())
        avg_degree = sum(degrees.values()) / len(degrees)
        
        for node, degree in degrees.items():
            if degree > avg_degree * 2 and degree >= 3:
                anomalies.append({
                    'type': 'HIGH_DEGREE_CENTRALITY',
                    'severity': 'HIGH' if degree > avg_degree * 3 else 'MEDIUM',
                    'description': f"Node with unusually high connections ({degree} connections)",
                    'node_id': node,
                    'degree': degree,
                    'average_degree': round(avg_degree, 2)
                })
    
    triangles = nx.triangles(G)
    if triangles:
        max_triangles = max(triangles.values())
        avg_triangles = sum(triangles.values()) / len(triangles) if triangles else 0
        
        for node, triangle_count in triangles.items():
            if triangle_count > avg_triangles * 2 and triangle_count > 2:
                anomalies.append({
                    'type': 'HIGH_CLUSTERING',
                    'severity': 'HIGH' if triangle_count > avg_triangles * 3 else 'MEDIUM',
                    'description': f"Node with high clustering ({triangle_count} triangles)",
                    'node_id': node,
                    'triangle_count': triangle_count,
                    'average_triangles': round(avg_triangles, 2)
                })
    
    if len(G.nodes()) > 3:
        try:
            betweenness = nx.betweenness_centrality(G, k=min(100, len(G.nodes())))
            
            for node, bc in betweenness.items():
                if bc > 0.3:
                    anomalies.append({
                        'type': 'HIGH_BETWEENNESS',
                        'severity': 'HIGH' if bc > 0.5 else 'MEDIUM',
                        'description': f"Bridge node connecting different network segments (betweenness: {bc:.3f})",
                        'node_id': node,
                        'betweenness': round(bc, 3)
                    })
        except nx.NetworkXException:
            pass
    
    hours = []
    for node in G.nodes():
        hour = G.nodes[node]['hour_of_day']
        hours.append(hour)
    
    if hours:
        hour_counts = Counter(hours)
        total_transactions = len(hours)
        
        for hour, count in hour_counts.items():
            if count > total_transactions * 0.15:
                anomalies.append({
                    'type': 'TIME_ANOMALY',
                    'severity': 'MEDIUM' if count > total_transactions * 0.25 else 'LOW',
                    'description': f"Unusual concentration of transactions at hour {hour}:00 ({count} transactions)",
                    'hour': hour,
                    'transaction_count': count,
                    'total_transactions': total_transactions
                })
    
    return anomalies


def detect_hierarchical_clusters(G, min_cluster_size=5):
    """Detect hierarchical clusters in the transaction network."""
    clusters = []
    
    if not G or len(G.nodes()) == 0:
        return clusters
    
    nodes = list(G.nodes())
    visited = set()
    communities = []
    
    while len(visited) < len(nodes):
        remaining_nodes = [n for n in nodes if n not in visited]
        if not remaining_nodes:
            break
        
        current_community = {remaining_nodes[0]}
        visited.add(remaining_nodes[0])
        
        changed = True
        while changed:
            changed = False
            for node in list(remaining_nodes):
                if node in visited:
                    continue
                
                similarity_scores = []
                for community_node in current_community:
                    if G.has_edge(node, community_node):
                        edge_weight = G.edges[node, community_node]['weight']
                    else:
                        edge_weight = 0
                    
                    node_data = G.nodes[node]
                    community_node_data = G.nodes[community_node]
                    
                    time_similarity = 1.0 if node_data['hour_of_day'] == community_node_data['hour_of_day'] else 0.5
                    type_similarity = 1.0 if node_data['transaction_type'] == community_node_data['transaction_type'] else 0.3
                    amount_similarity = min(node_data['amount'], community_node_data['amount']) / max(node_data['amount'], community_node_data['amount']) if max(node_data['amount'], community_node_data['amount']) > 0 else 0
                    
                    similarity = (edge_weight + time_similarity + type_similarity + amount_similarity) / 4
                    similarity_scores.append(similarity)
                
                if similarity_scores and max(similarity_scores) > 0.6:
                    current_community.add(node)
                    visited.add(node)
                    changed = True
        
        if len(current_community) >= min_cluster_size:
            communities.append(current_community)
    
    for community in communities:
        if len(community) < min_cluster_size:
            continue
        
        subgraph = G.subgraph(community)
        density = nx.density(subgraph)
        
        fraud_probs = []
        for node in community:
            fraud_prob = G.nodes[node]['fraud_probability']
            fraud_probs.append(fraud_prob)
        
        avg_fraud_prob = sum(fraud_probs) / len(fraud_probs) if fraud_probs else 0
        
        risk_levels = Counter(G.nodes[node]['risk_level'] for node in community)
        
        hours = [G.nodes[node]['hour_of_day'] for node in community]
        hour_dist = Counter(hours)
        
        cluster_info = {
            'nodes': list(community),
            'size': len(community),
            'density': density,
            'average_fraud_probability': avg_fraud_prob,
            'avg_degree': sum(G.degree(node) for node in community) / len(community),
            'risk_level_distribution': risk_levels,
            'hour_distribution': hour_dist,
            'is_high_risk': avg_fraud_prob > 50,
            'intra_community_edges': len(list(subgraph.edges()))),
            'average_edge_weight': (sum(G.edges[u, v]['weight'] for u, v in subgraph.edges()) / len(list(subgraph.edges()))) if list(subgraph.edges()) else 0
        }
        
        clusters.append(cluster_info)
    
    return clusters


def analyze_transaction_graph_patterns(G):
    """Analyze patterns in the transaction graph for fraud detection."""
    patterns = {
        'temporal_patterns': {},
        'structural_patterns': {},
        'behavioral_patterns': {}
    }
    
    if not G or len(G.nodes()) == 0:
        return patterns
    
    hours = [G.nodes[node]['hour_of_day'] for node in G.nodes()]
    if hours:
        hourly_counts = Counter(hours)
        patterns['temporal_patterns']['hourly_distribution'] = hourly_counts
        
        max_hour_count = max(hourly_counts.values())
        peak_hours = [hour for hour, count in hourly_counts.items() if count == max_hour_count]
        patterns['temporal_patterns']['peak_hours'] = peak_hours
        patterns['temporal_patterns']['max_transactions_per_hour'] = max_hour_count
        
        weekends = sum(1 for node in G.nodes() if G.nodes[node]['is_weekend'])
        weekdays = len(G.nodes()) - weekends
        patterns['temporal_patterns']['weekend_transactions'] = weekends
        patterns['temporal_patterns']['weekday_transactions'] = weekdays
    
    if nx.is_connected(G):
        degree_centrality = nx.degree_centrality(G)
        
        patterns['structural_patterns']['degree_centrality'] = {
            'max': max(degree_centrality.values()),
            'min': min(degree_centrality.values()),
            'mean': sum(degree_centrality.values()) / len(degree_centrality),
        }
        
        patterns['structural_patterns']['cluster_coefficient'] = {
            'max': max(nx.clustering(G).values()),
            'min': min(nx.clustering(G).values()),
            'mean': sum(nx.clustering(G).values()) / len(nx.clustering(G)),
        }
    
    transaction_types = Counter(G.nodes[node]['transaction_type'] for node in G.nodes())
    patterns['behavioral_patterns']['transaction_types'] = transaction_types
    
    risk_levels = Counter(G.nodes[node]['risk_level'] for node in G.nodes())
    patterns['behavioral_patterns']['risk_levels'] = risk_levels
    
    return patterns