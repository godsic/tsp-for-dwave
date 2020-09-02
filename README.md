# Traveling Santa Problem Formulated as [QUBO](https://en.wikipedia.org/wiki/Quadratic_unconstrained_binary_optimization) for D-Wave Quantum Annealer

Based on the ["Traveling Santa Problem"](http://quantumalgorithmzoo.org/traveling_santa/) tutorial by Stephen Jordan @ Microsoft Quantum and driven by the ["Quantum Programming 101: Solving a Problem From End to End"](https://youtu.be/Q4FE4jou5CA) webinar by D-Wave

## Prerequisites
- Python 3.8 and [pipenv](https://docs.pipenv.org/);
- clone this repo 
    ```bash
    git clone https://github.com/godsic/tsp-for-dwave.git && cd tsp-for-dwave
    ```
- configure Python environment with [D-Wave Ocean SDK](https://docs.ocean.dwavesys.com/en/stable/) by running the following command:
    ```bash
    pipenv install
    ```
- register at [D-Wave Leap](https://cloud.dwavesys.com/leap/) and obtain corresponding API key;
- configure environment with [dwave CLI](https://docs.ocean.dwavesys.com/en/stable/docs_cli.html#cli-example-config)  providing the API key when asked:
    ```bash
    dwave config create
    ```

## Usage
Simply execute 
```bash
pipenv run ./tsp.py
```
and will print QUBO coefficients, obtained solutions, their energies, frequencies during sampling and indicate any [chain breaking](https://docs.ocean.dwavesys.com/en/stable/concepts/embedding.html?highlight=chain%20breaking#chain-strength) events.

## Code Specifics

The quality of the solution is determined by
- `l_I` - weight of the constraint on the required number of travel segments;
- `l_II` - weight of the closed trip constraint;
- the `chain_strength` parameter is determined automatically; contrary to the [D-Wave recommendations](https://www.dwavesys.com/sites/default/files/14-1041A-A_Setting_The_Chain_Strength.pdf), quarter of the maximum absolute value of QUBO coefficients seem to work best for this particular problem.