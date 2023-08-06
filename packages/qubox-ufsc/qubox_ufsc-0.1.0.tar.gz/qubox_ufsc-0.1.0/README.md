# QuBOX UFSC Client

QuBOX is a portable quantum computing simulator developed by Quantuloop
for the [Ket language](https://quantumket.org). Accelerated by GPU, QuBOX has two simulation modes, 
being able to simulate more than 30 quantum bits.
    
In partnership with Quantuloop, the Quantum Computing Group - UFSC provides
free remote access to a QuBOX simulator. You can use this client to access 
the QuBOX hosted at the Federal University of Santa Catarina (UFSC).

See <https://qubox.ufsc.br> for more information.

## Installation

```shell
pip install qubox-ufsc
```

## Usage

```python
from ket import * # import quantum types and functions
import qubox_ufsc # import the QuBOX UFSC Client


# Request access to the QuBOX UFSC
qubox_ufsc.login(
    name="Your Name",
    email="you_email@example.com",
    affiliation="Your Affiliation"
)

# Configure the quantum execution
qubox_ufsc.config(
    mode="sparse",
    precision=1,
) # Every quantum execution after this line will run on the QuBOX

##################################
# Bell State preparation example #
##################################
a, b = quant(2)
cnot(H(a), b)
print(dump(a+b).show())
```
