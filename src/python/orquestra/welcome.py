"""
This module saves a welcome message.
"""
import numpy
import json

from qiskit import QuantumRegister,ClassicalRegister,QuantumCircuit
from qiskit import execute 
def welcome():
    message = "Welcome to Orquestra!"

    message_dict = {}
    message_dict["message"] = message
    message_dict["schema"] = "message"

    with open("welcome.json",'w') as f:
        f.write(json.dumps(message_dict, indent=2)) # Write message to file as this will serve as output artifact

pi = numpy.pi

def cnza(a,i,j,q,qc):
  """ general controlled-Z^a gate
  a is any float
  i is a list of n integers giving the indices for the controlling qubits
  j is the index of the target qubit
  q is the qubit register
  qc is the quantum circuit containing q
  """
  print("Called cnza with a=" + str(a) + ", i=" + str(i) + ", j=" + str(j))

  if hasattr(i, "__len__"): # check if i is a scalar or a list
    scalar = False
    n = len(i)
  else:
    scalar = True
    n = 1

  if n == 1:  # end of the recursion - apply a controlled phase gate
    if scalar:
      qc.cu1(a*pi,q[i],q[j])
    else:
      qc.cu1(a*pi,q[i[0]],q[j])
  elif n > 1: # apply the recursion rule for a controlled gate
    qc = cnza(a/2,i[n-1],j,q,qc)
    qc = cnx(i[0:n-1],i[n-1],q,qc)
    qc = cnza(-a/2,i[n-1],j,q,qc)
    qc = cnx(i[0:n-1],i[n-1],q,qc)
    qc = cnza(a/2,i[0:n-1],j,q,qc)

  return qc

def cnz(i,j,q,qc):
  """ general controlled-Z gate
  i is a list of n integers giving the indices for the controlling qubits
  j is the index of the target qubit
  q is the qubit register
  qc is the quantum circuit containing q
  """
  print("Called cnz with i=" + str(i) + ", j=" + str(j))
  qc = cnza(1,i,j,q,qc)
  return qc

def cnx(i,j,q,qc):
  """ general Toffoli gate
  i is a list of n integers giving the indices for the controlling qubits
  j is the index of the target qubit
  q is the qubit register
  qc is the quantum circuit containing q
  """
  print("Called cnx with i=" + str(i) + ", j=" + str(j))
  qc.h(q[j])
  qc = cnz(i,j,q,qc)
  qc.h(q[j])
  return qc

def run():
	i = [0,1,2] # indices of controlling qubits (can also be a scalar)
	n = len(i)  # number of controlling qubits
	j = n       # index of target qubit

	q = QuantumRegister(n+1)   # Create a quantum register with n+1 qubits.
	c = ClassicalRegister(n+1) # Create a classical register with n+1 bits.
	qc = QuantumCircuit(q, c)  # Create a quantum circuit, combining q and c.

	# Build and measure a quantum circuit using the Toffoli gate
	qc.x(q)
	qc.x(q[0])
	qc = cnx(i,j,q,qc)
	qc.measure(q,c)

# Compile and run the Quantum Program on a selected backend
	job = execute(qc, backend='local_qasm_simulator', shots=1024)
	results = job.result()

	print("Run: ", results)
	print(results.get_counts(qc))
# The first n bits of the outcome should be 1.
# The remaining (rightmost) bit should be 0.
