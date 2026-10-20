import matplotlib.pyplot as plt
import networkx as nx

# 1. Inisialisasi Graf Tak Berarah (Undirected Graph)
G = nx.Graph()

# 2. Menambahkan Simpul dengan Teks Ringkas & Rapi
nodes = {
    0: "SMKN 1 Sagaranten\n(Kel. A)",
    1: "Pertigaan\nCigadog-Tangkil",
    2: "Jalur Sukabumi\n- Cianjur",
    3: "SMKN 1 Agrabinta\n(Koalisi B1)",
    4: "Titik Kritis:\nJl. Raya Rambay",
    5: "SMKN 1 Tegalbuleud\n(Koalisi B2)",
    6: "Polsek & Puskesmas\n(Zona Netral)",
}

for node_id, label in nodes.items():
    G.add_node(node_id, label=label)

# 3. Menambahkan Sisi (Edges) sesuai Jalur Rute & Relasi Konflik pada YAML
edges = [
    # Rute pergerakan fisik menuju titik kritis Rambay (Node 4)
    (0, 1),
    (1, 4),
    (3, 2),
    (2, 4),
    (5, 4),
    # Sisi Konflik Langsung Antar-Sekolah (Conflict Graph)
    (0, 3),  # Sagaranten vs Agrabinta
    (0, 5),  # Sagaranten vs Tegalbuleud
    # Jalur Evakuasi / Pengamanan ke Polsek (Node 6)
    (4, 6),
    (5, 6),
]
G.add_edges_from(edges)

# 4. Posisi Simpul (Diperluas Jaraknya Agar Teks Tidak Bertabrakan)
pos = {
    0: (0.0, 2.8),  # SMKN 1 Sagaranten (Puncak)
    1: (0.0, 1.3),  # Pertigaan Cigadog - Tangkil
    2: (1.5, 0.2),  # Jalur Sukabumi - Cianjur
    3: (2.6, -2.0),  # SMKN 1 Agrabinta (Kanan Bawah)
    4: (0.0, -0.6),  # Titik Kritis: Jl. Raya Rambay (Pusat Tengah)
    5: (-2.6, -2.0),  # SMKN 1 Tegalbuleud (Kiri Bawah)
    6: (-0.9, -2.5),  # Polsek & Puskesmas Tegalbuleud (Zona Netral)
}

# 5. Algoritma Pewarnaan Graf Greedy Coloring
# Sesuai GreedyColoring.run: warnai simpul menurut urutan ID,
# dengan memilih warna terkecil yang belum digunakan tetangganya.
coloring = {}
for node in sorted(G.nodes()):
    neighbor_colors = {
        coloring[neighbor]
        for neighbor in G.neighbors(node)
        if neighbor in coloring
    }

    color = 0
    while color in neighbor_colors:
        color += 1

    coloring[node] = color

# Palet warna pastel
color_palette = ["#ff9999", "#99ccff", "#ffeb99", "#d9b3ff", "#99ff99"]
node_colors = [color_palette[coloring[node] % len(color_palette)] for node in G.nodes()]

# 6. Visualisasi Graf
plt.figure(figsize=(10, 8))
plt.title(
    "Manajemen Konflik Tawuran Pelajar (Greedy Coloring - Skenario YAML)",
    fontsize=11,
    fontweight="bold",
    pad=15,
)

conflict_edges = [(0, 3), (0, 5)]
route_edges = [
    e for e in G.edges() if e not in conflict_edges and (e[1], e[0]) not in conflict_edges
]

# Gambar Simpul (Node Size diperbesar sedikit ke 3600 agar menampung teks)
nx.draw_networkx_nodes(
    G, pos, node_color=node_colors, node_size=3600, edgecolors="black", linewidths=1.2
)

# Gambar Sisi Jalur
nx.draw_networkx_edges(
    G,
    pos,
    edgelist=route_edges,
    width=1.8,
    alpha=0.75,
    edge_color="black",
    label="Jalur Pergerakan / Evakuasi",
)

# Gambar Sisi Konflik (Garis Putus-Putus Merah)
nx.draw_networkx_edges(
    G,
    pos,
    edgelist=conflict_edges,
    width=2.2,
    alpha=0.85,
    edge_color="red",
    style="dashed",
    label="Relasi Konflik Langsung",
)

# Tampilkan Label Nama Simpul (Font Size diperkecil ke 6.5)
labels = nx.get_node_attributes(G, "label")
nx.draw_networkx_labels(
    G, pos, labels=labels, font_size=6.5, font_family="sans-serif", font_weight="bold"
)

plt.legend(loc="upper right", fontsize=8.5, framealpha=0.9)
plt.axis("off")
plt.tight_layout()

# Tampilkan Grafik
plt.show()
