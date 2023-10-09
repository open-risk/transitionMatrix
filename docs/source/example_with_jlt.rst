Working with an actual matrix
==============================

The core capability of transitionMatrix is to produce estimated matrices but getting a realistic example requires quite some work. In this section we assume we have estimated one.

Lets look at a realistic example from the JLT paper

.. code::

    # Reproduce JLT Generator
    # We load it using different sources
    E = tm.TransitionMatrix(values=JLT)
    E_2 = tm.TransitionMatrix(json_file=dataset_path + "JLT.json")
    E_3 = tm.TransitionMatrix(csv_file=dataset_path + "JLT.csv")
    # Lets check there are no errors
    Error = E - E_3
    print(np.linalg.norm(Error))
    # Lets look at validation and generators"
    # Empirical matrices will not satisfy constraints exactly
    print(E.validate(accuracy=1e-3))
    print(E.characterize())
    print(E.generator())
    Error = E - expm(E.generator())
    # Frobenious norm
    print(np.linalg.norm(Error))
    # L1 norm
    print(np.linalg.norm(Error, 1))
    # Use pandas style API for saving to files
    E.to_csv("JLT.csv")
    E.to_json("JLT.json")

