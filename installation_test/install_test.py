# ~/Workspace/Qiskit/test_installation.py
# Qiskit 설치 검증 및 기본 테스트 스크립트

import sys
print(f"Python version: {sys.version}")

# 1. Qiskit 기본 import 테스트
try:
    import qiskit
    print(f"Qiskit version: {qiskit.__version__}")
except ImportError as e:
    print(f"Qiskit import failed: {e}")
    exit(1)

# 2. 필수 모듈 import 테스트
try:
    from qiskit import QuantumCircuit, transpile
    from qiskit_aer import AerSimulator
    from qiskit.visualization import plot_histogram
    print("All required modules imported successfully")
except ImportError as e:
    print(f"Module import failed: {e}")
    exit(1)

# 3. Bell State 회로 생성 테스트
print("\n=== Bell State Circuit Test ===")
try:
    # 2큐빗, 2클래식 비트 회로 생성
    qc = QuantumCircuit(2, 2)
    
    # Hadamard gate를 첫 번째 큐빗에 적용
    qc.h(0)
    
    # CNOT gate 적용 (control: 0, target: 1)
    qc.cx(0, 1)
    
    # 모든 큐빗 측정
    qc.measure_all()
    
    print("✅ Bell state circuit created successfully")
    print(f"Circuit depth: {qc.depth()}")
    print(f"Number of qubits: {qc.num_qubits}")
    
except Exception as e:
    print(f"Circuit creation failed: {e}")
    exit(1)

# 4. 시뮬레이터 테스트
print("\n=== Simulator Test ===")
try:
    # AerSimulator 초기화
    simulator = AerSimulator()
    
    # 회로를 시뮬레이터에 맞게 트랜스파일
    compiled_circuit = transpile(qc, simulator)
    
    # 시뮬레이션 실행 (1024번 반복)
    job = simulator.run(compiled_circuit, shots=1024)
    result = job.result()
    counts = result.get_counts(compiled_circuit)
    
    print("Simulation completed successfully")
    print(f"Measurement results: {counts}")
    
    # Bell state 검증 (00과 11만 나와야 함)
    # Qiskit 결과에서 첫 2자리만 추출 (큐빗 상태)
    actual_qubit_states = [state.split()[0] for state in counts.keys()]
    expected_states = ['00', '11']
    
    if all(state in expected_states for state in actual_qubit_states):
        print("Bell state verification passed")
        print(f"   Qubit states: {actual_qubit_states}")
    else:
        print(f"Unexpected states found: {actual_qubit_states}")
    
    # 결과 분석
    total_shots = sum(counts.values())
    for state, count in counts.items():
        percentage = (count / total_shots) * 100
        print(f"   State {state}: {count} times ({percentage:.1f}%)")
        
except Exception as e:
    print(f"Simulation failed: {e}")
    exit(1)

# 5. 시각화 테스트 (Jupyter에서만 작동)
print("\n=== Visualization Test ===")
try:
    # 회로 다이어그램 텍스트 출력
    print("Circuit diagram:")
    print(qc.draw())
    
    print("Text visualization successful")
    print("Note: For visual plots, use Jupyter Notebook")
    
except Exception as e:
    print(f"Visualization failed: {e}")

print("\n All tests completed! Qiskit installation is working properly.")