from qiskit import Aer, ClassicalRegister, execute, QuantumCircuit, QuantumRegister
from qiskit.tools.monitor import job_monitor



qubits = 32
devices = 2 # increase this number to simulate having even more devices available
q = QuantumRegister(qubits)
c = ClassicalRegister(qubits)
qc = QuantumCircuit(q, c)

def qrandint(min, max): # generates integers
    range = max - min
    qaddend = range * qmeasure()
    qsum = qaddend + min
    qint = int(qsum +.5)
    return qint

def quniform(min, max): # generates floats
    range = max - min
    qaddend = range * qmeasure()
    qsum = qaddend + min
    return qsum
    
def qreset(): # resets qubits for reuse
    j = 0
    while j < qubits:
        qc.reset(q[j])
        j = j + 1
    
def qexecute(): # runs on the simulator
    i = 0
    while i < qubits:
        qc.h(q[i])
        i = i + 1
    qc.measure(q, c)
    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend, shots=1)
    job_monitor(job)
    result = job.result()
    mraw = result.get_counts(qc)
    mstr = str(mraw)
    return mstr

def qmeasure(): # converts measurements from the simulator to a float multiplier
    qdevice = 0
    subtotal = 0 
    while qdevice < devices:
        m = qexecute()
        for i in range(qubits):
            subtotal = subtotal + (int(m[i+2]) * 2**(i + (32 * qdevice)))
        multiplier = subtotal / (2**(qubits * devices))
        if (qdevice < (devices - 1)):
            qreset()
        qdevice = qdevice + 1 
    return multiplier



# specify min and max values for the random integer and/or float; the multiplier determines where to find your random number within your specified range
print(qrandint(-100, 100))
print(quniform(-1, 1))
