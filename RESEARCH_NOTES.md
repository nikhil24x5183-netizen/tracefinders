# 🔬 RESEARCH & TECHNICAL NOTES — TRACE FINDERS

**Document Version:** `2.0.0`  
**SIH 2026 Problem Statement:** `SIH26189` — AI-Powered Criminal Network Analysis System  
**Subject Area:** Graph Theory, Multi-Hop Evidence Fusion, Computer Vision ANPR Analytics, Explainable AI (XAI)  

---

## 📑 Table of Contents
1. [Theoretical Graph Analytics & Centrality Models](#1-theoretical-graph-analytics--centrality-models)
2. [Multi-Hop Cross-Domain Correlation Mechanics](#2-multi-hop-cross-domain-correlation-mechanics)
3. [CCTV / DVR ANPR & Facial Recognition Analytics](#3-cctv--dvr-anpr--facial-recognition-analytics)
4. [Explainable AI (XAI) & Legal Admissibility Framework](#4-explainable-ai-xai--legal-admissibility-framework)
5. [Entity Resolution & Deduplication Algorithms](#5-entity-resolution--deduplication-algorithms)
6. [References & Academic Literature](#6-references--academic-literature)

---

## 1. Theoretical Graph Analytics & Centrality Models

Criminal network analysis relies on mathematical graph representations where entities are vertices $V$ and evidentiary associations are directed or undirected weighted edges $E$.

$$G = (V, E, W)$$

### 1.1 Degree Centrality
Measures immediate connectivity and operational interaction volume:

$$C_D(v) = \frac{\deg(v)}{|V| - 1}$$

Where $\deg(v)$ represents the total number of distinct evidentiary links associated with node $v$.

### 1.2 Betweenness Centrality (Brokerage Detection)
Identifies critical "broker" nodes controlling communication or financial flow between disparate criminal syndicates:

$$C_B(v) = \sum_{s \neq v \neq t \in V} \frac{\sigma_{st}(v)}{\sigma_{st}}$$

Where $\sigma_{st}$ is the total number of shortest paths from node $s$ to node $t$ and $\sigma_{st}(v)$ is the number of those paths that pass through node $v$. Nodes with high betweenness centrality are flagged as key logistical hubs or Hawala intermediaries.

### 1.3 PageRank Centrality (Syndicate Leader Identification)
Evaluates directional influence by propagating link weight recursively:

$$PR(p) = \frac{1-d}{N} + d \sum_{i \in M(p)} \frac{PR(i)}{L(i)}$$

Where $d = 0.85$ is the damping factor, $M(p)$ is the set of nodes linking to $p$, and $L(i)$ is the out-degree of node $i$.

---

## 2. Multi-Hop Cross-Domain Correlation Mechanics

Evidence in modern criminal investigations spans disparate data silos:

$$\text{Domain}_1 (\text{Telecom}) \longleftrightarrow \text{Domain}_2 (\text{ANPR CCTV}) \longleftrightarrow \text{Domain}_3 (\text{Banking}) \longleftrightarrow \text{Domain}_4 (\text{Blockchain})$$

### 2.1 Spatio-Temporal Correlation Matrix
The correlation score $S_{\text{corr}}(A, B)$ between two events $A$ and $B$ is computed as:

$$S_{\text{corr}}(A, B) = w_t \cdot e^{-\lambda_t |t_A - t_B|} + w_s \cdot e^{-\lambda_s d(L_A, L_B)} + w_e \cdot \text{Sim}(E_A, E_B)$$

Where:
- $t_A, t_B$ are event timestamps.
- $d(L_A, L_B)$ is the Haversine distance between geographical coordinates.
- $\text{Sim}(E_A, E_B)$ is entity attribute similarity (Jaro-Winkler distance on names/aliases).
- $w_t, w_s, w_e$ are domain weighting constants ($0.4, 0.35, 0.25$).

---

## 3. CCTV / DVR ANPR & Facial Recognition Analytics

### 3.1 Automatic Number Plate Recognition (ANPR) Pipeline
1. **Frame Extraction & Preprocessing**: Dual-pass contrast enhancement and CLAHE adaptive histogram equalization.
2. **Bounding Box Detection**: YOLOv8-Nano vehicle license plate detector.
3. **OCR Feature Extraction**: Tesseract-v5 & EasyOCR ensemble parser trained on Indian HSRP (High Security Registration Plate) font geometry.

### 3.2 24-Hour Timeline Marker Aggregation
Events from 12 active surveillance cameras (`CAM-01` through `CAM-12`) are indexed into a temporal B-tree index, rendering real-time sighting markers across 24-hour windows (00:00 to 23:59 IST).

---

## 4. Explainable AI (XAI) & Legal Admissibility Framework

To satisfy judicial requirements under Section 65B of the Indian Evidence Act / Bharatiya Sakshya Adhiniyam, 2023, automated outputs must be fully transparent.

```
┌─────────────────────────────────────────────────────────────────┐
│                    XAI ASSESSMENT STRUCTURE                     │
├─────────────────────────────────────────────────────────────────┤
│  1. CORRELATION RATIONALE   ➔ Why these entities were linked   │
│  2. FLAGGING REASONING     ➔ Suspicious pattern criteria        │
│  3. CONFIDENCE METRIC      ➔ Calculated probability (e.g. 88%)  │
│  4. ALTERNATIVE HYPOTHESIS ➔ Defense counter-argument scenario │
│  5. EVIDENTIARY HASH REF   ➔ SHA-256 Chain of Custody Ref     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Entity Resolution & Deduplication Algorithms

When ambiguous candidates (e.g., `Arjun S.` vs `Arjun Sharma`) enter the system, the entity resolution engine evaluates identity likelihood using a multi-attribute similarity vector:

$$\mathbf{V}_{\text{match}} = \begin{bmatrix} \text{JaroWinkler}(\text{Name}_1, \text{Name}_2) \\ \text{GeographicOverlap}(\text{City}_1, \text{City}_2) \\ \text{CommonCoContacts}(\text{CDR}_1, \text{CDR}_2) \end{bmatrix}$$

Match Confidence Score $\mathcal{M} = \mathbf{w}^T \mathbf{V}_{\text{match}}$. Candidates scoring $0.40 \le \mathcal{M} < 0.75$ are placed in the **Entity Resolution Review Queue** for analyst verification.

---

## 6. References & Academic Literature

1. Freeman, L. C. (1977). *A set of measures of centrality based on betweenness*. Sociometry, 40(1), 35-41.
2. Page, L., Brin, S., Motwani, R., & Winograd, T. (1999). *The PageRank citation ranking: Bringing order to the web*. Stanford InfoLab Technical Report.
3. Krebs, V. E. (2002). *Uncloaking terrorist networks*. First Monday, 7(4).
4. Indian Evidence Act / Section 65B Admissibility of Electronic Records / Bharatiya Sakshya Adhiniyam, 2023.
5. Smart India Hackathon (SIH 2026) Problem Statement `SIH26189`.
