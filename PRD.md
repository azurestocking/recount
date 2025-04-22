# Mini PRD

**项目名称：** 针对创伤性事件受害者司法准备阶段的 AI Action Agent，用技术手段局部弥补制度性缺陷

---

## Painpoints

- 叙事负担过重（**MVP scope**）
- 资源分散，缺乏交叉性
- 紧急应对引导
- 设备锁定（硬件依赖）

---

## Overview: Pain Point 1

**HMW** reduce narrative burden while preserving legal usability for domestic violence survivors

### Key Hypothesis

- Survivors of domestic violence struggle to articulate traumatic experiences in highly rational, structured legal language before resorting to institutions (e.g., affidavits, police reports).
- Cognitive overload due to trauma
- Unfamiliarity with legal systems, terminology, proceedings, and expectations
- Disconnected evidence and broken timelines

> **AI** can bridge this gap by reconstructing coherent timelines from fragmented, sentimental inputs while minimizing re-traumatization

### Solution: An AI-Guided Interview

- Transforms fragmented memories into a coherent, legally-optimized timeline
- Minimizes narrative labor via step-by-step questioning (simulating an informed legal professional)
- Flags evidentiary gaps and constructs a timeline automatically
- Synthesizes the timeline into an affidavit using legally appropriate language

---

## Core Features

### 1. Guided Narrative Builder

**Purpose:**  
Interact with survivors (narrative, evidence) to collect fragmented information while minimizing trauma

**Core Architecture:**  
Input → AI Processing Pipeline → Output

#### Input Modalities

- **Audio**: Spoken descriptions of incidents
- **Text**: Typed answers to micro-questions
- **Image/Video**: Keyframe extraction + object detection

#### AI Processing

- Natural Language Understanding
- Extract key entities (people, objects, actions)
- Detect trauma-related keywords
- Dynamically select next micro-question based on gaps/specific framework
- Detect informational gaps
  - Ask related questions
- Integrate multimodal evidence
  - Detect temporal sequences
  - Detect conflicts in narrative/evidence

#### Output

- **Timeline**: Visualized narrative
- **Affidavit**: Text formatted to legal standards

### 2. Auxiliary Feature

**Low-hanging fruit:**  
Authorize social workers or attorneys to access the draft affidavit and exhibits for case evaluation

---

## Challenges

### Technical

- Precise entity recognition → confidence threshold tuning
- Multimodal evidence alignment → CLIP?
- Legal accuracy → Retrieval-Augmented Generation (RAG)
- Legally valid language → BERT trained on real affidavits?

### Ethical

- Coercion vs. autonomy → offer opt-outs and informed consent
- Systematic bias in datasets and language models
- Accountability → save original inputs, require attorney approval?
- Safety & privacy protections
