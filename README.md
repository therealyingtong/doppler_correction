# doppler_correction

from root directory run:

unshifted:
```
python3 src/main.py ../data/ALICE_12Apr_19_3 ../data/BOB_12Apr_19_3 ../data/GALASSIA-TLE.txt ../data/GALASSIA-15723-pass-48.txt unshifted
```

propagation delay:
```
python3 src/main.py ../data/ALICE_12Apr_19_3 ../data/BOB_12Apr_19_3 ../data/GALASSIA-TLE.txt ../data/GALASSIA-15723-pass-48.txt propagationDelay
```

clock drift shift:
```
python3 src/main.py ../data/ALICE_12Apr_19_3 ../data/BOB_12Apr_19_3 ../data/GALASSIA-TLE.txt ../data/GALASSIA-15723-pass-48.txt clockDriftShift
```

alice and bob:
```
python3 src/main.py ../data/ALICE_12Apr_19_3 ../data/BOB_12Apr_19_3 ../data/GALASSIA-TLE.txt ../data/GALASSIA-15723-pass-48.txt aliceBob
```

software used: MATLAB, LaTeX

paper generated at `paper/doppler_correction.pdf`.
