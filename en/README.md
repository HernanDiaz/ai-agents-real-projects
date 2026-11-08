<div align="center">
  <h1>Agents II: Working with Agents on Real Projects</h1>
  <h3><em>The workbench of a coding agent: instructions, contracts, verification and review, with open models in Python</em></h3>
  <p>by <strong>Hernán Díaz Rodríguez, PhD</strong> · Professor at the University of Oviedo</p>
  <p>
    <a href="https://creativecommons.org/licenses/by-nc/4.0/"><img src="https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg" alt="License: CC BY-NC 4.0"></a>
    <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Colab-free%20T4%20GPU-orange?logo=googlecolab" alt="Colab">
  </p>
</div>

---

## The book

**Agents II** takes the agent from a single file to a real repository: the management program of **North Cycles**, a bicycle store in Portland, Oregon, with several modules, tests and a task list like a real team's. There the agent fails a lot, and hardly ever because the model is bad: it doesn't know what it may touch, how to check that it is done, what happened in the previous session or who reviews its work. We call all of that the **workbench**, and each chapter adds a piece and measures it: instructions you can check, state between sessions, scope contracts, feedback and verification gates, a reviewer with a rubric, understanding before changing, delegating with isolation, specifications, success metrics, and permissions and limits. The last chapter installs the whole workbench in a repository the agent has never seen, that of a veterinary clinic.

What is measured is not only how many tasks the agent solves, but how much its word "done" is worth, how many rules it breaks, how many tasks it escalates with an explanation instead of hiding them, and how much person time it costs. Everything is programmed in Python with **free, open models**, with no API keys or paid services: Qwen3-4B-Instruct-2507 on Colab's free GPU. Tasks are checked with hidden tests the agent never sees, and every figure in the book comes from an experiment you can repeat in the chapter's notebook. This edition is not a plain translation: the store, the clinic, their data and every experiment are its own, run in English.

It belongs to the **AI in Practice** series: hands-on books on artificial intelligence, with original experiments, a notebook and a video in every chapter.

> *¿Prefieres español?* La edición española, **Agentes II: trabajar con agentes en proyectos reales**, está en la [raíz del repositorio](../).

---

## Chapters

Each chapter has its notebook on Google Colab and its video, with Robotín and the author.

| Ch. | Title | Notebook | Video |
|-----|-------|----------|-------|
| 1 | Why agents fail: the workbench | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HernanDiaz/ai-agents-real-projects/blob/main/en/notebooks/1_Why_agents_fail.ipynb) | coming soon |
| 2 | Instructions you can check | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HernanDiaz/ai-agents-real-projects/blob/main/en/notebooks/2_Instructions_you_can_check.ipynb) | coming soon |
| 3 | Repository memory and initialization | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HernanDiaz/ai-agents-real-projects/blob/main/en/notebooks/3_Repository_memory.ipynb) | coming soon |
| 4 | Scope contracts | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HernanDiaz/ai-agents-real-projects/blob/main/en/notebooks/4_Scope_contracts.ipynb) | coming soon |
| 5 | Feedback and verification gates | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HernanDiaz/ai-agents-real-projects/blob/main/en/notebooks/5_Feedback_and_verification.ipynb) | coming soon |
| 6 | The reviewer | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HernanDiaz/ai-agents-real-projects/blob/main/en/notebooks/6_The_reviewer.ipynb) | coming soon |
| 7 | Understand before you change | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HernanDiaz/ai-agents-real-projects/blob/main/en/notebooks/7_Understand_before_you_change.ipynb) | coming soon |
| 8 | Delegating with isolation | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HernanDiaz/ai-agents-real-projects/blob/main/en/notebooks/8_Delegating_with_isolation.ipynb) | coming soon |
| 9 | From the real workflow to the specification | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HernanDiaz/ai-agents-real-projects/blob/main/en/notebooks/9_From_workflow_to_specification.ipynb) | coming soon |
| 10 | Success metrics | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HernanDiaz/ai-agents-real-projects/blob/main/en/notebooks/10_Success_metrics.ipynb) | coming soon |
| 11 | Permissions, checkpoints and cost limits | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HernanDiaz/ai-agents-real-projects/blob/main/en/notebooks/11_Permissions_and_limits.ipynb) | coming soon |
| 12 | Project: a workbench for a real repository | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HernanDiaz/ai-agents-real-projects/blob/main/en/notebooks/12_The_workbench.ipynb) | coming soon |

---

## How to use the notebooks

- Click **Open in Colab** and run the cells in order. The first cell installs the library versions the book was checked with.
- Turn on the free GPU: *Runtime → Change runtime type → T4 GPU*. The model takes about 8 GB and the first time it takes a few minutes to download. Chapter 10 and many sections of the others need no GPU.
- The notebooks download the `en/data/` and `en/shared/` folders of this repository by themselves the first time.
- A full experiment takes hours; the notebooks run short samples, and the full results the book cites are saved in `data/results/`, so almost every exercise can be done without a GPU. The figures may change slightly with another GPU or other library versions.

---

## Folder structure

```
en/
├── notebooks/         ← One notebook per chapter
├── shared/            ← The agent's tools: read, search, edit, run the tests
├── data/
│   ├── north_cycles/      ← The store's repository the agent works on
│   ├── tasks/             ← Tasks T01 to T35, with their hidden tests and a reference solution
│   ├── northside_vet/     ← The veterinary clinic's repository (chapter 12)
│   ├── incidents/         ← The clinic's incidents I01 to I08
│   └── results/           ← The results of the book's experiments
└── notebook/N/        ← The book's links to each notebook on Colab
```

---

## Data

North Cycles, Northside Veterinary Clinic and all their data are fictional. The agent always works on a copy of the repository made for each task, so you can make mistakes without consequences.

| Folder | Contents | Chapters |
|--------|----------|----------|
| `north_cycles/` | The store's management program: orders, shipping, returns, stock, estimates, invoices, notices and reports, with its tests | 1 to 11 |
| `tasks/` | 35 tasks (bugs, new features, rule changes and refactorings), each with its request, its contract, its hidden tests and a reference solution | 1 to 9 |
| `northside_vet/` | A veterinary clinic's management program: appointments, vaccines, pharmacy, invoices and notices | 12 |
| `incidents/` | Eight incidents at the clinic, written by the people who suffer them, with their contract and hidden tests | 12 |
| `results/` | The book's runs, with every attempt of the agent; chapters 10 and 11 analyze them without running anything again | 1 to 12 |

---

## License

This material is distributed under the [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/) license: it can be used and adapted for teaching and study, crediting the author, but not for commercial purposes. The model used by the notebooks, Qwen3-4B-Instruct-2507, is distributed under the Apache 2.0 license.
