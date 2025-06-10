# 🔐 BB84 Quantum Dashboard

This Streamlit-based application provides interactive demonstrations of quantum key distribution (QKD) methods and classical cryptography comparisons. It focuses on the BB84 protocol, classical RSA encryption, Shor’s quantum factoring algorithm, and explores various quantum algorithms.

## 🚀 Features

* **Quantum vs Classical Cryptography**: Interactive simulation comparing BB84 with classical RSA.
* **BB84 Protocol Simulation**: Test quantum key distribution with or without eavesdropping (Eve).
* **Quantum Algorithms Lab**: Includes simulations of Grover's, Deutsch–Jozsa, and Bernstein–Vazirani algorithms.
* **Post-Quantum Cryptography (PQC)**: Explore future threats to classical encryption.
* **Quantum Attack Demonstrations**: Visualize Shor's algorithm and quantum threats to RSA.

## 🛠️ Installation

### Prerequisites

* Anaconda or Miniconda

### Setup

Clone this repository:

```bash
git clone <your_repo_url>
cd bb84-quantum-dashboard
```

Create the conda environment:

```bash
conda env create -f environment.yml
conda activate bb84_Q
```

## ▶️ Running the App

Launch Streamlit:

```bash
streamlit run app.py
```

Open the URL displayed in the terminal (usually `http://localhost:8501`).

## 📂 Project Structure

```plaintext
bb84-quantum-dashboard/
├── app.py
├── components/
│   ├── helpers.py
│   ├── tab1_bb84.py
│   ├── tab2_rsa.py
│   ├── tab3_comparison.py
│   ├── tab4_shor.py
│   ├── tab5_future_threat.py
│   ├── tab6_algorithms.py
│   └── algorithms/
│       ├── grover.py
│       ├── deutsch_jozsa.py
│       └── bernstein_vazirani.py
├── requirements.txt
└── environment.yml
```

## 📦 Dependencies

Core dependencies include:

* Qiskit (`1.0.2`)
* Qiskit Aer (`0.14.1`)
* Streamlit (`1.33.0`)
* Cryptography (`41.0.5`)
* Pandas, NumPy, Matplotlib
* pylatexenc (`2.10`) [for circuit visualization]

## 🤝 Contributing

Feel free to open issues or submit pull requests to enhance functionality or fix bugs.


